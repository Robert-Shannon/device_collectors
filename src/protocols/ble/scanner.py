from bleak import BleakScanner
from typing import Optional, List, Dict
import logging

class BLEScanner:
    def __init__(self):
        self.scanner = BleakScanner()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def scan_for_device(
        self,
        name_prefix: Optional[str] = None,
        service_uuid: Optional[str] = None,
        timeout: int = 5
    ) -> List[Dict]:
        try:
            self.logger.info(f"Starting BLE scan (timeout: {timeout}s)")
            devices = await self.scanner.discover(timeout=timeout)
            
            filtered_devices = []
            for device in devices:
                if name_prefix and not device.name.startswith(name_prefix):
                    continue
                if service_uuid and service_uuid not in device.metadata["uuids"]:
                    continue
                filtered_devices.append({
                    "address": device.address,
                    "name": device.name,
                    "rssi": device.rssi,
                    "metadata": device.metadata
                })
            
            self.logger.info(f"Found {len(filtered_devices)} matching devices")
            return filtered_devices
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            return []
