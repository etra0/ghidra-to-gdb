"""
Small utility to generate debugging symbols from a ghidra-exported header.
This is useful to load them to GDB and then cast raw pointers to the structs to
have a pretty print!
"""

from subprocess import Popen, PIPE
import re
import sys
import argparse

STRUCT_RE = re.compile(r"struct (\w+)")

def main(filename: str, extra_args: str, output_name: str):
    definitions = None
    with open(filename, 'r', encoding='utf-8') as header:
        definitions = header.read()

    # By default, ghidra doesn't export the `pointer` type, and some
    # definitions use the pointer32 too.
    definitions = "typedef void* pointer;\ntypedef void* pointer32;\n" + definitions

    # For some classes, ghidra will generate some names with double colon, so
    # we need to remove those.
    definitions = definitions.replace("::", "__")

    finds = set(STRUCT_RE.findall(definitions))
    # In order to generate symbols, we need the structs to be *actually* used.
    # So we generate some empty structs for the debugging flag to export.
    for struct in finds:
        definitions += f"struct {struct} dummy_{struct};\n"

    popen_args = ['gcc', '-g', '-c', '-xc', f'-o{output_name}']
    if extra_args is not None:
        popen_args += extra_args.split(',')

    # We compile from stdin.
    popen_args.append('-')

    returncode = None
    out, err = (None, None)
    with Popen(popen_args, stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        result = proc.communicate(input=definitions.encode())
        out, err = result
        returncode = proc.returncode

    if proc.returncode:
        print(f"""Something went wrong while running:\
                \n > {" ".join(popen_args)} \
                \n{err.decode()}""")
        sys.exit(returncode)

    if len(out) != 0:
        print(f"Compiled with some warnings:\n\n{out.decode()}")

    print(f"generated {output_name} successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate obj file with symbol information")
    parser.add_argument('header', help="Path of the header file")
    parser.add_argument('--gcc_args',
            help="Extra arguments for GCC, separated by a comma (,)")
    parser.add_argument('--output',
            help="Name of the output file, default is symbols.o",
            default="symbols.o")
    args = parser.parse_args()
    main(args.header, args.gcc_args, args.output)
