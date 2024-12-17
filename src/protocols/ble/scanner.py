# src/protocols/ble/scanner.py
from bleak import BleakScanner, BLEDevice
from typing import Optional, List, Dict
import logging
from dataclasses import dataclass

@dataclass
class BLEAdvertisementData:
    """Structured BLE advertisement data"""
    local_name: Optional[str]
    service_uuids: List[str]
    manufacturer_data: Dict[int, bytes]
    service_data: Dict[str, bytes]
    tx_power: Optional[int]
    rssi: Optional[int]
    is_connectable: bool

class BLEScanner:
    """Enhanced BLE scanner with detailed advertisement data handling"""
    
    def __init__(self):
        self.scanner = BleakScanner()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _parse_advertisement_data(self, device: BLEDevice, adv_data: dict) -> BLEAdvertisementData:
        """
        Parse CoreBluetooth advertisement data into structured format
        """
        return BLEAdvertisementData(
            local_name=getattr(device, 'name', None),
            service_uuids=adv_data.get('kCBAdvDataServiceUUIDs', []),
            manufacturer_data=adv_data.get('kCBAdvDataManufacturerData', {}),
            service_data=adv_data.get('kCBAdvDataServiceData', {}),
            tx_power=adv_data.get('kCBAdvDataTxPowerLevel'),
            rssi=getattr(device, 'rssi', None),
            is_connectable=adv_data.get('kCBAdvDataIsConnectable', False)
        )
    
    def _get_device_info(self, device: BLEDevice, adv_data: dict) -> Dict:
        """
        Extract relevant information from a BLE device
        """
        parsed_data = self._parse_advertisement_data(device, adv_data)
        
        return {
            "address": device.address,
            "name": parsed_data.local_name or '',
            "rssi": parsed_data.rssi,
            "is_connectable": parsed_data.is_connectable,
            "service_uuids": parsed_data.service_uuids,
            "tx_power": parsed_data.tx_power,
            "manufacturer_data": parsed_data.manufacturer_data,
            "service_data": parsed_data.service_data
        }
    
    async def scan_for_device(
        self,
        name_prefix: Optional[str] = None,
        service_uuid: Optional[str] = None,
        timeout: int = 5
    ) -> List[Dict]:
        """
        Scan for BLE devices with enhanced filtering
        
        Args:
            name_prefix: Optional prefix to filter device names
            service_uuid: Optional service UUID to filter devices
            timeout: Scan timeout in seconds
            
        Returns:
            List of dictionaries containing device information
        """
        try:
            self.logger.info(f"Starting BLE scan (timeout: {timeout}s)")
            devices = await self.scanner.discover(
                timeout=timeout,
                return_adv=True  # Get advertisement data
            )
            
            if not devices:
                self.logger.warning("No devices found during scan")
                return []
            
            self.logger.debug(f"Found {len(devices)} total devices")
            for device, adv_data in devices.items():
                self.logger.debug(
                    f"Found device: {getattr(device, 'name', 'Unknown')} "
                    f"({device.address})"
                )
            
            filtered_devices = []
            for device, adv_data in devices.items():
                device_info = self._get_device_info(device, adv_data)
                
                # Apply name prefix filter if specified
                if name_prefix:
                    if not device_info["name"] or not device_info["name"].upper().startswith(name_prefix.upper()):
                        continue
                
                # Apply service UUID filter if specified
                if service_uuid:
                    device_uuids = device_info["service_uuids"]
                    if not device_uuids or service_uuid.lower() not in [uuid.lower() for uuid in device_uuids]:
                        continue
                
                filtered_devices.append(device_info)
                self.logger.debug(
                    f"Added filtered device: {device_info['name']} "
                    f"({device_info['address']})"
                )
            
            self.logger.info(
                f"Found {len(filtered_devices)} matching device(s)"
            )
            return filtered_devices
            
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}", exc_info=True)
            return []