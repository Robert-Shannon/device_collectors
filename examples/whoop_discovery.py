import asyncio
import logging
from src.devices.whoop.collector import WhoopCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    collector = WhoopCollector()
    
    def handle_data(data_type: str, data: dict):
        logger.info(f"Received {data_type}: {data}")
    
    collector.set_data_callback(handle_data)
    
    try:
        if await collector.discover():
            if await collector.connect():
                if await collector.start_collection():
                    logger.info("Collecting data for 60 seconds...")
                    await asyncio.sleep(60)
                await collector.stop_collection()
            await collector.disconnect()
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
