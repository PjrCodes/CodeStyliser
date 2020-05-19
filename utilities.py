#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# Do not copy this code.
# DO NOT RE-DISTRIBUTE
# ---
# THE codeStyliser Utility
# ---
# Made in python 3.7.7 64 bit, use only this version
# ---
# utils.py
# utils for Codestyliser.py
# ---
#TODO: remove rouge -1
#TODO: use logger
#TODO: use EXCEPTIONS in a SMARTER WAY!!!

import re
import sys

SINGLELINE_COMMENT_PATTERN = r"(\/\*[^\n]*)|(\/\/[^\n]*)"
KEYWORDS = ['for', 'while', 'do', 'switch', 'if', 'else'] #TODO: convert into patterns

class LineWithComment:

    def __init__(self, line, hasComment, comment, isMultiline, multiLineJumpIndex):
        self.line = line
        self.hasComment = hasComment
        self.comment = comment
        self.isMultiline = isMultiline
        self.multiLineJumpIndex = multiLineJumpIndex

class ParenthResult:
    
    def __init__(self, isOnSameLine, lineIndex, lastCloseParenthIndex):
        self.isOnSameLine = isOnSameLine
        self.lineIndex = lineIndex
        self.lastCloseParenthIndex = lastCloseParenthIndex


def trimComment(line, lineNo, lines):
    searchForSingleLineComment = re.search(SINGLELINE_COMMENT_PATTERN, line)
    if (searchForSingleLineComment):
        if searchForSingleLineComment.group()[0:2] == "/*":
            # keep searching for */
            sameLineEnd = line.find("*/")
            if sameLineEnd != -1:
                # ends on same line
                # comment = searchForSingleLineComment.group()
                return LineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
            else:
                # iterate for line in lines till we get */
                index = lineNo + 1
                while True:
                    multiCommentEnd = lines[index].find("*/")
                    if multiCommentEnd != -1:
                        # multi line comment has ended
                        return LineWithComment(lines[index][(multiCommentEnd + 2):],True, lines[index][:(multiCommentEnd+2)] ,True, index)
                    else:
                        # no multi line comment end found
                        index = index + 1
                    
        # found a single line comment of type //
        return LineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
    else:
        # no comment
        return LineWithComment(line, False, "", False, None)


def getFirstCharacterIndex(str):
    return len(str) - len(str.lstrip())


def checkForParentheses(line, lineIndex, lines):
    
    openParenthNo = 0
    closeParenthNo = 0
    index = 0

    while index < len(line):
        if line[index] == '(':
            openParenthNo += 1
        if line[index] == ')':
            closeParenthNo += 1
        if openParenthNo == closeParenthNo and openParenthNo != 0:
            return ParenthResult(True, lineIndex, index)
        index += 1
        
    
    if openParenthNo != closeParenthNo:
        # the line doesnt have same amt of close and open parentheses
        # loop through till we reach same no. of parentheses.

        nxtLnIndex = lineIndex  + 1
        while closeParenthNo != openParenthNo:
            firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
            for keyword in KEYWORDS:
                if lines[nxtLnIndex].find(keyword) == firstCharOfNxtLn:
                    # another keyword has been found before () number got equal, Cancel case
                    # only happens if Keyword is on next line. Not checking keywords on same line
                    return None
                    
            # check for ().
            index = 0
            while index < len(lines[nxtLnIndex]):
                if lines[nxtLnIndex][index] == '(':
                    openParenthNo += 1
                if lines[nxtLnIndex][index] == ')':
                    closeParenthNo += 1
                index += 1
            else:
                nxtLnIndex += 1
        else:
            # closeParenthNo = openParenthNo
            if openParenthNo == 0:
                return None
            return ParenthResult(False, nxtLnIndex, index - 2) #TODO: WHY is it -2. NO ONE WILL EVER KNOW
        return None


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


