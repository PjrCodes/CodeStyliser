#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# Do not copy this code.
# check LICENSE for more details
# ---
# THE codeStyliser Utility
# ---
# Made in python 3.7.7 64 bit, use only this version
# ---
# utils.py
# utils for Codestyliser.py
# ---


#TODO: use logger
#TODO: use EXCEPTIONS in a SMARTER WAY!!!

import re
import sys

SINGLELINE_COMMENT_PATTERN = r"(\/\*[^\n]*)|(\/\/[^\n]*)"
OPENBRACE_PATTERN = r"^(\s*\{)|^(\{)"
KEYWORDS = [r'\b(for)\b', r'\b(while)\b', r'\b(do)\b', r'\b(switch)\b', r'\b(if)\b', r'\b(else)\b'] #TODO: convert into patterns

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


def checkForParentheses(line, lineIndex, lines, typeOfParenth):
    if typeOfParenth == "p":
        startingParenth = '('
        endingParenth = ')'
    if typeOfParenth == "b":
        startingParenth = '{'
        endingParenth = "}"
    openParenthNo = 0
    closeParenthNo = 0
    index = 0

    while index < len(line):
        if line[index] == startingParenth:
            openParenthNo += 1
        if line[index] == endingParenth:
            closeParenthNo += 1
        if openParenthNo == closeParenthNo and openParenthNo != 0:
            return ParenthResult(True, lineIndex, index)
        index += 1
        
    
    if openParenthNo != closeParenthNo:
        # the line doesnt have same amt of close and open parentheses
        # loop through till we reach same no. of parentheses.

        nxtLnIndex = lineIndex  + 1
        while closeParenthNo != openParenthNo:

            # check for ().
            index = 0
            while index < len(lines[nxtLnIndex]):
                if lines[nxtLnIndex][index] == startingParenth:
                    openParenthNo += 1
                if lines[nxtLnIndex][index] == endingParenth:
                    closeParenthNo += 1
                index += 1
            else:
                nxtLnIndex += 1
        else:
            # closeParenthNo = openParenthNo
            if openParenthNo == 0:
                return None
            # not on same line!!!
            # index is no. of characters seen, so cant return index.
            closeIndex = lines[nxtLnIndex].find(endingParenth)
            return ParenthResult(False, nxtLnIndex, closeIndex) 
        return None


def checkForOpenBrace(nextLineIndex, lines):

    while nextLineIndex < (len(lines)):
        lineWithoutComment = trimComment(lines[nextLineIndex], nextLineIndex, lines)

        if lineWithoutComment.hasComment:
            # line has comment
            if re.search(OPENBRACE_PATTERN, lineWithoutComment.line):
                # if the line before comment has {
                break
            if lineWithoutComment.isMultiline == True:
                # go after multiline comments
                nextLineIndex = lineWithoutComment.multiLineJumpIndex
                continue
            else:
                nextLineIndex = nextLineIndex + 1
                continue
        elif lineWithoutComment.line.isspace():
            # line is blank
            nextLineIndex += 1
            continue
        else:
            # line is not blank and isnt a comment
            break
    
    if re.search(OPENBRACE_PATTERN, lineWithoutComment.line):
        return (re.search(OPENBRACE_PATTERN, lineWithoutComment.line).end(), nextLineIndex)
    else:
        return (-1,None)

    

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

def getNextSemiColonLineIndex(index, lines):
    semiColonLineIndex = index
    while semiColonLineIndex < (len(lines)):
        lineWithoutComment = trimComment(lines[semiColonLineIndex], semiColonLineIndex, lines)
        if lineWithoutComment.isMultiline == True:
            semiColonIndex = lines[lineWithoutComment.multiLineJumpIndex].find(";")
        else:
            semiColonIndex = lineWithoutComment.line.find(";")
        if semiColonIndex == -1:
            # the line without Comment has NO semicolon
            semiColonLineIndex += 1
        else:
            # line has a semicolon and is NOT a comment
            break
    return semiColonLineIndex

