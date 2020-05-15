# Copyright (c) 2020 Pranjal Rastogi
#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, please use only this version
# utilities for CodeStyliser

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
            ifChecker = lines[nxtLnIndex].find("if")
            whileChecker = lines[nxtLnIndex].find("while")
            elseChecker = lines[nxtLnIndex].find("else")
            firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
            if forChecker == firstCharOfNxtLn or ifChecker == firstCharOfNxtLn or whileChecker == firstCharOfNxtLn or elseChecker == firstCharOfNxtLn:
                # another for has been found before () number got equal, Cancel case
                break
            openParenthNo = len(re.findall(
                r"\(", lines[nxtLnIndex])) + openParenthNo
            closeParenthNo = len(re.findall(
                r"\)", lines[nxtLnIndex])) + closeParenthNo
            nxtLnIndex = nxtLnIndex + 1
        else:
            # closeParenthNo = openParenthNo
            if openParenthNo == 0:
                return None
            return (False, nxtLnIndex)
        return None
    else:
        if openParenthNo == 0:
            return None
        return (True,)


def checkForOpenBrace(nextLineIndex, lines):

    while True:
        lineWithoutComment = trimComment(lines[nextLineIndex])
        if lineWithoutComment.hasComment == True or lines[nextLineIndex].isspace():
            # line has comment or is blank
            if lineWithoutComment.line.find("{") != -1:
                # if the line before comment has {, become happy
                break
            elif not lineWithoutComment.line.isspace():
                break
            nextLineIndex = nextLineIndex + 1
        else:
            break

    return lineWithoutComment.line.find("{")


def getNextSemiColonLine(index, lines):
    while True:
        lineWithoutComment = trimComment(lines[index])
        semiColonIndex = lineWithoutComment.line.find(";")
        if semiColonIndex == -1:
            # the line without Comment has NO semicolon
            index = index + 1
        else:
            # line has a semicolon and is NOT a comment
            break
    return index


if __name__ == "__main__":
    print("Do not run utils, run codeStyliser instead!")
