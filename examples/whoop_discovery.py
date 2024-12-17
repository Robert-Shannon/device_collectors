# src/devices/whoop/whoop_discovery.py
import asyncio
import logging
from datetime import datetime
from src.devices.whoop.collector import WhoopCollector

# Known Whoop device address
WHOOP_ADDRESS = "A227FD08-E57B-7F61-90F7-5842B94F7AE9"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataLogger:
    """Helper class to log and store received data"""
    
    def __init__(self):
        self.data_points = []
        self.start_time = None
    
    def handle_data(self, data_type: str, data: dict):
        """Process and log received data"""
        if not self.start_time:
            self.start_time = datetime.now()
        
        timestamp = datetime.now()
        elapsed = (timestamp - self.start_time).total_seconds()
        
        data["timestamp"] = timestamp.isoformat()
        data["elapsed_seconds"] = elapsed
        self.data_points.append(data)
        
        if "heart_rate" in data:
            logger.info(f"Heart Rate: {data['heart_rate']} BPM")
        elif "hrv" in data:
            logger.info(f"HRV: {data['hrv']} ms")
        elif "movement" in data:
            logger.info(f"Movement: {data['movement']}")
        elif "battery_level" in data:
            logger.info(f"Battery Level: {data['battery_level']}%")
        else:
            logger.debug(f"Other data received: {data}")
    
    def save_to_file(self, filename: str = "whoop_data.txt"):
        """Save collected data to a file"""
        with open(filename, "w") as f:
            f.write(f"Whoop Data Collection - {datetime.now()}\n")
            f.write("-" * 50 + "\n")
            for data_point in self.data_points:
                f.write(f"{data_point}\n")

async def run_data_collection(collector: WhoopCollector, duration: int = 60):
    """Run data collection for specified duration"""
    try:
        logger.info(f"Starting data collection for {duration} seconds...")
        await collector.start_collection()
        await asyncio.sleep(duration)
        await collector.stop_collection()
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        raise

async def main():
    # Create data logger
    data_logger = DataLogger()
    
    # Initialize collector with data handler
    collector = WhoopCollector(data_callback=data_logger.handle_data)
    
    try:
        # Connect directly to the known Whoop device
        logger.info(f"Connecting to Whoop device: {WHOOP_ADDRESS}")
        if await collector.connect_to_address(WHOOP_ADDRESS):
            logger.info("Device connected successfully")
            logger.info(f"Device Info: {collector.device_info}")
            
            # Data collection phase
            await run_data_collection(collector, duration=60)
            
            # Save collected data
            data_logger.save_to_file()
        else:
            logger.error("Failed to connect to Whoop device")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    
    finally:
        # Ensure cleanup happens
        if collector.is_connected:
            await collector.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Process failed: {e}", exc_info=True)
    finally:
        logger.info("Process completed")