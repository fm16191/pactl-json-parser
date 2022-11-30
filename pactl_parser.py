# import sys
import json
import os
import subprocess

# Using popen
# result = os.popen("pactl list sink-inputs").read()

# Using subprocess (much faster)
p = subprocess.run("pactl list sink-inputs".split(), capture_output=True)
result = p.stdout.decode()

# Syntax fix
result = result.replace(u"\xa0", " ") # Broken encoding for spaces
result = result.replace(u"\\\"", "\"") # Replacing all espaced doublequote to inline singlequote (JSON compliant)
result = result.replace(u"\"", "\'")

sinks = dict()

for oline in result.split("\n"):
    if oline == "": continue # Skip empty lines
    # Indentation indicates the JSON structure
    indent = oline.count('\t')
    line = oline[indent:]
    if indent == 0: # Get sink name
        sink_name = line.split("#")[-1]
        sinks[sink_name] = {}
    elif indent == 1: # Get sink object
        if line.startswith("        "): # Output is over two lines
            sinks[sink_name][name] = sinks[sink_name][name] + " " + line.strip()
        else:
            ii = line.index(":")
            name = line[:ii].strip()
            value = line[ii + 1:].strip()
            sinks[sink_name][name] = value
    elif indent == 2: # Get sink object properties
        if sinks[sink_name][name] == "":
            sinks[sink_name][name] = {}
        ii = line.index("=")
        sub_name = line[:ii].strip()
        sub_value = line[ii + 1:].strip()
        if sub_value[0] == "'" and sub_value[-1] == "'":
            sub_value = sub_value[1:-1]
        sinks[sink_name][name][sub_name] = sub_value
    else: # Unexpected indentation
        print("Unexpected line : ", oline)
        exit()

    # with open("test.json", "w") as fo:
    #     json.dump(sinks, fo, indent=2, ensure_ascii=False)

print(json.dumps(sinks, indent=2))