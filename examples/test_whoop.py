# examples/test_whoop_discovery.py
import asyncio
import logging
from src.protocols.ble.scanner import BLEScanner
from src.devices.whoop.protocol import WhoopProtocol

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    scanner = BLEScanner()
    
    # First, let's see all available devices
    logger.info("Scanning for all BLE devices...")
    all_devices = await scanner.scan_for_device(timeout=10)
    
    logger.info("Found devices:")
    for device in all_devices:
        pass
        # logger.info(
        #     f"  - {device['name'] or 'Unknown'} ({device['address']}) "
        #     f"RSSI: {device['rssi']}"
        # )
    
    # Now, let's look specifically for Whoop devices
    logger.info("\nScanning for Whoop devices...")
    whoop_devices = await scanner.scan_for_device(
        name_prefix=WhoopProtocol.DEVICE_NAME_PREFIX,
        timeout=10
    )
    
    if whoop_devices:
        logger.info("Found Whoop devices:")
        for device in whoop_devices:
            serial = WhoopProtocol.extract_serial(device['name'])
            logger.info(
                f"  - {device['name']} (Serial: {serial}) "
                f"Address: {device['address']}"
            )
    else:
        logger.warning("No Whoop devices found")

if __name__ == "__main__":
    asyncio.run(main())