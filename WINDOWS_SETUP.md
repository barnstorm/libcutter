# Libcutter Windows Setup

Successfully built libcutter for Windows!

## Build Artifacts

The following files have been built and are ready to use:

- **lib/Release/cutter.dll** - Shared library for linking with applications
- **lib/Release/cutter_static.lib** - Static library for linking with applications
- **util/Release/test_btea.exe** - Test utility for encryption functions
- **util/Release/test_endian.exe** - Test utility for endianness

## Encryption Keys Required

To use libcutter with your Cricut device, you need the encryption keys. These keys are **NOT** included with the library due to DMCA considerations.

### Keys Configuration File

1. Create a text file (e.g., `keys.txt`) with the following format:

```
MOVE_KEY_0  0xYOURKEY
MOVE_KEY_1  0xYOURKEY
MOVE_KEY_2  0xYOURKEY
MOVE_KEY_3  0xYOURKEY
LINE_KEY_0  0xYOURKEY
LINE_KEY_1  0xYOURKEY
LINE_KEY_2  0xYOURKEY
LINE_KEY_3  0xYOURKEY
CURVE_KEY_0 0xYOURKEY
CURVE_KEY_1 0xYOURKEY
CURVE_KEY_2 0xYOURKEY
CURVE_KEY_3 0xYOURKEY
```

2. Replace the `0xYOURKEY` placeholders with the actual encryption keys
3. Pass the path to this file when running libcutter utilities

A sample template has been created at: `keys_sample.txt`

## Compatible Cricut Devices

Based on the README, libcutter works with:
- Cricut Personal (v1.31, v1.34)
- Cricut Expression (v2.31, v2.34, v2.43)
- Cricut Create (v1.51, v1.54)
- Cricut Cake (v2.35)
- Cricut Cake Mini (v1.54)

**Note**: This will NOT work with Expression2, Mini, Explore, or Maker models.

## USB Driver Setup

For Windows, you need to install the FTDI USB drivers:
1. Download from: https://ftdichip.com/drivers/
2. Install the appropriate driver for your system (32-bit or 64-bit)
3. Connect your Cricut device
4. Windows should recognize it as a serial port (e.g., COM3, COM4, etc.)

## Using with SCAL (Sure Cuts A Lot)

If you're using SCAL software:
1. Copy `lib/Release/cutter.dll` to your SCAL installation directory
2. Refer to SCAL documentation for plugin integration

## Changes Made for Windows Compatibility

The following fixes were applied to make libcutter compile on Windows with MSVC:

1. Fixed CMakeLists.txt to properly switch from Unix serial_port.cpp to Windows serial_port_win32.cpp
2. Updated preprocessor macros from `__WIN32` to standard Windows detection (`_WIN32`, `_WIN64`, `WIN32`)
3. Replaced GCC-specific `__attribute__((packed))` with MSVC `#pragma pack` directives
4. Removed Unix-specific headers (sys/time.h, unistd.h) from Windows build
5. Replaced `gettimeofday()` with Windows `GetSystemTimeAsFileTime()` API

## Next Steps

1. Obtain the encryption keys for your Cricut device
2. Install FTDI USB drivers
3. Connect your Cricut and identify its COM port (Device Manager > Ports)
4. Create your keys configuration file
5. Test with the included utilities

## Support

For issues or questions about libcutter, visit:
- GitHub: https://github.com/vangdfang/libcutter
- Original documentation: http://www.built-to-spec.com/blog/
