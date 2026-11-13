import logging

from infrahub_sdk import InfrahubClient

from lib.inventory import device_names


async def run(client: InfrahubClient, log: logging.Logger, branch: str) -> None:
    devices = await client.all(kind="NetworkDevice", branch=branch)
    for name in device_names(devices):
        log.info(name)
