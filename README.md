# CodeStyliser
This is the repository for the Code Styliser utility, written by Pranjal Rastogi.

The Code Styliser utility adds curly braces `{}` in all C files `.c` under a directory, wherever needed.

This utility is written in Python 3.7.7, 64-Bit

Currently, it adds curly braces for `for()` and `while()` loops, and `if()`, `else if()`,`else` conditions.

## Installation

* Make sure you have Python 3.7.7 64-Bit installed on your device. If this is not done, Install Python3.7.7 from [python.org](https://www.python.org)
* This utility has no dependencies. Just download/ clone `utilities.py` AND `codeStyliser.py` into the required directory
* now, just run `$ python3.7 codeStyliser.py .`
* And, wait and watch as magic happens!

## Examples
An example could be,

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


## Known issues

Please check [issues](https://github.com/PjrCodes/CodeStyliser/issues) for the latest bugs
 
## License
Copyright (C) Pranjal Rastogi 2020

This utility has no warranty.
Please see LICENSE for warranty, sharing and other details.
