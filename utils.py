# Copyright (c) 2020 Pranjal Rastogi
#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, please use only this version
# utilities for CodeStyliser

import re

SINGLELINE_COMMENT_PATTERN = r"(\/\*[^\n]*)|(\/\/[^\n]*)"


class lineWithComment:

    def __init__(self, line, hasComment, comment, isMultiline, multiLineJumpIndex):
        self.line = line
        self.hasComment = hasComment
        self.comment = comment
        self.isMultiline = isMultiline
        self.multiLineJumpIndex = multiLineJumpIndex


def trimComment(line, lineNo, lines):
    searchForSingleLineComment = re.search(SINGLELINE_COMMENT_PATTERN, line)
    if (searchForSingleLineComment):
        if searchForSingleLineComment.group()[0:2] == "/*":
            # keep searching for */
            sameLineEnd = line.find("*/")
            if sameLineEnd != -1:
                # ends on same line
                # comment = searchForSingleLineComment.group()
                return lineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
            else:
                # iterate for line in lines till we get */
                index = lineNo + 1
                while True:
                    multiCommentEnd = lines[index].find("*/")
                    if multiCommentEnd != -1:
                        # multi line comment has ended
                        return lineWithComment(lines[index][(multiCommentEnd + 2):],True,None,True, index)
                    else:
                        # no multi line comment end found
                        index = index + 1
                    
        # found a single line comment of type //
        return lineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
    else:
        # no comment
        return lineWithComment(line, False, None, False, None)


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
        #TODO: handle multiline
        lineWithoutComment = trimComment(lines[nextLineIndex], nextLineIndex, lines)
        if lineWithoutComment.hasComment == True or lines[nextLineIndex].isspace():
            # line has comment or is blank
            if lineWithoutComment.line.find("{") != -1:
                # if the line before comment has {, become happy
                break
            elif lineWithoutComment.isMultiline == True:
                # go after multiline comments
                nextLineIndex = lineWithoutComment.multiLineJumpIndex
                if lineWithoutComment.line.find("{") != -1:
                    break
            nextLineIndex = nextLineIndex + 1
            # line is a multiline comment
        else:
            break
    return lineWithoutComment.line.find("{")


def getNextSemiColonLine(index, lines):
    while True:
        lineWithoutComment = trimComment(lines[index], index, lines)
        if lineWithoutComment.isMultiline == True:
            semiColonIndex = lines[lineWithoutComment.multiLineJumpIndex].find(";")
        else:
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
