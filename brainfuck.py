#==========================================================
# Imports
#==========================================================
import os
import sys
from typing import Any
#==========================================================
# GETCH input
#==========================================================
if os.name == "nt":
    import msvcrt
    
    def getch():
        return msvcrt.getch()
else:
    def getch():
        raise NotImplemented("Currently input support in terminal is only available for windows.")
#==========================================================
# The Interpreter
#==========================================================
OPERATORS = "<>+-,.[]"

def make_bracemap(code):
    brace_stack, bracemap = [], {}

    for i, char in enumerate(code):
        if char == '[':
            brace_stack.append(i)
        elif char == ']':
            start = brace_stack.pop()

            bracemap[start] = i
            bracemap[i] = start

    return bracemap

def evaluate(source: str, settings: dict[str, Any]):
    debug_each_time = settings.get("debug_each_time", False)
    debug_at_end = settings.get("debug_at_end", False)
    
    code = source
    bracemap = make_bracemap(code)

    arr = [0]
    ptr = 0
    codeptr = 0

    while codeptr < len(code):
        op = code[codeptr]

        if debug_each_time:
            if op in OPERATORS:
                print(f"Debug(op: {op} | ptr: {ptr} | codeptr: {codeptr+1} | array: {arr})")
            else:
                print(f"Debug(comment: {op} | ptr: {ptr} | codeptr: {codeptr+1} | array: {arr})")
        
        if op == '+':
            arr[ptr] += 1
            if arr[ptr] == 256:
                arr[ptr] = 0
        elif op == '-':
            arr[ptr] -= 1
            if arr[ptr] == -1:
                arr[ptr] = 255
        elif op == '<':
            ptr -= 1
            if ptr == -1:
                ptr = 0
        elif op == '>':
            ptr += 1
            if ptr == len(arr):
                arr.append(0)
        elif op == '.':
            print(chr(arr[ptr]), end='')
        elif op == ',':
            arr[ptr] = ord(getch())
        elif op == '[':
            if arr[ptr] == 0:
                codeptr = bracemap[codeptr]
        elif op == ']':
            if arr[ptr] != 0:
                codeptr = bracemap[codeptr]

        codeptr += 1

    if debug_at_end:
        print(f"Debug(ptr: {ptr} | array: {arr})")


#==========================================================
# The Program
#==========================================================

def run_file(filepath: str):
    with open(filepath, 'r', encoding="utf-8") as file:
        evaluate(file.read())

def run_prompt():
    print("Welcome to Brainf**k Interpreter, Enter 'quit' to exit.\n")

    settings = {}

    while True:
        line = input("Brainf**k > ")
        if line == 'quit':
            break
        elif line.strip().replace(' ', '').startswith("debugLevel="):
            command = line.strip().replace(' ', '')[len("debugLevel="):]

            if command == "0":
                settings["debug_each_time"] = False
                settings["debug_at_end"] = False
                continue
            elif command == "1":
                settings["debug_each_time"] = False
                settings["debug_at_end"] = True
                continue
            elif command == "2":
                settings["debug_each_time"] = True
                settings["debug_at_end"] = False
                continue
            elif command == "3":
                settings["debug_each_time"] = True
                settings["debug_at_end"] = True
                continue

        evaluate(line, settings)            
        print()

def main():

    args = sys.argv[:]

    if len(args) == 1:
        run_prompt()
    elif len(args) == 2:
        run_file(args[1])
    else:
        print(f"""Usage:
\tpython {args[0]} [filepath] : To run program from file
\tpython {args[0]}            : To run Brainf**k commandline interprater""")


if __name__ == "__main__":
    main()





    

        
