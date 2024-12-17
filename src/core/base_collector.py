from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable
import logging

class DeviceCollector(ABC):
    def __init__(self, data_callback: Optional[Callable[[str, Dict], None]] = None):
        self.is_connected = False
        self.device_info: Dict[str, Any] = {}
        self.data_callback: Optional[Callable] = None
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def discover(self) -> bool:
        pass
    
    @abstractmethod
    async def connect(self) -> bool:
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        pass
    
    @abstractmethod
    async def start_collection(self) -> bool:
        pass
    
    @abstractmethod
    async def stop_collection(self) -> bool:
        pass
