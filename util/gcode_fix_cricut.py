#!/usr/bin/env python3
"""
Fix GRBL-Plotter G-code for Cricut
- Keeps coordinates as-is (in mm)
- Adds G21 (metric mode)
- Converts Z-axis to M3/M5
"""

import re
import sys

def convert_file(input_path, output_path):
    print(f"Converting: {input_path} -> {output_path}")

    # Read file (handle UTF-16 from GRBL-Plotter)
    try:
        with open(input_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()
        print("  Encoding: UTF-16")
    except:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print("  Encoding: UTF-8")

    output = []
    output.append("G21 (metric mode - mm)\n")
    output.append("G90 (absolute positioning)\n")

    for line in lines:
        # Skip existing G21/G90 to avoid duplicates
        if re.match(r'^\s*G2[01]', line, re.IGNORECASE):
            continue

        # Convert Z-axis pen commands
        if 'Z' in line:
            if re.search(r'G0*\s+Z\s*[+]?[0-9.]+', line, re.IGNORECASE):
                output.append("M5\n")
                continue
            elif re.search(r'G0*1\s+Z\s*-[0-9.]+', line, re.IGNORECASE):
                output.append("M3\n")
                continue

        # Keep everything else as-is (coordinates in mm)
        output.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output)

    print(f"  Lines: {len(lines)} -> {len(output)}")
    print(f"\n[OK] Done! Coordinates kept in mm, libcutter will convert.")
    print(f"\nTest with:")
    print(f'  draw_gcode.exe COM7 "{output_path}" -d 1')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gcode_fix_cricut.py <input.nc> <output.nc>")
        sys.exit(1)

    convert_file(sys.argv[1], sys.argv[2])
