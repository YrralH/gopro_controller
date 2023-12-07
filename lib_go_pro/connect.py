

import re
import sys
import asyncio
import argparse
from typing import Dict, Any, List, Callable, Optional

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from lib_go_pro.logger import logger


async def connect_ble(
    notification_handler: Callable[[int, bytes], None],
    identifier: Optional[str] = None
) -> BleakClient:
    """Connect to a GoPro, then pair, and enable notifications

    If identifier is None, the first discovered GoPro will be connected to.

    Retry 10 times

    Args:
        notification_handler (Callable[[int, bytes], None]): callback when notification is received
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Raises:
        Exception: couldn't establish connection after retrying 10 times

    Returns:
        BleakClient: connected client
    """

    # Map of discovered devices indexed by name
    devices: Dict[str, BleakDevice] = {}

    # Scan for devices
    logger.info("Scanning for bluetooth devices...")

    # Scan callback to also catch nonconnectable scan responses
    # pylint: disable=cell-var-from-loop
    def _scan_callback(device: BleakDevice, _: Any) -> None:
        # Add to the dict if not unknown
        if device.name and device.name != "Unknown":
            devices[device.name] = device

    # Now get list of connectable advertisements
    for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
        if device.name != "Unknown" and device.name is not None:
            devices[device.name] = device
    # Log every device we discovered
    for d in devices:
        logger.info(f"\tDiscovered: {d}")
    # Now look for our matching device(s)
    token = re.compile(r"GoPro [A-Z0-9]{4}" if identifier is None else f"GoPro {identifier}")
    matched_devices = [device for name, device in devices.items() if token.match(name)]
    logger.info(f"Found {len(matched_devices)} matching devices.")

    if len(matched_devices) > 0:

        # Connect to first matching Bluetooth device
        device = matched_devices[0]

        logger.info(f"Establishing BLE connection to {device}...")
        client = BleakClient(device)
        await client.connect(timeout=15)
        logger.info("BLE Connected!")

        # Try to pair (on some OS's this will expectedly fail)
        logger.info("Attempting to pair...")
        try:
            await client.pair()
        except NotImplementedError:
            # This is expected on Mac
            pass
        logger.info("Pairing complete!")

        # Enable notifications on all notifiable characteristics
        logger.info("Enabling notifications...")
        for service in client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    logger.info(f"Enabling notification on char {char.uuid}")
                    await client.start_notify(char, notification_handler)  # type: ignore
        logger.info("Done enabling notifications")

        return client
    else:
        logger.info("not found with for camera sn %s" % identifier)
        return None