def getClosingBraceLineIndex(index, lines):

    # run operations on line
    keywordLineCheckIndex = index
    hasKeyword = False
    while keywordLineCheckIndex < (len(lines)):

        currentLineWoComment = trimComment(lines[keywordLineCheckIndex], keywordLineCheckIndex, lines)
        line = currentLineWoComment.line

        firstCharOfLn = getFirstCharacterIndex(lines[keywordLineCheckIndex])
        if line.isspace():
            if currentLineWoComment.isMultiline:
                # jump line to after multiline comment
                keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                continue
            else:
                keywordLineCheckIndex += 1
                continue

        elif not line.isspace():
            if currentLineWoComment.hasComment:
                # we must check if current ln has keyword
                for keyword in KEYWORDS:
                    keywordCheckRe = re.search(keyword, line)
                    if  keywordCheckRe:
                        if keywordCheckRe.start() == firstCharOfLn:
                            # we found a keyword
                            cont = False
                            hasKeyword = True
                            break
                        else:
                            continue
                    else:
                        # didnt find KEYWORD
                        continue
                else:
                    # no keyword wasfound

                    if currentLineWoComment.isMultiline:
                        keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                        continue
                    else:
                        keywordLineCheckIndex += 1
                        continue
                
                if cont == True:
                    continue
                else:
                    break

            elif not currentLineWoComment.hasComment:

                for keyword in KEYWORDS:
                    keywordCheckRe = re.search(keyword, line)
                    if  keywordCheckRe:
                        if keywordCheckRe.start() == firstCharOfLn:
                            # we found a keyword
                            cont = False
                            hasKeyword = True
                            break
                        else:
                            cont = False
                            hasKeyword = False
                            continue
                    else:
                        # didnt find KEYWORD
                        cont = False
                        hasKeyword = False
                        continue
                    
                else:
                    # didnt find any keyword
                    keywordLineCheckIndex += 1

                if cont == True:
                    continue
                else:
                    break

    if hasKeyword == False:
        # didnt find a keyword
        return getNextSemiColonLineIndex(index, lines) + 1 # we found semicolon
    else:
        # here we reach only if it is KEYWORD found
        openCurlyBraceIndex = line.find("{")
        openNextLineCurlyBraceIndex = checkForOpenBrace(keywordLineCheckIndex + 1, lines)
        if openCurlyBraceIndex != -1 or openNextLineCurlyBraceIndex[0] != -1:
            # we found open curly brace related to this other keyword
            # we must go on to find the close }
            closeCurlyBraceIndex = line.find("}")
            if closeCurlyBraceIndex == -1:
                # run the code
                # search for matchin {}, 
                    # if match, return that line ki index.
                    # else, raise, DEATHERROR.
                if openCurlyBraceIndex == -1:
                    result = checkForParentheses(lines[openNextLineCurlyBraceIndex[1]], openNextLineCurlyBraceIndex[1], lines, typeOfParenth="b")
                else:
                    result = checkForParentheses(lines[keywordLineCheckIndex], keywordLineCheckIndex, lines, typeOfParenth="b")
                if result == None:
                    
                    return None
                else:
                    return result.lineIndex
            else:
                # same line has the thingy
                return getNextSemiColonLineIndex(keywordLineCheckIndex, lines) + 1
        else:
            # we didnt find it.
            # we must return semicolon index again!
            return getNextSemiColonLineIndex(keywordLineCheckIndex, lines) + 1

