# CodeStyliser
This is the repository for the Code Styliser utility, written by Pranjal Rastogi.

The Code Styliser utility adds curly braces \[`{}`\] in all C-source \[`.c`\] files and Header \[`.h`\] files under a given directory, wherever needed.
It adds braces after single line `if()`, `for()`, `while()`, `else`, `else if()` statements.

For example,

```c
if(a == b)
  statement;
```

will become

```c
if(a == b) {
  statement;
}
```

This utility is written in Python 3.7.7, 64-Bit. Currently, you must have Python 3.7.7, 64-Bit installed on your machine for this utility to work. Check [install](#Install) for more details

## Install

* Make sure you have Python 3.7.7 64-Bit installed on your device. 
  * If this is not done, Install Python3.7.7 from [python.org](https://www.python.org)
* Now, download `utilities.py` and `codeStyliser.py` from releases into the required directory

* now, just run `$ python3.7 codeStyliser.py .` in the desired directory

## Known issues

Please check [issues](https://github.com/PjrCodes/CodeStyliser/issues) for the latest bugs
 
## License
Copyright (C) Pranjal Rastogi 2020

This utility has no warranty.
license: BSD-2 Clause
Please see LICENSE for more information
