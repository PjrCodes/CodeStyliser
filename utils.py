# utils
import re

SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"

def getFirstCharacterIndex(str):
    return len(str) - len(str.lstrip())

def checkForParentheses(line, lineIndex, lines):
    openParenthNo = len(re.findall(r"\(", line))
    closeParenthNo = len(re.findall(r"\)", line))

    if openParenthNo != closeParenthNo:
        # the line doesnt have same amt of close and open parentheses
        nxtLnIndex = lineIndex + 1

        while closeParenthNo != openParenthNo:
            forChecker = lines[nxtLnIndex].find("for")
            firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
            if forChecker == firstCharOfNxtLn:
                # another for has been found before () number got equal, Cancel case
                break
            openParenthNo = len(re.findall(r"\(", lines[nxtLnIndex])) + openParenthNo
            closeParenthNo = len(re.findall(r"\)", lines[nxtLnIndex])) + closeParenthNo
            nxtLnIndex = nxtLnIndex + 1
        else:
            # closeParenthNo = openParenthNo
            # check for OpenCurlyBrace on same line as (condition)
            return (False, nxtLnIndex)
        return None
    else:
       
        return (True,)

def checkForOpenBrace(nextLineIndex, lines):
    while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
        # next line is a singleLineComment OR a space, we must skip it
        nextLineIndex =  nextLineIndex + 1
    else:
        return lines[nextLineIndex].find("{")


if __name__ == "__main__":
    print("Do not run utils, run codeStyliser instead!")