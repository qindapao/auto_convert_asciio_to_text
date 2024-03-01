#!/usr/bin/env python3

import os
import sys
import time
import subprocess

# print(sys.argv)
if len(sys.argv) != 5:
    print("Usage: {} <asciio file> <target file> <start marker> <end marker>".format(sys.argv[0]))
    sys.exit(1)

asciio_file = sys.argv[1]
target_file = sys.argv[2]
start_marker = sys.argv[3]
end_marker = sys.argv[4]

last_modified = os.path.getmtime(asciio_file)

first_run = True

os.system("startxwin >/dev/null 2>&1 &")
os.environ["DISPLAY"] = ":0.0"

while True:
    current_modified = os.path.getmtime(asciio_file)
    if current_modified != last_modified or first_run:
        time.sleep(0.2)
        last_modified = current_modified

        with open(os.devnull, 'w') as devnull:
            asciio_text = subprocess.check_output(["asciio_to_text", asciio_file], stderr=devnull).decode('utf-8', 'ignore')

        # print("asciio text:")
        # print(asciio_text)

        with open(target_file, 'r') as file:
            lines = file.readlines()

        # print(lines)
        target_text = "".join(lines[lines.index(start_marker+'\n')+1 : lines.index(end_marker+'\n')])

        # print("target text:")
        # print(target_text)

        start_count = "".join(lines).count(start_marker)
        end_count = "".join(lines).count(end_marker)

        if start_count != 1 or end_count != 1:
            print("Start or end marker is not unique. No replacement will be made.")
            continue

        if asciio_text != target_text:
            lines[lines.index(start_marker+'\n')+1 : lines.index(end_marker+'\n')] = [ asciio_text ]
            with open(target_file, 'w') as file:
                file.write("".join(lines))
            print("Content has been replaced!")
        else:
            print("No need to replace.")

        first_run = False

    time.sleep(0.2)
