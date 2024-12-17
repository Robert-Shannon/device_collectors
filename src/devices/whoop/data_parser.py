# src/devices/whoop/data_parser.py
import struct
from typing import Optional, List, Dict, Any
from .protocol import WhoopProtocol

class WhoopDataParser:
    """Parse raw Whoop device data"""
    
    @staticmethod
    def parse_heart_rate(data: bytes) -> Optional[int]:
        """Decode heart rate measurement"""
        try:
            return int(data[1]) if len(data) >= 2 else None
        except (IndexError, ValueError):
            return None
    
    @staticmethod
    def parse_hrv(data: bytes) -> Optional[float]:
        """Decode Heart Rate Variability"""
        try:
            return struct.unpack('<H', data[:2])[0] / 10.0 if len(data) >= 2 else None
        except Exception:
            return None
    
    @staticmethod
    def parse_accelerometer(data: bytes) -> Optional[List[float]]:
        """Decode movement/accelerometer data"""
        try:
            if len(data) >= 6:
                x = struct.unpack('<h', data[0:2])[0] / 16384.0
                y = struct.unpack('<h', data[2:4])[0] / 16384.0
                z = struct.unpack('<h', data[4:6])[0] / 16384.0
                return [x, y, z]
        except Exception:
            pass
        return None
    
    @staticmethod
    def parse_battery_level(data: bytes) -> Optional[int]:
        """Decode battery level"""
        try:
            return int(data[0])
        except (IndexError, ValueError):
            return None
    
    @classmethod
    def parse_characteristic_data(cls, characteristic_uuid: str, data: bytes) -> Dict[str, Any]:
        """Parse data based on characteristic UUID"""
        parsed_data = {
            "raw": data.hex(),
            "characteristic": characteristic_uuid
        }
        
        # Convert UUID to standard format if needed
        uuid = str(characteristic_uuid).lower()
        
        # Match against known characteristics
        if uuid == WhoopProtocol.CHARACTERISTICS["HEART_RATE"]["uuid"].lower():
            parsed_data["heart_rate"] = cls.parse_heart_rate(data)
            
        elif uuid == WhoopProtocol.CHARACTERISTICS["BATTERY_LEVEL"]["uuid"].lower():
            parsed_data["battery_level"] = cls.parse_battery_level(data)
            
        elif uuid == WhoopProtocol.CHARACTERISTICS["CUSTOM_NOTIFY_1"]["uuid"].lower():
            parsed_data["hrv"] = cls.parse_hrv(data)
            
        elif uuid == WhoopProtocol.CHARACTERISTICS["CUSTOM_NOTIFY_2"]["uuid"].lower():
            parsed_data["movement"] = cls.parse_accelerometer(data)
            
        elif uuid == WhoopProtocol.CHARACTERISTICS["CUSTOM_NOTIFY_3"]["uuid"].lower():
            parsed_data["custom_data_3"] = data.hex()
            
        elif uuid == WhoopProtocol.CHARACTERISTICS["CUSTOM_NOTIFY_4"]["uuid"].lower():
            parsed_data["custom_data_4"] = data.hex()
        
        return parsed_data