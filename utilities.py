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
# utilities.py
# utility functions for the codeStyliser utility
# ---


#TODO: use logger
#TODO: use EXCEPTIONS in a SMARTER WAY!!!

#HACK:FIXME: EVERYTHING IS A HACK!!!

import re
import sys
import exceptions
import models
import constants as consts


def trimComment(line, lineNo, lines):
    searchForSingleLineComment = re.search(consts.SINGLELINE_COMMENT_PATTERN, line)
    if (searchForSingleLineComment):
        if searchForSingleLineComment.group()[0:2] == "/*":
            # keep searching for */
            sameLineEnd = line.find("*/")
            if sameLineEnd != -1:
                # ends on same line
                #TODO: ALSO CHECK IF THERE IS ANYTHING ON THE LINE AFTER THE COMMENT, IN WHICH CASE WE NEED TO DIE
                #FIXME: THIS WILL FAIL IF THERE IS SOMETHING AFTER COMMENT
                #BUG: THIS IS A BUG AS IT CAUSES AN ERROR IN COMMENT HANDLING, AND PARENTHESES COUNTING, RAISING INDEX ERROR's
                # comment = searchForSingleLineComment.group()
                return models.LineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
            else:
                # iterate for line in lines till we get */
                index = lineNo + 1
                while True:
                    multiCommentEnd = lines[index].find("*/")
                    if multiCommentEnd != -1:
                        # multi line comment has ended
                        return models.LineWithComment(lines[index][(multiCommentEnd + 2):],True, lines[index][:(multiCommentEnd+2)] ,True, index)
                    else:
                        # no multi line comment end found
                        index = index + 1
                    
        # found a single line comment of type //
        return models.LineWithComment(line[:searchForSingleLineComment.start()], True, searchForSingleLineComment.group(),False, None)
    else:
        # no comment
        return models.LineWithComment(line, False, "", False, None)


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
            return models.ParenthResult(True, lineIndex, index)
        index += 1
        
    
    if openParenthNo != closeParenthNo:
        # the line doesnt have same amt of close and open parentheses
        # loop through till we reach same no. of parentheses.

        nxtLnIndex = lineIndex  + 1
        while closeParenthNo != openParenthNo:
            if nxtLnIndex > (len(lines) - 1):
                # we never found a parentheses match!
                # this can only happen if there is syntax error, which there isnt.
                # We have already ignored Macros where this can happen
                # so, we must HAVE HIT A COMMENT!
                raise exceptions.CommentError
            # check for {} on the line
            for char in lines[nxtLnIndex]:
                if char == startingParenth:
                    openParenthNo += 1
                elif char == endingParenth:
                    closeParenthNo += 1
            else:
                # after iterating through line
                nxtLnIndex += 1
        else:
            # closeParenthNo = openParenthNo
            if openParenthNo == 0:
                return None
            # not on same line!!!
            # index is no. of characters seen, so cant return index.
            closeIndex = lines[nxtLnIndex - 1].find(endingParenth)
            return models.ParenthResult(False, nxtLnIndex, closeIndex) 
        return None


