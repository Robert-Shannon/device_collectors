# Device Collectors

A framework for collecting data from various fitness devices.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

See examples directory for usage examples.



scan: starting scan for 10s
/Users/robertshannon/projects/device_collectors/examples/test_ble.py:26: FutureWarning: BLEDevice.rssi is deprecated and will be removed in a future version of Bleak, use AdvertisementData.rssi instead
  print(f"scan: Device {device.address} [{device_name}], RSSI={device.rssi} dB")
scan: Device C0BC4F3D-C902-36D1-195A-9D6A21530B4A [None], RSSI=-69 dB
scan: Device 140C579F-9FA9-3079-18EB-2D24609DA246 [Bathroom], RSSI=-71 dB
scan: Device B2E048B4-EDAA-6145-8264-BDF8040273EB [Living Room], RSSI=-54 dB
scan: Device 95E5C473-D2CD-CF61-A3F8-A272E90F8B5F [None], RSSI=-65 dB
scan: Device 90A528B5-1EDF-B427-2F79-A8EB308C6C45 [None], RSSI=-80 dB
scan: Device A227FD08-E57B-7F61-90F7-5842B94F7AE9 [WHOOP 4B0018792], RSSI=-44 dB
scan: Device D6EA7939-874F-5C67-3227-841CEEDAFAC1 [Govee_H61C2_2887], RSSI=-78 dB
scan: Device C44B1506-5731-EDB3-5FC9-90D698DE5C9A [None], RSSI=-83 dB
scan: Device 5B49BC5B-B005-3E7A-9E1C-8A7A9C93572F [Balcony], RSSI=-64 dB
scan: Device 2CF35C2F-BDED-9425-CAE6-E8705C4E1134 [[TV] dirty mike], RSSI=-54 dB
scan: Device 6773D652-4D45-949F-E7C1-AF918B844258 [LE_WH-1000XM5], RSSI=-42 dB
scan: Device C215CDAD-970C-5075-D457-89622DEAF170 [CarBack], RSSI=-69 dB
scan: Device DEE11CD8-D9EA-F98C-F8A6-1E79051A4DCB [L50039G], RSSI=-77 dB
scan: Device C8753B2C-D8E5-AB58-E3E3-1894FA5242AA [[TV] Vinny], RSSI=-78 dB
scan: Device C3D405D4-4A63-2CD1-4BCC-9F5D643332C3 [None], RSSI=-44 dB
scan: Device 87ED42A9-09B8-04DB-FE98-9DAD0C752CB5 [None], RSSI=-67 dB
scan: Device 753DC914-133C-5673-C46E-D245BA42716D [iPad], RSSI=-43 dB
scan: Device 44D9CCA8-744F-40AB-B3E7-35CE54743E0A [None], RSSI=-81 dB
scan: Device 1ACD9EC6-0FEE-095D-A15E-E0586DE2218A [Robert], RSSI=-42 dB
scan: Device 2980867B-D1C6-D6A7-2076-962D48DAE61D [None], RSSI=-53 dB
scan: Device 8AF347A0-5CDF-A64F-9373-3929F2CA1A78 [None], RSSI=-70 dB
scan: Device AA405A76-E755-D549-E104-2A8296F20BDE [None], RSSI=-64 dB
scan: Device 8E3E6328-4967-C43C-7933-3B062AA23B0B [None], RSSI=-72 dB
scan: Device 33A6EBB9-DD97-5757-8C30-4DBE386A4654 [None], RSSI=-82 dB
scan: Device 8EE72A7B-1614-F70D-C613-DB5144EB0775 [None], RSSI=-82 dB
scan: Device 2E88C27F-21D8-A918-6673-98A5F1BC97B8 [None], RSSI=-80 dB
scan: Device 0FB49E01-419A-1E8C-3C18-23007AA697BB [[TV] Samsung TU700D 43 TV], RSSI=-84 dB
scan: Device C12E812C-F536-D599-E0E0-E586F04EDB6C [None], RSSI=-51 dB
scan: Device 5840FBEF-9347-BC52-7133-95E5A5066FBD [None], RSSI=-79 dB
scan: Device 68E5ED9F-6524-0CCE-7747-D8BBF28469E6 [None], RSSI=-80 dB
scan: Device 188CBEE2-DA5A-4EF8-311B-B2750E1E961E [NB779], RSSI=-55 dB
scan: Device C683A9AC-1078-4A52-A959-3DA85AA9F086 [None], RSSI=-74 dB
scan: Device 1173BFCE-BD10-DA08-645F-4E5459DBE10E [Robert’s Trek Bike], RSSI=-72 dB
scan: Device 4A41FD35-6DDB-2122-6EB9-6F352248C6AF [None], RSSI=-85 dB
scan: Device 54A063DB-1094-8857-0323-AF8CE8CDE47B [None], RSSI=-85 dB
scan: Device 56936786-6EBA-FC57-5D02-35E0ED9CEAA2 [None], RSSI=-77 dB
scan: Device 5D99E984-8449-4E2E-79D9-1CD609B9D910 [Robert’s Keys], RSSI=-70 dB
scan: Complete, found 37 devices
> ls A227FD08-E57B-7F61-90F7-5842B94F7AE9
Listing services...
   -- SERVICE: 61080001-8d6d-82b8-614a-1c8cb0f8dcc6 [Unknown]
   --   --> CHAR: 61080002-8d6d-82b8-614a-1c8cb0f8dcc6, Handle: 15 (0x000f) - WRITE WRITE NO RESPONSE - [Unknown]
   --   --> CHAR: 61080003-8d6d-82b8-614a-1c8cb0f8dcc6, Handle: 17 (0x0011) - NOTIFY - [Unknown]
   --   --> CHAR: 61080004-8d6d-82b8-614a-1c8cb0f8dcc6, Handle: 20 (0x0014) - NOTIFY - [Unknown]
   --   --> CHAR: 61080005-8d6d-82b8-614a-1c8cb0f8dcc6, Handle: 23 (0x0017) - NOTIFY - [Unknown]
   --   --> CHAR: 61080007-8d6d-82b8-614a-1c8cb0f8dcc6, Handle: 26 (0x001a) - NOTIFY - [Unknown]
   -- SERVICE: 0000180d-0000-1000-8000-00805f9b34fb [Heart Rate]
   --   --> CHAR: 00002a37-0000-1000-8000-00805f9b34fb, Handle: 36 (0x0024) - NOTIFY - [Heart Rate Measurement]
   -- SERVICE: 0000180a-0000-1000-8000-00805f9b34fb [Device Information]
   --   --> CHAR: 00002a29-0000-1000-8000-00805f9b34fb, Handle: 40 (0x0028) - READ - [Manufacturer Name String]
   -- SERVICE: 0000180f-0000-1000-8000-00805f9b34fb [Battery Service]
   --   --> CHAR: 00002a19-0000-1000-8000-00805f9b34fb, Handle: 43 (0x002b) - READ NOTIFY - [Battery Level]

Listing descriptors...
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 19 (0x0013)
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 22 (0x0016)
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 25 (0x0019)
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 28 (0x001c)
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 38 (0x0026)
   --  DESCRIPTORS: 00002902-0000-1000-8000-00805f9b34fb, [Client Characteristic Configuration], Handle: 45 (0x002d)

Reading characteristics...
  -- READ: 00002a29-0000-1000-8000-00805f9b34fb [Manufacturer Name String] (0x0028), Value: bytearray(b'WHOOP Inc.')
  -- READ: 00002a19-0000-1000-8000-00805f9b34fb [Battery Level] (0x002b), Value: bytearray(b'3')
