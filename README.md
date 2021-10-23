# MIPS disassembler
## Index
  - [Overview](#overview) 
  - [Getting Started](#getting-started)
  - [Usage](#Usage)
## About this project
A (very small and cute) project to disassemble MIPS instructions based on format parsing.

## Overview
- One of the homeworks in the **Computer Structure subject** was to manually analyze the format of MIPS instructions. And I came to implement this tool.
- This project parses the hex value of the 32-bit instruction corresponding to the **MIPS code**, **analyzes the format**, and **disassembles it**.

## Getting Started
### Depencies
None

## Usage

Jus call `parse` function as follows.

```python
parse(0x3c101001)
```

Then the output is as follows.

```
[*] [lui $s0, $r0, 4097] I-Format
    op     rs    rt    imm
    001111 00000 10000 0001000000000001
    0x0F   0x00  0x10  0x1001
```





