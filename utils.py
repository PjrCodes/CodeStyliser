# utils
import re

def checkForParentheses(line, lineIndex, lines):
    openParenthNo = len(re.findall(r"\(", line))
    closeParenthNo = len(re.findall(r"\)", line))

    if openParenthNo != closeParenthNo:
        isOnSameLine = False
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
            openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
        continue
    else:
        openCurlyBraceIndex = line.find("{")
        isOnSameLine = True


if __name__ == "__main__":
    print("Do not run utils, run codeStyliser instead!")