def handleKeyword(KEYWORD, line, lineIndex, lines, fileToEdit, currentLineIsComment, commentOfCurrentLine, isMultiline, keywordIndex):
    # found a  "KEYWORD"
    errorPrintData = (KEYWORD, (lineIndex + 1), fileToEdit.name)
    hasHash = checkForHash(lineIndex, lines)
    if hasHash != -1:
        # has hash
        print("hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
        return None
    # check for keyword
    # print(utils.hasKeyword(lineIndex, lines))
    # if utils.hasKeyword(lineIndex, lines) == True:
    #     print("keyword ignore: ignored for loop at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
    #     continue
    
    # we must now skip over all parentheses to find the end of the (condition)
    if KEYWORD == "else -":
        if line.find("if") != -1:
            # line is else if
            isElseIf = True
            checkParenthResult = checkForParentheses(line, lineIndex, lines)
        else:
            isElseIf = False
            checkParenthResult = ParenthResult(True, lineIndex, None)
    else:
        isElseIf = False
        checkParenthResult = checkForParentheses(line, lineIndex, lines)

    if checkParenthResult == None:
        print("keyword in parenth ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
        return None

    elif checkParenthResult.isOnSameLine == False:
        # doesnt end on same line
        isOnSameLine = checkParenthResult.isOnSameLine
        nxtLnIndex = checkParenthResult.lineIndex
        nextLineIndex = nxtLnIndex
        openCurlyBraceIndex = lines[nxtLnIndex - 1][checkParenthResult.lastCloseParenthIndex:].find("{")
        
        if not isElseIf and KEYWORD == "else -":
            lastCloseParenthRe = re.search(r"\b(else)\b", lines[nxtLnIndex - 1])
            if lastCloseParenthRe:
                lastCloseParenthIndex = lastCloseParenthRe.end()
            else:
                lastCloseParenthIndex = -1
        else:
            lastCloseParenthIndex = checkParenthResult.lastCloseParenthIndex + 1
            
    elif checkParenthResult.isOnSameLine == True:
        # ends on same line
        isOnSameLine = checkParenthResult.isOnSameLine
        nextLineIndex = lineIndex + 1
        openCurlyBraceIndex = line[checkParenthResult.lastCloseParenthIndex:].find("{")
        if not isElseIf and KEYWORD == "else -":
            lastCloseParenthRe = re.search(r"\b(else)\b", line)
            if lastCloseParenthRe:
                lastCloseParenthIndex = lastCloseParenthRe.end()
            else:
                lastCloseParenthIndex = -1
        else:
            lastCloseParenthIndex = checkParenthResult.lastCloseParenthIndex + 1
    
    if openCurlyBraceIndex == -1 and checkForOpenBrace(nextLineIndex, lines) == -1:
        
        # no { on same ln and on subsequent lines

        # check if it has stuff on same line
        # add brace
       
        if isOnSameLine:
            lastSemiColonIndex = line[lastCloseParenthIndex:].find(";")
            

            if not isElseIf and KEYWORD == "else -":

                if lastSemiColonIndex != -1:
                # semicolon found on same line
                    print("HERE IO")
                    print(lastCloseParenthIndex)
                    print(lastSemiColonIndex)
                    print(line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[lastCloseParenthIndex:]))])
                    if currentLineIsComment:
                        if isMultiline:
                            toAddLine = commentOfCurrentLine + line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n"
                        else:
                            toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):] + commentOfCurrentLine + "\n"
                    else:
                        toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n"
                    
                    del lines[lineIndex]
                    lines.insert(lineIndex, toAddLine)
                    return lines
                else:
                    if currentLineIsComment:
                        if isMultiline:
                            toAddLine = commentOfCurrentLine + line.rstrip() + " { " + "\n"
                        else:
                            toAddLine = line.rstrip() + " { " + commentOfCurrentLine + "\n"
                    else:
                        toAddLine = line.rstrip() + " {\n"

                    del lines[lineIndex]
                    lines.insert(lineIndex, toAddLine)
                    checkForSemiColonIndex = lineIndex + 1

            elif line[lastCloseParenthIndex:].isspace():

                if currentLineIsComment:
                    if isMultiline:
                        toAddLine = commentOfCurrentLine + line.rstrip() + " { " + "\n"
                    else:
                        toAddLine = line.rstrip() + " { " + commentOfCurrentLine + "\n"
                else:
                    toAddLine = line.rstrip() + " {\n"

                del lines[lineIndex]
                lines.insert(lineIndex, toAddLine)
                checkForSemiColonIndex = lineIndex + 1

            elif lastSemiColonIndex != -1:

                # semicolon found on same line

                if currentLineIsComment:
                    if isMultiline:
                        toAddLine = commentOfCurrentLine + line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n"
                    else:
                        toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):] + commentOfCurrentLine + "\n"
                else:
                    toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n" 

                del lines[lineIndex]
                lines.insert(lineIndex, toAddLine)
                return lines

            else:
                print("macro w/o brace or syntax error: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                return None
        else:
            if not isElseIf and KEYWORD == "else -":
                lastSemiColonIndex = lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";")
                if lastSemiColonIndex != -1:
                    nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)

                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + "\n"
                        else:
                            toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + nxtLnTrimComment.comment + "\n"
                    
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + " { " + lines[nxtLnIndex -1][lastCloseParenthIndex:].rstrip() + " }\n"
                    

                    hasHash = checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        print("hash ignore (later): ignored %s loop/ condition at %d in file %s" % errorPrintData)
                        return None
                
                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    return lines

                else:
                    nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)

                    if nxtLnTrimComment.hasComment: 
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line.rstrip() + " { " + "\n"
                        else:
                            toAddLine = nxtLnTrimComment.line.rstrip() + " { " + nxtLnTrimComment.comment + "\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1].rstrip() + " {\n"
                        
                    hasHash = checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        print("hash ignore (later): ignored %s loop/ condition at %d in file %s" % errorPrintData)
                        return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    checkForSemiColonIndex = nxtLnIndex

            elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace():
                
                nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                if nxtLnTrimComment.hasComment: 
                    if nxtLnTrimComment.isMultiline:
                        toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line.rstrip() + " { " + "\n"
                    else:
                        toAddLine = nxtLnTrimComment.line.rstrip() + " { " + nxtLnTrimComment.comment + "\n"
                else:
                    toAddLine = lines[nxtLnIndex - 1].rstrip() + " {\n"

                hasHash = checkForHash(nxtLnIndex - 1, lines)
                if hasHash != -1:
                    # has hash
                    print("hash ignore (later): ignored %s loop/ condition at %d in file %s" % errorPrintData)
                    return None

                del lines[nxtLnIndex - 1]
                lines.insert(nxtLnIndex - 1, toAddLine)
                checkForSemiColonIndex = nxtLnIndex

            elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1:
                nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                if nxtLnTrimComment.hasComment:
                    if nxtLnTrimComment.isMultiline:
                        toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + "\n"
                    else:
                        toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + nxtLnTrimComment.comment + "\n"
                else:
                   toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + " { " + lines[nxtLnIndex - 1][lastCloseParenthIndex:].rstrip() + " }\n"
                
                hasHash = checkForHash(nxtLnIndex - 1, lines)
                if hasHash != -1:
                    # has hash
                    print("hash ignore (later): ignored %s loop/ condition at %d in file %s" % errorPrintData)
                    return None

                del lines[nxtLnIndex - 1]
                lines.insert(nxtLnIndex - 1, toAddLine)
                return lines

            else:
                print("macro w/o brace or syntax error: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                return None

        # check for semicolons to add Closing brace
        closingBraceLineIndex = getNextSemiColonLine(checkForSemiColonIndex, lines) + 1

        # add closing braces at closingBraceLine (inserting a new ln) with indentation
        if isMultiline:
            spaces = " " * (keywordIndex + len(commentOfCurrentLine))

        else:
            spaces = " " * keywordIndex

        lines.insert(closingBraceLineIndex, "")
        addClosingBraceLine = spaces + "}\n"
        lines.insert(closingBraceLineIndex, addClosingBraceLine)
        return lines


if __name__ == "__main__":
    print("Do not run utilities!!!, run codeStyliser.py instead!")
    sys.exit()
