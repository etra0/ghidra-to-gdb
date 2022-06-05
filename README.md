# Ghidra to GDB
Small utility to generate debugging symbols from a ghidra-exported header.
This is useful to load them to GDB and then cast raw pointers to the structs to
have a pretty print!

```gdb
# cossacks.h is exported from the Data Type Manager from Ghidra.
python ghidra_to_gdb.py --gcc_args=-m32 cossacks.h

gdb my_software
(gdb) add-symbol-file ./symbols.o
(gdb) p/x *(struct TList*)*0x008F4D24
$5 = {ptr = 0x4223a0, first_element = 0x331ca70, size = 0x1, field3_0xc = 0x4}
```

## Usage:
```bash
usage: ghidra_to_gdb.py [-h] [--gcc_args GCC_ARGS] [--output OUTPUT] header

Generate obj file with symbol information

positional arguments:
  header               Path of the header file

options:
  -h, --help           show this help message and exit
  --gcc_args GCC_ARGS  Extra arguments for GCC, separated by a comma (,)
  --output OUTPUT      Name of the output file, default is symbols.o
```
