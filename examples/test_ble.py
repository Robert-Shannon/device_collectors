#!/usr/bin/env python3

import asyncio
import datetime
from bleak import BleakScanner, BleakClient
from typing import List, Dict

class BLELS:
    def __init__(self):
        self.public_devices = []

    async def scan(self, duration: int = 10):
        """Scan for BLE devices for the specified duration."""
        try:
            print(f"scan: starting scan for {duration}s")
            devices = await BleakScanner.discover(timeout=duration)
            found_devices = 0
            self.public_devices = []

            for device in devices:
                # Bleak handles device names differently
                device_name = device.name or "None"
                
                # Note: Bleak doesn't distinguish between public/random addresses
                # but we'll keep track of all devices for consistency
                print(f"scan: Device {device.address} [{device_name}], RSSI={device.rssi} dB")
                found_devices += 1
                self.public_devices.append(device)

            print(f"scan: Complete, found {len(devices)} devices")

        except Exception as e:
            print("scan: Error,", e)

    async def connect_and_read(self, address: str):
        """Connect to a device and read its characteristics."""
        try:
            async with BleakClient(address) as client:
                print("Listing services...")
                for service in client.services:
                    print(f"   -- SERVICE: {service.uuid} [{service.description or service.uuid}]")
                    
                    for char in service.characteristics:
                        properties = []
                        if "read" in char.properties:
                            properties.append("READ")
                        if "write" in char.properties:
                            properties.append("WRITE")
                        if "write-without-response" in char.properties:
                            properties.append("WRITE NO RESPONSE")
                        if "notify" in char.properties:
                            properties.append("NOTIFY")
                        
                        props_str = " ".join(properties)
                        print(f"   --   --> CHAR: {char.uuid}, Handle: {char.handle} "
                              f"(0x{char.handle:04x}) - {props_str} - [{char.description or char.uuid}]")

                print("\nListing descriptors...")
                for service in client.services:
                    for char in service.characteristics:
                        for desc in char.descriptors:
                            print(f"   --  DESCRIPTORS: {desc.uuid}, "
                                  f"[{desc.description or desc.uuid}], "
                                  f"Handle: {desc.handle} (0x{desc.handle:04x})")

                print("\nReading characteristics...")
                for service in client.services:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                print(f"  -- READ: {char.uuid} [{char.description or char.uuid}] "
                                      f"(0x{char.handle:04x}), Value: {value}")
                            except Exception as e:
                                print(f"  -- READ: {char.uuid} [{char.description or char.uuid}] "
                                      f"(0x{char.handle:04x}), Error reading: {str(e)}")

        except Exception as e:
            print("connect_and_read: Error,", e)

async def main():
    print("BLE LS Script ---")
    print("--------------------")
    print("scan [duration]     : Scan")
    print("ls <ADDRESS>        : Read attributes for device")
    print("q                   : Quit")
    
    ble = BLELS()
    
    while True:
        choice = input("> ").lower()
        
        if choice.startswith('q'):
            print("exiting...")
            break
            
        elif choice.startswith('scan'):
            duration = 10
            if len(choice) > 4:
                args = choice.split(' ', 2)
                if len(args) == 2 and 0 < int(args[1]) < 60:
                    duration = int(args[1])
            await ble.scan(duration)
            
        elif choice.startswith('ls'):
            addr = ''
            if len(choice) > 2:
                args = choice.split(' ', 2)
                if len(args) == 2:
                    addr = args[1]
            if not addr:
                print("Please provide a device address")
                continue
            await ble.connect_and_read(addr)
            
        elif choice.startswith('t'):
            print(f"time is {datetime.date.today().isoformat()}")
            
        else:
            print("Unknown option:", choice)
    
    print("--------------------")
    print("Goodbye!")

if __name__ == '__main__':
    asyncio.run(main())