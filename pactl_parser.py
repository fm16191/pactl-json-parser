# import subprocess
# import sys
import json
import os

def get_indent(line): # Returns clean line & its indentation
    indent = 0
    while(line.startswith("\t")):
        line = line[1:]
        indent = indent + 1
    return indent, line

# Using subprocess
# sys.stdout.reconfigure(encoding='utf-8')
# result = subprocess.check_output("pactl list sink-inputs", shell=True)
# result = result.decode("utf-8")

# Using popen
result = os.popen("pactl list sink-inputs").read()

# Syntax fix
result = result.replace(u"\xa0", " ") # Broken encoding for spaces
result = result.replace(u"\\\"", "\"") # Replacing all espaced doublequote to inline singlequote (JSON compliant)
result = result.replace(u"\"", "\'")

sinks = dict()

for oline in result.split("\n"):
    if oline == "": continue # Skip empty lines
    (indent, line) = get_indent(oline) # Indentation indicates the JSON structure
    if indent == 0: # Get sink name
        sink_name = line.split("#")[-1]
        sinks[sink_name] = {}
    elif indent == 1: # Get sink object
        if line.startswith("        "): # Output is over two lines
            sinks[sink_name][name] = sinks[sink_name][name] + " " + line.strip()
        else:
            name = line[:line.index(":")].strip()
            value = line[line.index(":")+1:].strip()
            sinks[sink_name][name] = value
    elif indent == 2: # Get sink object properties
        if sinks[sink_name][name] == "":
            sinks[sink_name][name] = {}
        sub_name = line[:line.index("=")].strip()
        sub_value = line[line.index("=")+1:].strip()
        if sub_value[0] == "'" and sub_value[-1] == "'":
            sub_value = sub_value[1:-1]
        sinks[sink_name][name][sub_name] = sub_value
    else: # Unexpected indentation
        print("Unexpected line : ", oline)
        exit()

    # with open("test.json", "w") as fo:
    #     json.dump(sinks, fo, indent=2, ensure_ascii=False)

print(json.dumps(sinks, indent=2))