def checkForOpenBrace(nextLineIndex, lines):

    while nextLineIndex < (len(lines)):
        lineWithoutComment = trimComment(lines[nextLineIndex], nextLineIndex, lines)
        if lineWithoutComment.hasComment:
            # line has comment
            if lineWithoutComment.line.isspace():
                nextLineIndex += 1
                continue
            else:
                if re.search(consts.OPENBRACE_PATTERN, lineWithoutComment.line):
                    # if the line before comment has {
                    break
                else:
                    # there is something before line, but it is not an open brace
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
    
    if re.search(consts.OPENBRACE_PATTERN, lineWithoutComment.line):
        return (re.search(consts.OPENBRACE_PATTERN, lineWithoutComment.line).end(), nextLineIndex)
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
            semiColonIndex = lineWithoutComment.line.find(";")
            semiColonLineIndex = lineWithoutComment.multiLineJumpIndex
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
        firstCharOfLn = getFirstCharacterIndex(line)
        if line.isspace() or len(line) == 0:
            if currentLineWoComment.isMultiline:
                # jump line to after multiline comment
                keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                continue
            else:
                keywordLineCheckIndex += 1
                continue
        else:
            
            if currentLineWoComment.hasComment:
                if currentLineWoComment.isMultiline:
                    for keyword in consts.KEYWORDS:
                        keywordCheckRe = re.search(keyword, line)
                        if  keywordCheckRe:
                            if keywordCheckRe.start() == firstCharOfLn:
                                # we found a keyword
                                cont = False
                                hasKeyword = True
                                break
                            else:
                                # keyword not on first char
                                hasKeyword = False
                                continue
                        else:
                            # didnt find KEYWORD
                            hasKeyword = False
                            continue
                    if cont == True:
                        continue
                    else:
                        keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                        break
                    keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                    continue

                if currentLineWoComment.line.isspace():
                    continue
                else:
                    if line.find("*/") != -1:
                        keywordLineCheckIndex += 1
                    for keyword in consts.KEYWORDS:
                        keywordCheckRe = re.search(keyword, line)
                        if  keywordCheckRe:
                            if keywordCheckRe.start() == firstCharOfLn:
                                # we found a keyword
                                cont = False
                                hasKeyword = True
                                break
                            else:
                                # keyword not on first char
                                hasKeyword = False
                                continue
                        else:
                            # didnt find KEYWORD
                            hasKeyword = False
                            continue
                    else:
                        # no keyword was found or line is a statement
                       
                        if currentLineWoComment.line.isspace() or len(currentLineWoComment.line) == 0:
                            if currentLineWoComment.isMultiline:
                                keywordLineCheckIndex = currentLineWoComment.multiLineJumpIndex
                                continue
                            else:
                                keywordLineCheckIndex += 1
                                continue
                        else:
                            
                            hasKeyword = False
                            cont = False
                            break
                    
                if cont == True:
                    continue
                else:
                    break

            elif not currentLineWoComment.hasComment:
                
                if line.find("*/") != -1:
                    keywordLineCheckIndex += 1
                line = lines[keywordLineCheckIndex]
                if line.isspace():
                    continue
                else:
                    for keyword in consts.KEYWORDS:
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
                        hasKeyword = False

                    if cont == True:
                        continue
                    else:
                        break
            

    if hasKeyword == False:
        # didnt find a keyword
        return getNextSemiColonLineIndex(index, lines) + 1 # we found semicolon
    else:
        # here we reach only if it is KEYWORD found
        if keyword == r"\b(else)\b" or keyword == r"\b(do)\b":
            if line.find("if") != -1:
                # line is else if
                checkParenthResult = checkForParentheses(line, keywordLineCheckIndex, lines, "p")
            else:
                checkParenthResult = models.ParenthResult(True, keywordLineCheckIndex, None)
        else:
            checkParenthResult = checkForParentheses(line, keywordLineCheckIndex, lines, "p")
        if checkParenthResult == None:
            return None

        elif not checkParenthResult.isOnSameLine:
            # (condition) doesnt end on same line
            nxtLnIndex = checkParenthResult.lineIndex
            nextLineIndex = nxtLnIndex
            openCurlyBraceIndex = lines[nxtLnIndex - 1][checkParenthResult.lastCloseParenthIndex:].find("{")
            
        else:
            # (condition) ends on same line
            nextLineIndex = keywordLineCheckIndex + 1
            nxtLnIndex = keywordLineCheckIndex + 1
            openCurlyBraceIndex = line[checkParenthResult.lastCloseParenthIndex:].find("{")


        # dont touch me!
        openNextLineCurlyBraceIndex = checkForOpenBrace(nextLineIndex, lines)
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
                    result = checkForParentheses(lines[nxtLnIndex - 1], nxtLnIndex - 1, lines, typeOfParenth="b")
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
