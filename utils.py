# utils
import re

SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"

class lineWithComment:

    def __init__(self, line, hasComment, comment):
        self.line = line
        self.hasComment = hasComment
        self.comment = comment

def trimComment(line):
    searchForComment = re.search(SINGLELINE_COMMENT_PATTERN, line)
    if (searchForComment):
        # found a comment
        return lineWithComment(line[:searchForComment.start()], True, searchForComment.group())
    else:
        # no comment
        return lineWithComment(line, False, None)



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
            return (False, nxtLnIndex)
        return None
    else:
       
        return (True,)

def checkForOpenBrace(nextLineIndex, lines):
    invalidLine = True
    while invalidLine:
        lineWithoutComment = trimComment(lines[nextLineIndex])
        if lineWithoutComment.hasComment == True:
            if lines[nextLineIndex].isspace():
                nextLineIndex =  nextLineIndex + 1
                invalidLine = True
            else:
                # line is normal, and not invalid
                invalidLine = False
        else:
            invalidLine = False
        
    else:
        return lineWithoutComment.line.find("{")


if __name__ == "__main__":
    print("Do not run utils, run codeStyliser instead!")