def handleKeyword(KEYWORD, line, lineIndex, lines, fileToEdit, isMacro, currentLineIsComment, commentOfCurrentLine, isMultiline, keywordIndex):
    # found a  "KEYWORD"
    errorPrintData = (KEYWORD, (lineIndex + 1), fileToEdit.name)
    hasHash = checkForHash(lineIndex, lines)
    if hasHash != -1:
        # has hash
        if line.find("{") != -1:
            # has {
            return None
        else:
            print("WARN: Hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
        return None
    
    # we must now skip over all parentheses to find the end of the (condition)
    if KEYWORD == "else -":
        if line.find("if") != -1:
            # line is else if
            isElseIf = True
            checkParenthResult = checkForParentheses(line, lineIndex, lines, "p")
        else:
            isElseIf = False
            checkParenthResult = ParenthResult(True, lineIndex, None)
    else:
        isElseIf = False
        checkParenthResult = checkForParentheses(line, lineIndex, lines, "p")

    if checkParenthResult == None:
        print("WARN: Keyword in parentheses ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
        return None

    elif not checkParenthResult.isOnSameLine:
        # (condition) doesnt end on same line
        isOnSameLine = checkParenthResult.isOnSameLine
        nxtLnIndex = checkParenthResult.lineIndex
        nextLineIndex = nxtLnIndex
        openCurlyBraceIndex = lines[nxtLnIndex - 1][checkParenthResult.lastCloseParenthIndex:].find("{")
        
        if not isElseIf and KEYWORD == "else -":
            lastCloseParenthIndex = 0
        else:
            lastCloseParenthIndex = checkParenthResult.lastCloseParenthIndex + 2
            
    else:
        # (condition) ends on same line
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
    

    if openCurlyBraceIndex == -1 and checkForOpenBrace(nextLineIndex, lines)[0] == -1:
        
        # no { on same line and on subsequent lines, we must add {} if possible        

        if isOnSameLine:
            lastSemiColonIndex = line[lastCloseParenthIndex:].find(";")
            isBackSlashPresent = line.rstrip()[-1] == "\\"
            if isBackSlashPresent:
                # backSLASH!
                if lastSemiColonIndex != -1:
                    # semicolon found on same line

                    if currentLineIsComment:
                        if isMultiline:
                            toAddLine = commentOfCurrentLine + line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n"
                        else:
                            toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):] + commentOfCurrentLine + "\n"
                    else:
                        toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1)] + " } " + line[(lastSemiColonIndex+len(line[:lastCloseParenthIndex])+1):].rstrip() + "\n" 

                    # insert toAddLine and return
                    del lines[lineIndex]
                    lines.insert(lineIndex, toAddLine)
                    return lines
                elif lastSemiColonIndex == -1:
                    if currentLineIsComment:
                        if isMultiline:
                            toAddLine = commentOfCurrentLine + line.rstrip()[:-1] + " { \\" + "\n"
                        else:
                            toAddLine = line.rstrip() + " { " + commentOfCurrentLine + "\\\n"
                    else:
                        toAddLine = line.rstrip()[:-1] + " { \\\n"
                    del lines[lineIndex]
                    lines.insert(lineIndex, toAddLine)
                    checkForSemiColonIndex = lineIndex + 1
                else:
                    print("err")

            elif not isBackSlashPresent:
        
                if line[lastCloseParenthIndex:].isspace():
                    # if there is nothing on line except the keyword()
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

                    # insert toAddLine and return
                    del lines[lineIndex]
                    lines.insert(lineIndex, toAddLine)
                    return lines
                else:
                    print("err")
            else:
                print("WARN: syntax Loop/condition in macro has no brace OR a Syntax error: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                return None
        else:
            # the (condition) doesnt end on same line
            isBackSlashPresent = lines[nxtLnIndex - 1].rstrip()[-1] == "\\"
            lastSemiColonIndex = lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";")
            if isBackSlashPresent:
                if lastSemiColonIndex != -1:
                    # same line semicolon
                    nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)

                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip()[:-1] + " } " + "\\\n"
                        else:
                            toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + nxtLnTrimComment.comment + "\\\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + " { " + lines[nxtLnIndex - 1][lastCloseParenthIndex:].rstrip()[:-1] + " } \\\n"
                    
                    hasHash = checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    return lines

                elif lastSemiColonIndex == -1:
                    nxtLnTrimComment = trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                    
                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line.rstrip()[:-1] + " { " + "\\\n"
                        else:
                            toAddLine = nxtLnTrimComment.line.rstrip() + " { " + nxtLnTrimComment.comment + "\\\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1].rstrip()[:-1] + " { \\\n"

                    hasHash = checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    checkForSemiColonIndex = nxtLnIndex
                else:
                    print("errNOTLINE")
            elif not isBackSlashPresent:
                if lines[nxtLnIndex - 2].rstrip()[-1] == "\\":
                    return None
                if lastSemiColonIndex == -1:
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
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    checkForSemiColonIndex = nxtLnIndex

                elif lastSemiColonIndex != -1:
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
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Hash ignore: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    return lines
                else:
                    print("errNXTLINE")
                    return None
            else:
                print("WARN: syntax - Loop/condition in a macro has no brace OR a Syntax error: ignored %s loop/ condition at %d in file %s" % errorPrintData)
                return None



        closingBraceLineIndex = getClosingBraceLineIndex(checkForSemiColonIndex, lines)
        if closingBraceLineIndex == None:
            print("FATAL ERROR: ignored %s loop/ condition at %d in file %s" % errorPrintData)
            return None
        else:
            # add closing braces at closingBraceLine (inserting a new ln) with indentation
            if isMultiline:
                spaces = " " * (keywordIndex + len(commentOfCurrentLine))
            else:
                spaces = " " * keywordIndex

            if lines[closingBraceLineIndex - 1].rstrip()[-1] == "\\":
                # we found \
                addClosingBraceLine = spaces + "} \\\n"
            elif lines[closingBraceLineIndex - 1].rstrip()[-1] != "\\":
                if lines[closingBraceLineIndex - 2].rstrip()[-1] == "\\":
                    toAddBackSlash = lines[closingBraceLineIndex - 1].rstrip() + " \\\n"
                    del lines[closingBraceLineIndex - 1]
                    lines.insert(closingBraceLineIndex - 1, toAddBackSlash)        
                
                addClosingBraceLine = spaces + "}\n"
            
            lines.insert(closingBraceLineIndex, "")
            lines.insert(closingBraceLineIndex, addClosingBraceLine)
            return lines



if __name__ == "__main__":
    print("Do not run utilities!!!, run codeStyliser.py instead!")
    sys.exit()
