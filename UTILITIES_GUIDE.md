# Libcutter Utilities Guide

Complete guide to all built libcutter utilities for Windows.

## Built Utilities

All utilities are located in: `build/util/Release/`

### ✅ Successfully Built (7 utilities)

1. **draw_gcode.exe** - Draw G-code files with your Cricut
2. **enumerate.exe** - Enumerate and identify connected Cricut devices
3. **interpreter.exe** - Execute custom command scripts
4. **test_btea.exe** - Test BTEA encryption/decryption
5. **test_endian.exe** - Test system byte order
6. **test_serial.exe** - Test serial communication
7. **test_speed.exe** - Benchmark cutting speed

### ⚠️ Not Built (requires additional libraries)

- **draw_svg.exe** - Requires libsvg, libjpeg, libpng (see [Installing SVG Support](#installing-svg-support))

---

## Utility Usage

### draw_gcode.exe

Draw G-code files on your Cricut.

**Syntax:**
```bash
draw_gcode.exe <device> <gcode_file> [-d debug_level]
```

**Parameters:**
- `<device>` - COM port (e.g., COM6)
- `<gcode_file>` - Path to G-code file
- `-d debug_level` - Optional: 0-5 (default: 1)
  - 0 = Critical only
  - 1 = Errors only (default)
  - 2 = Warnings
  - 3 = Info
  - 4 = Debug
  - 5 = Verbose

**Example:**
```bash
cd build\util\Release
draw_gcode.exe COM6 C:\path\to\design.gcode -d 2
```

**G-code Notes:**
- Coordinate system: Based on Cricut's internal units (404 units = 1 inch)
- Supports standard G-code commands (G0, G1, G2, G3, etc.)
- Tool on/off controlled by M3/M5 commands

---

### enumerate.exe

Enumerate and identify connected Cricut devices.

**Syntax:**
```bash
enumerate.exe <device>
```

**Parameters:**
- `<device>` - COM port to query (e.g., COM6)

**Example:**
```bash
enumerate.exe COM6
```

**Output:**
- Device model (Expression, Personal, Create, etc.)
- Firmware version
- Device capabilities

---

### interpreter.exe

Execute custom command scripts for Cricut control.

**Syntax:**
```bash
interpreter.exe <device> <script_file>
```

**Parameters:**
- `<device>` - COM port (e.g., COM6)
- `<script_file>` - Path to command script file

**Example:**
```bash
interpreter.exe COM6 commands.txt
```

**Script Format:**

Commands are single-letter codes followed by parameters:

```
M x y              # Move to position (x, y)
L x y              # Line to position (x, y)
C x1 y1 x2 y2 x3 y3 x4 y4  # Bezier curve with 4 control points
S seconds          # Sleep/delay for N seconds
```

**Example Script:**
```
M 0 0
L 1000 0
L 1000 1000
L 0 1000
L 0 0
```

---

### test_serial.exe

Test basic serial communication with your Cricut.

**Syntax:**
```bash
test_serial.exe <device>
```

**Parameters:**
- `<device>` - COM port (e.g., COM6)

**Example:**
```bash
test_serial.exe COM6
```

**What it does:**
- Opens the serial port
- Sends a test rectangle cutting sequence
- Reports success/failure
- Useful for verifying connectivity

**Expected output:**
```
timing = 0.000750
Port open
port closed
```

---

### test_speed.exe

Benchmark cutting speed and performance.

**Syntax:**
```bash
test_speed.exe <device> <config_file>
```

**Parameters:**
- `<device>` - COM port (e.g., COM6)
- `<config_file>` - Configuration file with test parameters

**Example:**
```bash
test_speed.exe COM6 speed_config.txt
```

**Config File Format:**
```
device=COM6
speed=5
pressure=3
```

---

### test_btea.exe

Test BTEA (Block TEA) encryption algorithm.

**Syntax:**
```bash
test_btea.exe [test_string]
```

**Parameters:**
- `[test_string]` - Optional test phrase (default: "TestPhrase!")

**Example:**
```bash
test_btea.exe
test_btea.exe "MyCustomTest"
```

**What it does:**
- Encrypts the test string
- Decrypts it back
- Verifies correctness
- Reports pass/fail

**Expected output:**
```
Huzzah! You passed the default btea test
Hurray, you passed the btea encryption identity test
```

---

### test_endian.exe

Test system byte order (endianness).

**Syntax:**
```bash
test_endian.exe
```

**No parameters required.**

**Example:**
```bash
test_endian.exe
```

**Expected output:**
```
This appears to be a little-endian machine
No errors detected
```

---

## Creating G-code Files

### Manual G-code

Create a text file with G-code commands:

**simple_square.gcode:**
```gcode
G21         ; Set units to mm
G90         ; Absolute positioning
M3          ; Pen down (start cutting)
G1 X0 Y0    ; Move to origin
G1 X1000 Y0 ; Line to (1000, 0)
G1 X1000 Y1000
G1 X0 Y1000
G1 X0 Y0
M5          ; Pen up (stop cutting)
M2          ; End program
```

### From CAD Software

Many CAD programs can export G-code:
- **Inkscape** - With G-code extension
- **Fusion 360** - CAM workspace
- **FreeCAD** - Path workbench

### Coordinate System

- Units: Cricut internal units (404 units = 1 inch)
- Origin: Typically bottom-left of cutting mat
- X-axis: Left to right
- Y-axis: Bottom to top
- Max dimensions depend on your Cricut model:
  - Personal: ~6" x 12"
  - Expression: ~12" x 12" or 12" x 24"

### Converting Inches to Units

```
Cricut Units = Inches × 404
```

**Examples:**
- 1 inch = 404 units
- 6 inches = 2424 units
- 12 inches = 4848 units

---

## Installing SVG Support

To build `draw_svg.exe`, you need to install these libraries:

### Option 1: vcpkg (Recommended)

1. **Install vcpkg:**
```bash
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```

2. **Install dependencies:**
```bash
.\vcpkg install libpng:x64-windows
.\vcpkg install libjpeg-turbo:x64-windows
```

3. **Install libsvg:**

Libsvg is not in vcpkg and must be built from source. It requires:
- libxml2
- libpng
- Cairo (optional)

**Note:** libsvg is an older, unmaintained library. For modern SVG support, consider converting SVG to G-code using other tools like:
- Inkscape (with G-code plugins)
- svg2gcode Python tools
- Online SVG to G-code converters

### Option 2: Convert SVG to G-code Externally

**Easier workflow:**
1. Use Inkscape or online tools to convert SVG → G-code
2. Use `draw_gcode.exe` to cut the G-code file

**Inkscape G-code Plugin:**
- Extensions → Render → G-code Tools
- Configure for Cricut coordinate system (404 units/inch)

---

## Troubleshooting

### "Port not open"

**Solutions:**
1. Verify COM port in Device Manager
2. Close other applications using the port
3. Try running as Administrator
4. Use `\\.\COMx` format for COM10 and above

### "Cannot find device file"

**Solutions:**
1. Check Cricut is powered on and connected
2. Install FTDI drivers: https://ftdichip.com/drivers/
3. Restart computer after driver installation

### G-code doesn't cut correctly

**Possible issues:**
1. **Coordinate mismatch** - Verify units (404 = 1 inch)
2. **Outside cutting area** - Check max dimensions for your model
3. **Missing M3/M5** - Ensure pen up/down commands are present
4. **Wrong orientation** - Try rotating design 90°

### Commands execute but Cricut doesn't move

**Solutions:**
1. Verify encryption keys in `keys.txt`
2. Check Cricut model compatibility
3. Try different firmware version (enumerate.exe)
4. Power cycle the Cricut

---

## Example Workflows

### Workflow 1: Test Basic Connectivity

```bash
# 1. Test system
test_endian.exe
test_btea.exe

# 2. Test serial connection
test_serial.exe COM6

# 3. Identify device
enumerate.exe COM6
```

### Workflow 2: Cut a G-code File

```bash
# Create or download a G-code file (simple_square.gcode)

# Cut the file
draw_gcode.exe COM6 simple_square.gcode -d 2

# Monitor output for errors
```

### Workflow 3: Custom Script

```bash
# Create script (square.txt):
# M 0 0
# L 1000 0
# L 1000 1000
# L 0 1000
# L 0 0

# Execute script
interpreter.exe COM6 square.txt
```

---

## Additional Windows-Specific Notes

### COM Port Names

- **COM1-COM9**: Use directly (e.g., `COM6`)
- **COM10+**: May need `\\.\COM10` format

### File Paths

Always use absolute paths or proper escaping:

**Good:**
```bash
draw_gcode.exe COM6 "C:\Users\bill\designs\square.gcode"
draw_gcode.exe COM6 C:\designs\square.gcode
```

**Bad:**
```bash
draw_gcode.exe COM6 C:\Users\bill\my designs\square.gcode  # Space not quoted
```

### Permissions

Some operations may require Administrator privileges:
- Right-click Command Prompt → "Run as Administrator"

---

## Next Steps

1. **Create test G-code files** - Start with simple shapes
2. **Test with scrap material** - Don't use expensive materials initially
3. **Calibrate coordinates** - May need to adjust origin/scaling
4. **Explore G-code generators** - Find tools that output compatible G-code
5. **Join community forums** - Share findings and get help

---

## Summary of Fixed Issues

All utilities required Windows-specific fixes:

1. ✅ `gcode.cpp` - Added `_USE_MATH_DEFINES` for M_PI constants
2. ✅ `gcode.cpp` - Fixed C99 compound literal syntax
3. ✅ `enumerate.cpp` - Removed Unix sys/time.h dependency
4. ✅ `interpreter.cpp` - Added Windows Sleep() wrapper
5. ✅ `test_speed.cpp` - Implemented Windows getCurTime()

All source code changes maintain Linux/Mac compatibility.

---

**Last Updated:** 2025-11-15
**Tested On:** Windows 11, COM6, Cricut Expression
