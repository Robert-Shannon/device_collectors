# src/devices/whoop/collector.py
from ...core.base_collector import DeviceCollector
from ...protocols.ble.scanner import BLEScanner
from .protocol import WhoopProtocol
from .data_parser import WhoopDataParser
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from typing import Optional, Dict, Any, Callable, Union
import asyncio
import logging

class WhoopCollector(DeviceCollector):
    """Collector for Whoop devices"""
    
    def __init__(self, device_address: Optional[str] = None, data_callback: Optional[Callable[[str, Dict], None]] = None):
        super().__init__()
        self.scanner = BLEScanner()
        self.client: Optional[BleakClient] = None
        self.device_address = device_address
        self.data_callback = data_callback
        self.device_info: Dict[str, Any] = {}
        self.logger.setLevel(logging.DEBUG)
    
    async def discover(self) -> bool:
        """
        Discover Whoop devices - implemented to satisfy abstract method
        In direct connection mode, this is not typically used
        """
        if self.device_address:
            self.logger.debug(f"Using known device address: {self.device_address}")
            return True
            
        self.logger.debug(f"Starting discovery with name prefix: {WhoopProtocol.DEVICE_NAME_PREFIX}")
        
        try:
            devices = await self.scanner.scan_for_device(
                name_prefix=WhoopProtocol.DEVICE_NAME_PREFIX,
                timeout=5
            )
            
            if devices:
                self.device_address = devices[0]["address"]
                self.logger.info(f"Found device: {self.device_address}")
                return True
                
            self.logger.warning("No Whoop devices found")
            return False
            
        except Exception as e:
            self.logger.error(f"Discovery failed: {str(e)}")
            return False
    
    async def connect(self) -> bool:
        """
        Connect to the Whoop device - implemented to satisfy abstract method
        """
        if not self.device_address:
            self.logger.error("No device address available")
            return False
            
        return await self.connect_to_address(self.device_address)
    
    async def connect_to_address(self, address: str) -> bool:
        """Connect directly to a device by address"""
        try:
            self.logger.debug(f"Connecting directly to device: {address}")
            self.client = BleakClient(address)
            await self.client.connect()
            
            # Store basic device info
            self.device_info = {
                "address": address,
            }
            
            # Read additional device info if available
            try:
                services = await self.client.get_services()
                for service in services.services.values():
                    if service.uuid == WhoopProtocol.SERVICES["DEVICE_INFO_SERVICE"]:
                        for char in service.characteristics:
                            if WhoopProtocol.CHARACTERISTICS["MANUFACTURER_NAME"]["uuid"] in str(char.uuid):
                                manufacturer = await self.client.read_gatt_char(char.uuid)
                                self.device_info["manufacturer"] = manufacturer.decode()
            except Exception as e:
                self.logger.debug(f"Couldn't read manufacturer name: {e}")
            
            try:
                battery_char = WhoopProtocol.CHARACTERISTICS["BATTERY_LEVEL"]["uuid"]
                battery = await self.client.read_gatt_char(battery_char)
                self.device_info["battery_level"] = int(battery[0])
            except Exception as e:
                self.logger.debug(f"Couldn't read battery level: {e}")
            
            self.is_connected = True
            self.logger.info(f"Connected to device: {address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False
    
    def _handle_data(self, characteristic: Union[BleakGATTCharacteristic, str], data: bytearray):
        """
        Handle incoming data from device
        
        Args:
            characteristic: Either a BleakGATTCharacteristic object or UUID string
            data: Raw data received from the device
        """
        if self.data_callback:
            try:
                # Extract the UUID from the characteristic object or use the string directly
                if isinstance(characteristic, BleakGATTCharacteristic):
                    char_uuid = str(characteristic.uuid)
                else:
                    char_uuid = str(characteristic)
                
                parsed_data = WhoopDataParser.parse_characteristic_data(char_uuid, data)
                self.data_callback("whoop_data", parsed_data)
                
                # Log the first few bytes of data for debugging
                self.logger.debug(f"Received data from {char_uuid}: {data[:8].hex()}")
                
            except Exception as e:
                self.logger.error(f"Data handling error for {characteristic}: {str(e)}")
    
    async def start_collection(self) -> bool:
        """Start collecting data from the device"""
        if not self.client or not self.is_connected:
            self.logger.error("Device not connected")
            return False
        
        try:
            # Enable notifications for all notifiable characteristics
            services = await self.client.get_services()
            
            for service in services.services.values():
                self.logger.debug(f"Checking service: {service.uuid}")
                for char in service.characteristics:
                    if "notify" in char.properties:
                        try:
                            self.logger.debug(f"Enabling notifications for: {char.uuid}")
                            await self.client.start_notify(char, self._handle_data)
                            self.logger.info(f"Enabled notifications for {char.uuid}")
                        except Exception as e:
                            self.logger.warning(f"Failed to enable notifications for {char.uuid}: {e}")
            
            self.logger.info("Started data collection")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start collection: {str(e)}")
            return False
    
    async def stop_collection(self) -> bool:
        """Stop collecting data"""
        if not self.client or not self.is_connected:
            return False
            
        try:
            services = await self.client.get_services()
            for service in services.services.values():
                for char in service.characteristics:
                    if "notify" in char.properties:
                        try:
                            await self.client.stop_notify(char)
                        except Exception as e:
                            self.logger.warning(f"Failed to disable notifications for {char.uuid}: {e}")
            
            self.logger.info("Stopped data collection")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop collection: {str(e)}")
            return False
    async def disconnect(self) -> bool:
        """Disconnect from the device"""
        if self.client and self.is_connected:
            try:
                await self.client.disconnect()
                self.is_connected = False
                self.logger.info("Disconnected from device")
                return True
            except Exception as e:
                self.logger.error(f"Disconnect failed: {str(e)}")
        return False