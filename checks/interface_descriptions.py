from infrahub_sdk.checks import InfrahubCheck


class InterfaceDescriptions(InfrahubCheck):
    query = "device_config"

    def validate(self, data: dict) -> None:
        device = data["NetworkDevice"]["edges"][0]["node"]
        for edge in device["interfaces"]["edges"]:
            interface = edge["node"]
            if not interface["description"]["value"]:
                self.log_error(
                    message=f"{device['name']['value']} {interface['name']['value']} has no description",
                    object_id=interface["id"],
                    object_type="NetworkInterface",
                )
