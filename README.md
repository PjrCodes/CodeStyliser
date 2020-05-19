# CodeStyliser
This is the repository for the Code Styliser utility, written by Pranjal Rastogi.

The Code Styliser utility adds curly braces `{}` in all C files `.c` under a directory, wherever needed.

This utility is written in Python 3.7.7, 64-Bit

Currently, it adds curly braces for `for()` and `while()` loops, and `if()`, `else if()`,`else` conditions.

## Installation

* Make sure you have Python 3.7.7 64-Bit installed on your device. If this is not done, Install Python3.7.7 from [www.python.org](www.python.org)
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

### MACRO-ERROR
```c
/* MACRO-ERROR */
// In multiline macros, the {} are added invalidly as they must be added before \. but are added after \.

if()  \
   s; \
else asl; \

// Also in this error is this:
// If the keyword is found at the end of the macro, braces are added invalidly

macro \
if() {
... // somewhere later in the file
statement;
}
...
```
The above error occurs if there is a macro. See above for a description

### HASH-ERROR
```c
/* HASH-ERROR */
// hash(#) error, {} is added invalidly if there is an preprocesser/ macro after the keyword that has been detected

if (rv->rv_d.dc < dnpw_cfg->samelane_right_edge_mts)))
   #endif
```
The above error occurs if there is a macro. See above for a description

### KEYWORD-ERROR
```c
/* KEYWORD-ERROR */
// Here, for() is ignored, as { } of the switch() are detected as for's {}
for()
   switch() {
      a;
   }


// Here, for() is not ignored, but instead {} are added invalidly
for()
  switch()
  {
    a;
  }
```
The above error occurs if there is a macro. See above for a description

## License
Copyright (C) Pranjal Rastogi 2020

This utility has no warranty.
Please see LICENSE for warranty, sharing and other details.
