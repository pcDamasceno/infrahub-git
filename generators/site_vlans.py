from infrahub_sdk.generator import InfrahubGenerator


class SiteVlans(InfrahubGenerator):
    """Create the VLAN of one VLAN definition at every site.

    Infrahub allocates the VLAN ID from the pool of each site, because vlan_id is a NumberPool attribute scoped by
    site. An upsert keeps the VLAN ID of a VLAN that already exists. The generator deletes the VLANs it created in an
    earlier run and no longer creates, for example the VLAN of a site that was deleted.
    """

    async def generate(self, data: dict) -> None:
        definition = data["NetworkVlanDefinition"]["edges"][0]["node"]
        for site in data["LocationSite"]["edges"]:
            vlan = await self.client.create(
                kind="NetworkVlan",
                data={"name": definition["name"]["value"], "site": site["node"]["id"]},
            )
            await vlan.save(allow_upsert=True)
