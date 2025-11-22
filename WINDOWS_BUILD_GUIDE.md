# Libcutter Windows Build and Installation Guide

Complete guide for building libcutter on Windows with Visual Studio/MSVC.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting the Source Code](#getting-the-source-code)
- [Windows Compatibility Fixes](#windows-compatibility-fixes)
- [Building the Library](#building-the-library)
- [Setting Up Encryption Keys](#setting-up-encryption-keys)
- [Testing the Installation](#testing-the-installation)
- [Using Libcutter](#using-libcutter)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Git for Windows**
   - Download from: https://git-scm.com/download/win
   - Used to clone the repository

2. **CMake** (version 3.8 or higher)
   - Download from: https://cmake.org/download/
   - Ensure "Add CMake to system PATH" is selected during installation
   - Verify: `cmake --version`

3. **Visual Studio 2022** (or Visual Studio 2019)
   - Download Community Edition: https://visualstudio.microsoft.com/downloads/
   - During installation, select:
     - "Desktop development with C++"
     - C++ CMake tools for Windows
   - This provides the MSVC compiler and build tools

4. **FTDI USB Drivers**
   - Download from: https://ftdichip.com/drivers/
   - Choose VCP (Virtual COM Port) drivers
   - Required for Cricut USB communication

### Optional (for advanced utilities)

- **libsvg** - For SVG drawing utilities
- **SDL2** - For simulation tools

---

## Getting the Source Code

1. **Clone the repository:**

```bash
git clone https://github.com/vangdfang/libcutter.git
cd libcutter
```

---

## Windows Compatibility Fixes

The original libcutter code was written for Unix/Linux systems. Several files need modifications to compile on Windows with MSVC.

### Fix 1: CMakeLists.txt - Serial Port Selection

**File:** `lib/CMakeLists.txt`

**Issue:** Incorrect list manipulation syntax prevents switching to Windows serial port implementation.

**Location:** Around line 31-34

**Original code:**
```cmake
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    list(REMOVE_AT cutter_files list(FIND serial_port.cpp))
    list(APPEND cutter_files serial_port_win32.cpp)
endif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
```

**Fixed code:**
```cmake
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    list(FIND cutter_files "serial_port.cpp" _index)
    if(NOT _index EQUAL -1)
        list(REMOVE_AT cutter_files ${_index})
    endif()
    list(APPEND cutter_files serial_port_win32.cpp)
endif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
```

### Fix 2: serial_port.hpp - Platform Detection

**File:** `include/serial_port.hpp`

**Issue:** Uses `__WIN32` macro which MSVC doesn't define. MSVC uses `_WIN32`, `_WIN64`, or `WIN32`.

**Location:** Lines 27 and 61

**Original code:**
```cpp
#if( !__WIN32 )
```

**Fixed code:**
```cpp
#if( !defined(_WIN32) && !defined(_WIN64) && !defined(WIN32) )
```

**Apply this fix in TWO locations** in the file (around lines 27 and 61).

### Fix 3: test_serial.hpp - Platform Detection

**File:** `util/test_serial.hpp`

**Issue:** Same `__WIN32` macro issue.

**Location:** Line 29

**Original code:**
```cpp
#if( __WIN32 )
#define sleep(x) Sleep(x*1000)
#endif
```

**Fixed code:**
```cpp
#if( defined(_WIN32) || defined(_WIN64) || defined(WIN32) )
#define sleep(x) Sleep(x*1000)
#endif
```

### Fix 4: device_c.cpp - Struct Packing

**File:** `lib/device_c.cpp`

**Issue:** GCC's `__attribute__((packed))` is not supported by MSVC.

**Location:** Around line 32

**Original code:**
```cpp
struct __attribute__(( packed )) lmc_command
{
    uint8_t  bytes;
    uint8_t  cmd;
    uint32_t data[3];
};
```

**Fixed code:**
```cpp
#if defined(_MSC_VER)
#pragma pack(push, 1)
#endif

struct
#if defined(__GNUC__) || defined(__clang__)
__attribute__(( packed ))
#endif
lmc_command
{
    uint8_t  bytes;
    uint8_t  cmd;
    uint32_t data[3];
};

#if defined(_MSC_VER)
#pragma pack(pop)
#endif
```

### Fix 5: serial_port_win32.cpp - Remove Unix Headers

**File:** `lib/serial_port_win32.cpp`

**Issue:** Includes Unix headers that don't exist on Windows.

**Location:** Lines 22-31

**Original code:**
```cpp
#include "serial_port.hpp"
#include <cstdio>
#include <sys/types.h>
#include <cstdlib>
#include <sys/time.h>
#include <unistd.h>
#include <cmath>
#include <string>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
```

**Fixed code:**
```cpp
#include "serial_port.hpp"
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <string>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
```

### Fix 6: serial_port_win32.cpp - Replace gettimeofday()

**File:** `lib/serial_port_win32.cpp`

**Issue:** Uses Unix `gettimeofday()` function which doesn't exist on Windows.

**Location:** Around line 155-160

**Original code:**
```cpp
uint64_t serial_port::getTime( void )
{
    timeval tv;
    gettimeofday( &tv, NULL );
    return (uint64_t)tv.tv_sec * 1000000 + (uint64_t)tv.tv_usec ;
}
```

**Fixed code:**
```cpp
uint64_t serial_port::getTime( void )
{
    FILETIME ft;
    ULARGE_INTEGER uli;

    GetSystemTimeAsFileTime(&ft);
    uli.LowPart = ft.dwLowDateTime;
    uli.HighPart = ft.dwHighDateTime;

    // Convert from 100-nanosecond intervals to microseconds
    return uli.QuadPart / 10;
}
```

### Fix 7: test_serial.cpp - Conditional Unix Headers

**File:** `util/test_serial.cpp`

**Issue:** Includes `unistd.h` unconditionally.

**Location:** Around line 31

**Original code:**
```cpp
#include <unistd.h>
```

**Fixed code:**
```cpp
#if !defined(_WIN32) && !defined(_WIN64) && !defined(WIN32)
#include <unistd.h>
#endif
```

---

## Building the Library

### Step 1: Configure with CMake

Open a Command Prompt or PowerShell in the libcutter directory:

```bash
mkdir build
cd build
cmake ..
```

**Expected output:**
```
-- Building for: Visual Studio 17 2022
-- The C compiler identification is MSVC 19.44.xxxxx
-- The CXX compiler identification is MSVC 19.44.xxxxx
...
-- Configuring done
-- Generating done
-- Build files have been written to: C:/path/to/libcutter/build
```

### Step 2: Build the Project

```bash
cmake --build . --config Release
```

**Expected output:**
```
Building Custom Rule...
  device.cpp
  device_c.cpp
  serial_port_win32.cpp
  btea.c
  cutter.vcxproj -> C:/path/to/libcutter/build/lib/Release/cutter.dll
  ...
  test_btea.vcxproj -> C:/path/to/libcutter/build/util/Release/test_btea.exe
  test_endian.vcxproj -> C:/path/to/libcutter/build/util/Release/test_endian.exe
  test_serial.vcxproj -> C:/path/to/libcutter/build/util/Release/test_serial.exe
```

### Step 3: Verify Build Artifacts

Check that the following files were created:

```bash
dir /s /b *.dll *.lib *.exe
```

**Expected files:**
- `build/lib/Release/cutter.dll` - Shared library
- `build/lib/Release/cutter_static.lib` - Static library
- `build/util/Release/test_btea.exe` - Encryption test
- `build/util/Release/test_endian.exe` - Endianness test
- `build/util/Release/test_serial.exe` - Serial communication test

---

## Setting Up Encryption Keys

### Understanding Encryption Keys

Libcutter requires encryption keys to communicate with Cricut devices. These keys are **NOT** included in the repository due to DMCA considerations.

### Key Configuration File Format

Create a file named `keys.txt` in the libcutter directory with this format:

```
MOVE_KEY_0  0xYOURKEYHERE
MOVE_KEY_1  0xYOURKEYHERE
MOVE_KEY_2  0xYOURKEYHERE
MOVE_KEY_3  0xYOURKEYHERE
LINE_KEY_0  0xYOURKEYHERE
LINE_KEY_1  0xYOURKEYHERE
LINE_KEY_2  0xYOURKEYHERE
LINE_KEY_3  0xYOURKEYHERE
CURVE_KEY_0 0xYOURKEYHERE
CURVE_KEY_1 0xYOURKEYHERE
CURVE_KEY_2 0xYOURKEYHERE
CURVE_KEY_3 0xYOURKEYHERE
```

### Key Mapping

The keys correspond to specific command types:
- **MOVE_KEY** (KEY2) - Controls blade movement without cutting
- **LINE_KEY** (KEY4) - Controls straight line cuts
- **CURVE_KEY** (KEY6) - Controls curved cuts

**Note:** KEY3 and KEY5 also work for LINE and CURVE but lift the blade after each cut, creating gaps.

---

## Testing the Installation

### Test 1: System Endianness

```bash
cd build\util\Release
test_endian.exe
```

**Expected output:**
```
This appears to be a little-endian machine
No errors detected
```

### Test 2: Encryption (BTEA)

```bash
test_btea.exe
```

**Expected output:**
```
using 'TestPhrase!' as cleartext
...
Huzzah! You passed the default btea test
...
Hurray, you passed the btea encryption identity test
```

### Test 3: Serial Communication

First, identify your Cricut's COM port:

1. Connect your Cricut via USB
2. Open **Device Manager** (Win+X → Device Manager)
3. Expand **Ports (COM & LPT)**
4. Look for "USB Serial Port (COMx)" or similar
5. Note the COM port number (e.g., COM6)

Then test the connection:

```bash
test_serial.exe COM6
```

*Replace COM6 with your actual COM port.*

**Expected output:**
```
timing = 0.000750
Port open
port closed
```

**If successful, your Cricut should:**
- Make noise (motors activating)
- Attempt to cut a small test rectangle (if paper/material is loaded)

---

## Using Libcutter

### From Command Line Utilities

#### Test Serial Communication

```bash
cd build\util\Release
test_serial.exe COMx
```

Replace `x` with your COM port number.

#### For G-code Files (if draw_gcode is built)

```bash
draw_gcode.exe COMx path\to\file.gcode path\to\keys.txt
```

#### For SVG Files (if draw_svg is built)

Requires libsvg to be installed and linked.

```bash
draw_svg.exe path\to\file.svg COMx path\to\keys.txt
```

### From Your Own Application

#### Include Headers

```cpp
#include "device_c.hpp"
#include "serial_port.hpp"
```

#### Link the Library

**Option 1: Dynamic Linking (DLL)**

1. Link against `cutter.lib` (import library)
2. Ensure `cutter.dll` is in your application's directory or system PATH

**Option 2: Static Linking**

Link against `cutter_static.lib`

#### Example Code

```cpp
#include "serial_port.hpp"

int main() {
    serial_port sp;
    sp.p_open("COM6", 200000);

    if (sp.is_open()) {
        // Send commands to Cricut
        const uint8_t start[] = {0x04, 0x21, 0x00, 0x00, 0x00};
        sp.p_write(start, sizeof(start));

        sp.p_close();
    }

    return 0;
}
```

---

## Troubleshooting

### Build Issues

#### CMake can't find compiler

**Error:**
```
CMake Error: your CXX compiler: "CMAKE_CXX_COMPILER-NOTFOUND" was not found
```

**Solution:**
- Install Visual Studio with "Desktop development with C++"
- Run cmake from "Developer Command Prompt for VS 2022"
- Or use: `cmake -G "Visual Studio 17 2022" ..`

#### "Cannot open include file: 'termios.h'"

**Solution:**
Apply [Fix 2](#fix-2-serial_porthpp---platform-detection) and [Fix 5](#fix-5-serial_port_win32cpp---remove-unix-headers) from the compatibility fixes section.

#### "__attribute__ is not defined"

**Solution:**
Apply [Fix 4](#fix-4-device_ccpp---struct-packing) from the compatibility fixes section.

### Runtime Issues

#### "Port not open" when running test_serial

**Possible causes:**

1. **Wrong COM port**
   - Verify in Device Manager
   - Try `\\.\COMx` format for ports > COM9

2. **Cricut not connected or powered on**
   - Ensure USB cable is connected
   - Power on the Cricut device

3. **Driver issues**
   - Install FTDI VCP drivers
   - Restart computer after driver installation

4. **Permission issues**
   - Close any other applications using the COM port
   - Try running as Administrator

#### Cricut doesn't respond to commands

**Possible causes:**

1. **Incorrect encryption keys**
   - Verify keys.txt has correct values
   - Ensure keys are in hexadecimal format (0x prefix)

2. **Incompatible Cricut model**
   - Libcutter works with: Personal, Expression, Create, Cake, Cake Mini
   - Does NOT work with: Expression 2, Mini, Explore, Maker

3. **Cricut in wrong mode**
   - Some models need to be in specific modes
   - Try power cycling the device

### Advanced Utilities Not Building

#### draw_svg or draw_gcode not found

**Issue:** These utilities require additional dependencies.

**Solution:**

For **draw_svg**:
1. Download and compile libsvg
2. Install libpng
3. Reconfigure CMake: `cmake -DLIBSVG_FOUND=TRUE ..`

For **draw_gcode**:
1. Should build by default
2. If missing, check CMake output for errors

---

## Compatible Cricut Devices

| Cutter            | Version | Status      |
|-------------------|---------|-------------|
| Cricut Cake       | v2.35   | Should work |
| Cricut Cake Mini  | v1.54   | Should work |
| Cricut Create     | v1.51   | Should work |
| Cricut Create     | v1.54   | Should work |
| Cricut Expression | v2.00   | Too old     |
| Cricut Expression | v2.31   | **Works**   |
| Cricut Expression | v2.34   | Should work |
| Cricut Expression | v2.43   | Should work |
| Cricut Personal   | v1.00   | Too old     |
| Cricut Personal   | v1.31   | **Works**   |
| Cricut Personal   | v1.34   | **Works**   |

**Not Compatible:** Expression 2, Mini, Explore, Maker

---

## Additional Resources

- **Official Repository:** https://github.com/vangdfang/libcutter
- **Original Documentation:** http://www.built-to-spec.com/blog/
- **FTDI Drivers:** https://ftdichip.com/drivers/

---

## Summary of Changes for Windows

This build includes the following modifications to the original libcutter code:

1. ✅ Fixed CMakeLists.txt list manipulation for Windows serial port selection
2. ✅ Updated platform detection macros from `__WIN32` to standard Windows macros
3. ✅ Replaced GCC `__attribute__((packed))` with MSVC `#pragma pack`
4. ✅ Removed Unix-specific headers (sys/time.h, unistd.h, sys/types.h)
5. ✅ Implemented Windows-native `getTime()` using GetSystemTimeAsFileTime()
6. ✅ Conditional inclusion of Unix headers in test utilities
7. ✅ Verified serial communication on Windows COM ports

All changes maintain backward compatibility with Unix/Linux builds.

---

## License

Libcutter is licensed under the GNU Lesser General Public License (LGPL) v2.1.

The utilities are licensed under the GNU General Public License (GPL) v2.

---

**Last Updated:** 2025-11-15
**Tested On:** Windows 11, Visual Studio 2022, CMake 3.29
