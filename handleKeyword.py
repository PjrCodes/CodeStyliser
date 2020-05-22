#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, use only this version
# ---
# Copyright (c) 2020, Pranjal Rastogi 
# All rights reserved.
# Do not copy this code without permission
# check LICENSE for more details
# ---
# Part of The codeStyliser utility
# ---
# handleKeyword.py
# The brain for Codestyliser.py
# ---

import utilities as utils
import re
import models

def handleKeyword(keyword, line, lineIndex, lines, fileToEdit, isMacro, currentLineIsComment, commentOfCurrentLine, isMultiline, keywordIndex):
    # found a  "KEYWORD"
    errorPrintData = (keyword, (lineIndex + 1), fileToEdit.name)
    hasHash = utils.checkForHash(lineIndex, lines)
    if hasHash != -1:
        # has hash
        if line.find("{") != -1:
            # has {
            return None
        else:
            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % errorPrintData)
        return None
    
    # we must now skip over all parentheses to find the end of the (condition)
    if keyword == "else -":
        if line.find("if") != -1:
            # line is else if
            isElseIf = True
            checkParenthResult = utils.checkForParentheses(line, lineIndex, lines, "p")
        else:
            isElseIf = False
            checkParenthResult = models.ParenthResult(True, lineIndex, None)
    else:
        isElseIf = False
        checkParenthResult = utils.checkForParentheses(line, lineIndex, lines, "p")

    if checkParenthResult == None:
        print("ERROR: While checking parentheses: ignored %s loop/ condition at %d in file %s" % errorPrintData)
        return None

    elif not checkParenthResult.isOnSameLine:
        # (condition) doesnt end on same line
        isOnSameLine = checkParenthResult.isOnSameLine
        nxtLnIndex = checkParenthResult.lineIndex
        nextLineIndex = nxtLnIndex
        openCurlyBraceIndex = lines[nxtLnIndex - 1][checkParenthResult.lastCloseParenthIndex:].find("{")
        if not isElseIf and keyword == "else -":
            lastCloseParenthIndex = 0
        else:
            lastCloseParenthIndex = checkParenthResult.lastCloseParenthIndex + 2
            
    else:
        # (condition) ends on same line
        isOnSameLine = checkParenthResult.isOnSameLine
        nextLineIndex = lineIndex + 1
        openCurlyBraceIndex = line[checkParenthResult.lastCloseParenthIndex:].find("{")
        if not isElseIf and keyword == "else -":
            lastCloseParenthRe = re.search(r"\b(else)\b", line)
            if lastCloseParenthRe:
                lastCloseParenthIndex = lastCloseParenthRe.end()
            else:
                lastCloseParenthIndex = -1
        else:
            lastCloseParenthIndex = checkParenthResult.lastCloseParenthIndex + 1
    

    if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines)[0] == -1:
        
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
                    return None

            elif not isBackSlashPresent:
                if lines[lineIndex - 2].isspace() or len(lines[lineIndex-2]) == 0:
                    pass
                else:
                    if lines[lineIndex - 2].rstrip()[-1] == "\\":
                        if lastSemiColonIndex == -1:
                            # not semicolon ending
                            return None
                if lastSemiColonIndex == -1:
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
                    return None
            else:
                return None
        else:
            # the (condition) doesnt end on same line
            isBackSlashPresent = lines[nxtLnIndex - 1].rstrip()[-1] == "\\"
            lastSemiColonIndex = lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";")
            if isBackSlashPresent:
                
                if lastSemiColonIndex != -1:
                    # same line semicolon
                    nxtLnTrimComment = utils.trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)

                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip()[:-1] + " } " + "\\\n"
                        else:
                            toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + nxtLnTrimComment.comment + "\\\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + " { " + lines[nxtLnIndex - 1][lastCloseParenthIndex:].rstrip()[:-1] + " } \\\n"
                    
                    hasHash = utils.checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    return lines

                elif lastSemiColonIndex == -1:
                    nxtLnTrimComment = utils.trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                    
                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line.rstrip()[:-1] + " { " + "\\\n"
                        else:
                            toAddLine = nxtLnTrimComment.line.rstrip() + " { " + nxtLnTrimComment.comment + "\\\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1].rstrip()[:-1] + " { \\\n"

                    hasHash = utils.checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    checkForSemiColonIndex = nxtLnIndex
            elif not isBackSlashPresent:
                
                if lines[nxtLnIndex - 2].isspace() or len(lines[nxtLnIndex-2]) == 0:
                    pass
                else:
                    if lines[nxtLnIndex - 2].rstrip()[-1] == "\\":
                        if lastSemiColonIndex == -1:
                            # not semicolon ending
                            return None
                
                if lastSemiColonIndex == -1:
                    nxtLnTrimComment = utils.trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                    
                    if nxtLnTrimComment.hasComment: 
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line.rstrip() + " { " + "\n"
                        else:
                            toAddLine = nxtLnTrimComment.line.rstrip() + " { " + nxtLnTrimComment.comment + "\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1].rstrip() + " {\n"

                    hasHash = utils.checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    checkForSemiColonIndex = nxtLnIndex

                elif lastSemiColonIndex != -1:
                    nxtLnTrimComment = utils.trimComment(lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                    
                    if nxtLnTrimComment.hasComment:
                        if nxtLnTrimComment.isMultiline:
                            toAddLine = nxtLnTrimComment.comment + nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + "\n"
                        else:
                            toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip() + " } " + nxtLnTrimComment.comment + "\n"
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + " { " + lines[nxtLnIndex - 1][lastCloseParenthIndex:].rstrip() + " }\n"
                    
                    hasHash = utils.checkForHash(nxtLnIndex - 1, lines)
                    if hasHash != -1:
                        # has hash
                        if lines[nxtLnIndex - 1].find("{") != -1:
                            # has {
                            return None
                        else:
                            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % errorPrintData)
                            return None

                    del lines[nxtLnIndex - 1]
                    lines.insert(nxtLnIndex - 1, toAddLine)
                    return lines
                else:
                    return None
            else:
                return None


        closingBraceLineIndex = utils.getClosingBraceLineIndex(checkForSemiColonIndex, lines)
        if closingBraceLineIndex == None:
            print("FATAL ERROR: ignored %s loop/ condition at %d in file %s" % errorPrintData)
            return None
        else:
            # add closing braces at closingBraceLine (inserting a new ln) with indentation
            if isMultiline:
                spaces = " " * (keywordIndex + len(commentOfCurrentLine))
            else:
                spaces = " " * keywordIndex
            if len(lines[closingBraceLineIndex - 1].strip()) == 0 or len(lines[closingBraceLineIndex - 2].strip()) == 0:
                addClosingBraceLine = spaces + "}\n"
                pass
            else:
                if lines[closingBraceLineIndex - 1].rstrip()[-1] == "\\":
                    # we found \
                    addClosingBraceLine = spaces + "} \\\n"
                elif lines[closingBraceLineIndex - 2].rstrip()[-1] == "\\":
                    toAddBackSlash = lines[closingBraceLineIndex - 1].rstrip() + " \\\n"
                    del lines[closingBraceLineIndex - 1]
                    lines.insert(closingBraceLineIndex - 1, toAddBackSlash)
                    addClosingBraceLine = spaces + "}\n"        
                else:
                    addClosingBraceLine = spaces + "}\n"
            
            lines.insert(closingBraceLineIndex, "")
            lines.insert(closingBraceLineIndex, addClosingBraceLine)
            return lines
