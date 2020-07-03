# Changelog

All notable changes to the CodeStyliser project will be documented in this file.

## RELEASED

### [0.1.11] - 2020-05-21 [CURRENT RELEASE]

#### Added

- Support for giving only filename as a command line argument, using python's argparse package. One Can now give File name using `-f` or a directory name using `-d` flags. Help can be obtained by `-h`.

#### Changed

- Updated README
- Updated Command line output

#### Removed

- Compulsory Directory name.

## DEVELOPMENT

### [Not Listed Changes]


### [0.1.11.8-DEV] - 2020-07-03

#### Changed
Changed change log entry to accurately represent fixed issues

#### Fixed
- Fixed multiple issues, [#29](https://github.com/PjrCodes/CodeStyliser/issues/29), 
[#30](https://github.com/PjrCodes/CodeStyliser/issues/30), [#31](https://github.com/PjrCodes/CodeStyliser/issues/31
), [#32](https://github.com/PjrCodes/CodeStyliser/issues/32)


### [0.1.11.7-DEV] - 2020-07-03

#### Fixed
- Fixed latest issue [Non Matching else issue](https://github.com/PjrCodes/CodeStyliser/issues/28)

### [0.1.11.6+1-DEV] - 2020-07-03 [HOT-FIX]

#### Fixed
- Comment error (unlisted issue)

### [0.1.11.6-DEV] - 2020-07-03 

#### Fixed
- An error that rose related to else/ else if checking in previous version.

### [0.1.11.5-DEV] - 2020-06-25 [YANKED]

#### Fixed
- Exception handling error that arose in version [0.1.11.4-DEV](#[0.1.11.4-dev]---2020-06-25-[yanked])

### [0.1.11.4-DEV] - 2020-06-25 [YANKED]

***WARNING***: Not completely tested.

#### Changed
- The way else/ else if is handled


### [0.1.11.2-DEV] - 2020-06-18

#### Changed
- **Highly** modularised code internally
- Performance improvements
- PEP8 Compliance

### [0.1.11.1] - 2020-05-21

#### Changed

- Added experimental support for `.h` files back.

### [0.1.11] - 2020-05-21

This is the current release, please see [CURRENT RELEASE](#[0.1.11]---2020-05-21-[CURRENT-RELEASE])

### [0.1.10.4] - 2020-05-21

#### Added

- A time taken counter

#### Changed

- Updated README
- Updated Command line output

### [0.1.10.3] - 2020-05-21

#### Changed

- Updated README

#### Fixed

- A few FATAL issues that arised related to macros

#### Removed

- Support for `.h`, Header files

### [0.1.10.2] - 2020-05-21 [YANKED]

#### Fixed

- A few macro related bugs

### [0.1.10.1] - 2020-05-21 [YANKED]

#### Changed

- README has been updated

#### Fixed

- A few bugs

### [0.1.10.0] - 2020-05-21

#### Added

- Experimental support for `.h`, Header files

#### Changed

- Updated README

#### Fixed

- keyword on last line of macro error

### [0.1.9.9] - 2020-05-20

#### Changed

- How the macro system is detected
- Keyword detection has been revamped

#### Fixed

- MACRO-error, which had arised again
- FUNNY-FOR-LOOP error, which is now fixed
- New comment issue, which will now be catched

### [0.1.9.8] - 2020-05-20

#### Changed

- README has been updated

#### Fixed

- MACRO-error, now works for macros!

### [0.1.9.8] - 2020-05-20

#### Changed

- README has been updated

#### Fixed

- MACRO-error, now works for macros!

### [0.1.9.7] - 2020-05-20

#### Changed

- Command line output beautification

#### Fixed

- A lot of bugs

### [0.1.9.6] - 2020-05-20

#### Removed

- Printing of new changes

#### Changed

- Command line output beautification

#### Fixed

- A lot of bugs

### [0.1.9.5] - 2020-05-19

#### Added

- BSD-2 Clause LICENSE, README files

#### Changed

- Updated gitignore and untracked gitignore changes

#### Fixed

- Multi line comment error, Now the code doesnt fail for multiline comments

#### Removed

- Printing of known bugs

### [0.1.9.3] - 2020-05-19

#### Fixed

- Same line parentheses error: {} added after last ) but must be added after (condition) parentheses

### [0.1.9.3] - 2020-05-19

#### Fixed

- Same line parentheses error: {} added after last ) but must be added after (condition) parentheses

### [0.1.9.2] - 2020-05-18

#### Added

- Now prints out all current errors

#### Changed

- Renamed "utils.py" to "utilities.py"

### [0.1.9] - 2020-05-17

#### Changed

- Single line code handling is now smarter and add's comments back

### [0.1.8] - 2020-05-17

#### Added

- The code now handles keywords that end on the same line also, for example, `if(...) statement;` is now handled.

### [0.1.6] - 2020-05-16

#### Added

- The code now ignores all keywords that have a # after them on the next immediate line

#### Fixed

- Another unnamed error that had arised (error #9), this was an error related to `#` after detected keywords

### [0.1.5] - 2020-05-16

#### Added

- Support for multiline comments
  - i.e, now the code checks for multiline comments

#### Fixed

- Another unnamed error that had arised (error #N2), this was an error related to comments

### [0.1.4] - 2020-05-16

#### Fixed

- Another unnamed error that had arised (error #10), this was an error related to line index with parentheses and multi line conditions

### [0.1.3] - 2020-05-16

#### Fixed

- Another unnamed error that had arised (error #11), this was an error related to line index

### [0.1.2] - 2020-05-16

#### Added

- Multiline comment block on top of source code files

#### Fixed

- Another unnamed error that had arised (error #6)

### [0.1.1] - 2020-05-16

#### Changed

- The source code file "codeStyliser0.1.0+1.py" has been renamed to "codeStyliser.py" to keep simplicity

#### Fixed

- Another unnamed error that had arised

### [0.1.0] - 2020-05-16

#### Added

- Now gives errors in the command line and catches exceptions instead of fatally failing and crashing

#### Changed

- Command line output has been beautified
- Renamed "codeStyliser0.0.9.6.py" to "codeStyliser0.1.0+1.py"

### [0.0.9.6] - 2020-05-16

#### Added

- Changes line endings from windows style to unix style for all files that are given
- A "utils.py" file to support "codeStyliser0.0.9.6.py"

#### Changed

- Command line output, It has now been Beautified
- Under the hood refactoring changes, such as dividing code into two seperate files
- Renamed "codeStyliser0.0.9.4.py" to "codeStyliser0.0.9.6.py"

#### Fixed

- Program doesnt give UnicodeDecodeError's anymore for CRLF files, by the fix in added.
- A few fatal bugs that had arised during testing of v0.0.9.4

### [0.0.9.4] - 2020-05-14

#### Changed

- The "codeStyliser.py" file is now renamed to "codeStyliser0.0.9.4.py"

#### Fixed

- Error handling methods

### [0.0.9.3] - 2020-05-14 [YANKED]

#### Added

- Better error handling method

### [0.0.9.1] - 2020-05-14

#### Fixed

- Extension checking method now detects only c files, before it also used to detect .c.extension files.

### [0.0.9] - 2020-05-14

#### Added

- Recursive folder editing, Now recursively goes throught the folders and subfodlers of a given directory instead of working on just one file

#### Removed

- Support for giving only a file to format. One must now always give a directory

### [0.0.8] - 2020-05-14

#### Fixed

- Now adds comment's back on the line if a comment was on that line

### [0.0.7] - 2020-05-14

#### Added

- Support for `else` and `} else` statements

#### Changed

- Command line output slightly

### [0.0.6] - 2020-05-14

#### Added

- First character check to ignore all keywords that are not on the first non-whitespace character of a line

#### Removed

- Multiline comment checking

### [0.0.5] - 2020-05-14

#### Fixed

- Fixed range error that was being recieved when searching for open curly braces

### [0.0.4] - 2020-05-14

#### Added

- Multiline (Condition) checks for for and while loops and if conditions.
- Multiline comment checking

### [0.0.3] - 2020-05-14

#### Added

- Loops over close and open parentheses till it finds the same amount of close and open parentheses
- Added basic support for If conditions

#### Changed

- renamed "main.py" to "codeStyliser.py"
- Updated some command line output

### [0.0.2] - 2020-05-14

#### Added

- Basic command line argument support

### [0.0.1] - 2020-05-14

#### Added

- Initial logic to add curly braces in "main.py"
- Support for while and for loops
- Parentheses checking, single line comment checking, SemiColon checking
- Initial (first) commit, with basic files


[Not Listed Changes]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.11...HEAD
<!-- [0.1.11.1]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.11...v0.1.11.1 -->
[0.1.11]: https://github.com/PjrCodes/CodeStyliser/compare/releases/tag/v0.1.11
<!-- [0.1.10.4]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.10.3...v0.1.10.4
[0.1.10.3]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.10.2...v0.1.10.3
[0.1.10.2]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.10.1...v0.1.10.2
[0.1.10.1]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.10.0...v0.1.10.1
[0.1.10.0]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.9...v0.1.10.0
[0.1.9.9]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.8...v0.1.9.9
[0.1.9.8]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.7...v0.1.9.8
[0.1.9.7]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.6...v0.1.9.7
[0.1.9.6]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.5...v0.1.9.6
[0.1.9.5]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.3...v0.1.9.5
[0.1.9.3]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9.2...v0.1.9.3
[0.1.9.2]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.9...v0.1.9.2
[0.1.9]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.8...v0.1.9
[0.1.8]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.6...v0.1.8
[0.1.6]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/PjrCodes/CodeStyliser/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.9.6...0.1.0
[0.0.9.6]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.9.4...v0.0.9.6
[0.0.9.4]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.9.3...v0.0.9.4
[0.0.9.3]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.9.1...v0.0.9.3
[0.0.9.1]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.9...v0.0.9.1
[0.0.9]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/PjrCodes/CodeStyliser/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/PjrCodes/CodeStyliser/releases/tag/v0.0.1 -->
