# src/devices/whoop/protocol.py
class WhoopProtocol:
    """Whoop-specific BLE protocol constants and methods"""
    
    # Device identification - now just the prefix since the rest is the serial number
    DEVICE_NAME_PREFIX = "WHOOP"
    
    # Known Whoop BLE Service and Characteristic UUIDs
    SERVICES = {
        "CUSTOM_SERVICE": "61080001-8d6d-82b8-614a-1c8cb0f8dcc6",
        "HEART_RATE_SERVICE": "0000180d-0000-1000-8000-00805f9b34fb",
        "DEVICE_INFO_SERVICE": "0000180a-0000-1000-8000-00805f9b34fb",
        "BATTERY_SERVICE": "0000180f-0000-1000-8000-00805f9b34fb"
    }
    
    CHARACTERISTICS = {
        "CUSTOM_WRITE": {
            "uuid": "61080002-8d6d-82b8-614a-1c8cb0f8dcc6",
            "properties": ["write", "write-no-response"]
        },
        "CUSTOM_NOTIFY_1": {
            "uuid": "61080003-8d6d-82b8-614a-1c8cb0f8dcc6",
            "properties": ["notify"]
        },
        "CUSTOM_NOTIFY_2": {
            "uuid": "61080004-8d6d-82b8-614a-1c8cb0f8dcc6",
            "properties": ["notify"]
        },
        "CUSTOM_NOTIFY_3": {
            "uuid": "61080005-8d6d-82b8-614a-1c8cb0f8dcc6",
            "properties": ["notify"]
        },
        "CUSTOM_NOTIFY_4": {
            "uuid": "61080007-8d6d-82b8-614a-1c8cb0f8dcc6",
            "properties": ["notify"]
        },
        "HEART_RATE": {
            "uuid": "00002a37-0000-1000-8000-00805f9b34fb",
            "properties": ["notify"]
        },
        "BATTERY_LEVEL": {
            "uuid": "00002a19-0000-1000-8000-00805f9b34fb",
            "properties": ["read", "notify"]
        }
    }
    
    @staticmethod
    def is_whoop_device(device_name: str) -> bool:
        """
        Check if a device name matches Whoop format
        
        Args:
            device_name: Name of the device to check
            
        Returns:
            bool: True if device appears to be a Whoop
        """
        if not device_name:
            return False
            
        # Check for exact format: "WHOOP" followed by space and serial number
        parts = device_name.split()
        return (len(parts) == 2 and 
                parts[0].upper() == "WHOOP" and 
                len(parts[1]) > 0)
    
    @staticmethod
    def extract_serial(device_name: str) -> str:
        """
        Extract serial number from Whoop device name
        
        Args:
            device_name: Full device name (e.g., "WHOOP 4B0018792")
            
        Returns:
            str: Serial number or empty string if not found
        """
        try:
            return device_name.split()[1]
        except (IndexError, AttributeError):
            return ""