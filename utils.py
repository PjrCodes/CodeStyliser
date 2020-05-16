#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# This code cannot be copied. Violators will be prosecuted.
# ---
# code styliser program
# ---
# Made in python 3.7.7 64 bit, please use only this version
# ---
# utils.py
# utils for Codestyliser.py
# ---
# DO NOT RE-DISTRIBUTE

import re

SINGLELINE_COMMENT_PATTERN = r"(\/\*[^\n]*)|(\/\/[^\n]*)"
KEYWORDS = ['for', 'while', 'do', 'switch', 'if', 'else']

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
            firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
            for keyword in KEYWORDS:
                if lines[nxtLnIndex].find(keyword) == firstCharOfNxtLn:
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

    while nextLineIndex < (len(lines)):
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
    
    while index < (len(lines)):
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

def checkForHash(index, lines):
    index = index + 1
    while index < (len(lines)):
        lineWithoutComment = trimComment(lines[index], index, lines)
        if lineWithoutComment.hasComment == True or lines[index].isspace():
            # line has comment or is blank
            if lineWithoutComment.isMultiline == True:
                # go after multiline comments
                if lineWithoutComment.line.find("#") != -1:
                    break
                index = lineWithoutComment.multiLineJumpIndex
                
            index = index + 1
        else: 
            break
    return lineWithoutComment.line.find("#")



""" 
THE FOLLOWING CODE DONT WORK. COMMENTING
"""
# def hasKeyword(index, lines):

#     #TODO: Fix, DOESNT WORK!!!
#     # return True if we find a keyword IMMEDIATELY after the keyword.
#     # current line index = index, so index has the first keyword
#     index = index + 1 # start check from one line next
#     while index < (len(lines)):
#         # loop through till file ends
#         lineNoComment = trimComment(lines[index], index, lines)
#         if lineNoComment.isMultiline == True:
#             # it is multiline comment
#             # we must jump index, but also check keywords  
#             for keyword in KEYWORDS:
#                 if lineNoComment.line.find(keyword) != -1:
#                     return True
#                 else:
#                     # keyword not found, after Multiline Comment!
#                     index = lineNoComment.multiLineJumpIndex
#             index = lineNoComment.multiLineJumpIndex
#         elif lineNoComment.hasComment and lineNoComment.isMultiline == False:
#             # line has comment, we must check for the space before line
#             for keyword in KEYWORDS:
#                 if lineNoComment.line.find(keyword) != -1:
#                     return True
#                 else:
#                     # line has no keyword
#                     index = index + 1
#         elif lines[index].isspace():
#             index = index + 1
#             continue
#         else:
#             for keyword in KEYWORDS:
#                 if lineNoComment.line.find(keyword) != -1:
#                     return True
#                 else:
#                     continue
#             return False
#     return False


if __name__ == "__main__":
    print("Do not run utils, run codeStyliser instead!")
