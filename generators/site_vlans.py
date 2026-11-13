from infrahub_sdk.generator import InfrahubGenerator


class SiteVlans(InfrahubGenerator):
    """Create the VLAN of one VLAN definition at every site.

    The VLAN ID of a new VLAN is allocated from the number pool created in Infrahub for NetworkVlan.vlan_id. When that
    pool is scoped by site, each site gets its own VLAN IDs. A VLAN that already exists keeps its VLAN ID, because the
    generator does not save it again. The generator deletes the VLANs it created in an earlier run and no longer
    creates or keeps, for example the VLAN of a site that was deleted.
    """

    async def generate(self, data: dict) -> None:
        definition = data["NetworkVlanDefinition"]["edges"][0]["node"]
        name = definition["name"]["value"]
        pool_id = self._vlan_id_pool(data=data)

        existing_by_site = {
            vlan["node"]["site"]["node"]["id"]: vlan["node"]["id"]
            for vlan in data["NetworkVlan"]["edges"]
            if vlan["node"]["site"]["node"]
        }

        for site in data["LocationSite"]["edges"]:
            site_id = site["node"]["id"]
            existing_id = existing_by_site.get(site_id)
            if existing_id:
                # The VLAN is not saved again, so its VLAN ID stays as allocated; recording it stops this run deleting it
                await self.client.group_context.add_related_nodes(ids=[existing_id])
                continue
            vlan = await self.client.create(
                kind="NetworkVlan",
                data={
                    "name": name,
                    "site": site_id,
                    "vlan_id": {"from_pool": {"id": pool_id}},
                },
            )
            await vlan.save()

    @staticmethod
    def _vlan_id_pool(data: dict) -> str:
        """Return the id of the one number pool that allocates NetworkVlan.vlan_id.

        Raises:
            ValueError: When no pool, or more than one pool, allocates NetworkVlan.vlan_id.

        """
        pools = [edge["node"] for edge in data["CoreNumberPool"]["edges"]]
        if len(pools) != 1:
            names = ", ".join(pool["name"]["value"] for pool in pools) or "none"
            raise ValueError(
                f"Expected one number pool for NetworkVlan.vlan_id, found {len(pools)} ({names}). "
                "Create one number pool with node NetworkVlan and node attribute vlan_id, scoped by site."
            )
        return pools[0]["id"]
