#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# This code cannot be copied. Violators will be prosecuted.
# ---
# code styliser program
# ---
# Made in python 3.7.7 64 bit, use only this version
# ---
# codeStyliser.py
# code Styliser, starting point
# ---
# DO NOT RE-DISTRIBUTE

import sys
import re
import os
import utilities as utils
import time
# TODO: use logger


def styliseCode(fileToEdit):
    # lines edited in this file
    linesEdited = 0
    # so that first line's index is 0

    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    lineIndex = -1
    while lineIndex < (len(lines) - 1):

        # try:
            # increment line count
            lineIndex = lineIndex + 1
            # current line
            line = lines[lineIndex]
            # print(str(lineIndex) + "\t" + line, end="")
            currentLineIsComment = False

            firstCharIndex = utils.getFirstCharacterIndex(line)

            # search for comments
            trimmedCommentResult = utils.trimComment(line, lineIndex, lines)
            line = trimmedCommentResult.line

            # print(str(lineIndex) + "@@@" + fileToEdit.name + "\t" + line)

            if trimmedCommentResult.hasComment == True and trimmedCommentResult.isMultiline == False:
                currentLineIsComment = True
                commentOfCurrentLine = trimmedCommentResult.comment
            elif trimmedCommentResult.isMultiline == True:
                currentLineIsComment = trimmedCommentResult.hasComment
                commentOfCurrentLine = trimmedCommentResult.comment
                # if comment, jump
                lineIndex = trimmedCommentResult.multiLineJumpIndex
            elif trimmedCommentResult.hasComment == False:
                currentLineIsComment = False
                commentOfCurrentLine = trimmedCommentResult.comment
            else:
                print("FATAL error in comment checking, at line " +
                    str(lineIndex) + " file: " + fileToEdit.name)

            # ---------------------------------------------------------------------------
            # find for loops
            forLoopIndex = line.find("for")
            if forLoopIndex == firstCharIndex:
                forLoopHandler = utils.handleKeyword(KEYWORD="for", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=forLoopIndex)
                if forLoopHandler == None:
                    continue
                else:
                    lines = forLoopHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------

            # find while loops
            whileLoopIndex = line.find("while")
            if whileLoopIndex == firstCharIndex:
                whileLoopHandler = utils.handleKeyword(KEYWORD="while", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=whileLoopIndex)
                if whileLoopHandler == None:
                    continue
                else:
                    lines = whileLoopHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------

            # find if conditions
            ifConditionIndex = line.find("if")
            if ifConditionIndex == firstCharIndex:
                ifConditionHandler = utils.handleKeyword(KEYWORD="if", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=ifConditionIndex)
                if ifConditionHandler == None:
                    continue
                else:
                    lines = ifConditionHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------
            # find else conditions
            startingCurlyBraceIndex = line.find("}")
            startingAtElseIndex = line.find("else")
            lineStartsOnBrace = False
            if startingCurlyBraceIndex == firstCharIndex:
                # line starts on a }
                lineStartsOnBrace = True
            if (lineStartsOnBrace and line[startingCurlyBraceIndex:].find("else") != -1) or (startingAtElseIndex == firstCharIndex and lineStartsOnBrace == False):
                # we have a line with an } and an else after it
                # process else

                # we must now skip over all parentheses to find the end of the (condition)
                hasHash = utils.checkForHash(lineIndex, lines)
                isElseIf = False
                if hasHash != -1:
                    # has hash
                    print("hash ignore: ignored else/ else if at " +
                        str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # check for keyword
                # print(utils.hasKeyword(lineIndex, lines))
                # if utils.hasKeyword(lineIndex, lines) == True:
                #     print("keyword ignore: ignored else/ else if at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                #     continue
                if line.find("if") != -1:
                    # line is else if
                    isElseIf = True
                    checkParenthResult = utils.checkForParentheses(
                        line, lineIndex, lines)
                else:
                    # no need to call checkForParentheses
                    isElseIf = False
                    checkParenthResult = (True,)

                if checkParenthResult == None:
                    print("keyword in parenth ignore: ignored else/ else if at " +
                        str(lineIndex+1) + " in file " + fileToEdit.name)
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                    if isElseIf:
                        lastCloseParenthIndex = lines[nxtLnIndex -
                                                    1].rfind(")") + 1
                    else:
                        lastCloseParenthIndex = lines[nxtLnIndex -
                                                    1].rfind("e") + 1
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                    if isElseIf:
                        lastCloseParenthIndex = line.rfind(")") + 1
                    else:
                        lastCloseParenthIndex = line.rfind("e") + 1

                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln or on subsequent lines
                    # add open CURLY on same line
                    linesEdited = linesEdited + 1
                    if isOnSameLine:
                        if line[lastCloseParenthIndex:].isspace() and isElseIf:
                            if currentLineIsComment:
                                toAddLine = line.rstrip() + \
                                    " { " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line.rstrip() + " {\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            checkForSemiColonIndex = lineIndex + 1
                        elif line[lastCloseParenthIndex:].find(";") != -1 and isElseIf:
                            # add braces around {}
                            if currentLineIsComment:
                                toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:].rstrip(
                                ) + " } " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line[:lastCloseParenthIndex] + \
                                    " { " + \
                                    line[lastCloseParenthIndex:].rstrip() + " }\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            continue
                        elif not isElseIf:
                            # add braces around {}
                            lastSemiColonIndex = line.rfind(";")
                            if lastSemiColonIndex != -1:
                            # semicolon found on same line
                            # not an else if
                                if currentLineIsComment:
                                    toAddLine = line[:lastCloseParenthIndex] + " { " + line[lastCloseParenthIndex:].rstrip(
                                    ) + " } " + commentOfCurrentLine + "\n"
                                else:
                                    toAddLine = line[:lastCloseParenthIndex] + \
                                        " { " + \
                                        line[lastCloseParenthIndex:].rstrip() + \
                                        " }\n"
                                del lines[lineIndex]
                                lines.insert(lineIndex, toAddLine)
                                continue
                            else:
                                if currentLineIsComment:
                                    toAddLine = line.rstrip() + \
                                        " { " + commentOfCurrentLine + "\n"
                                else:
                                    toAddLine = line.rstrip() + " {\n"
                                del lines[lineIndex]
                                lines.insert(lineIndex, toAddLine)
                                checkForSemiColonIndex = lineIndex + 1
                        else:
                            print("macro w/o brace or syntatical error in else IF/ else condition in " +
                                fileToEdit.name + " at line " + str(lineIndex))
                            linesEdited = linesEdited - 1
                            continue
                    else:
                        if lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace() and isElseIf:
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line.rstrip() + \
                                    " { " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1].rstrip() + " {\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            checkForSemiColonIndex = nxtLnIndex
                        elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1 and isElseIf:
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip(
                                ) + " } " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + \
                                    " { " + lines[nxtLnIndex -
                                                1][lastCloseParenthIndex:].rstrip() + " }\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            continue
                        elif not isElseIf:
                            lastSemiColonIndex = line.rfind(";")
                            if lastSemiColonIndex != -1:
                                nxtLnTrimComment = utils.trimComment(
                                    lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                                if nxtLnTrimComment.hasComment:
                                    toAddLine = nxtLnTrimComment.line[:lastCloseParenthIndex] + " { " + nxtLnTrimComment.line[lastCloseParenthIndex:].rstrip(
                                    ) + " } " + nxtLnTrimComment.comment + "\n"
                                else:
                                    toAddLine = lines[nxtLnIndex - 1][:lastCloseParenthIndex] + \
                                        " { " + lines[nxtLnIndex -
                                                    1][lastCloseParenthIndex:].rstrip() + " }\n"
                                del lines[nxtLnIndex - 1]
                                lines.insert(nxtLnIndex - 1, toAddLine)
                                continue
                            else:
                                nxtLnTrimComment = utils.trimComment(
                                    lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                                if nxtLnTrimComment.hasComment:
                                    toAddLine = nxtLnTrimComment.line.rstrip() + \
                                        " { " + nxtLnTrimComment.comment + "\n"
                                else:
                                    toAddLine = lines[nxtLnIndex -
                                                    1].rstrip() + " {\n"
                                del lines[nxtLnIndex - 1]
                                lines.insert(nxtLnIndex - 1, toAddLine)
                                checkForSemiColonIndex = nxtLnIndex
                        else:
                            print("macro w/o brace or syntatical error in else if/ else condition in " +
                                fileToEdit.name + " at line " + str(lineIndex))
                            linesEdited = linesEdited - 1
                            continue
                    # check for closng brace

                    closingBraceLineIndex = utils.getNextSemiColonLine(
                        checkForSemiColonIndex, lines) + 1
                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    if lineStartsOnBrace:
                        spaces = " " * startingCurlyBraceIndex
                    elif not lineStartsOnBrace:
                        spaces = " " * startingAtElseIndex
                    lines.insert(closingBraceLineIndex, "\n")
                    addClosingBraceLine = lines[closingBraceLineIndex].rstrip(
                    ) + spaces + "}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

            # ---------------------------------------------------------------------------

        # except:
        #     e = sys.exc_info()[0]
        #     print("runtime error: " + str(e) + " in file name: " +
        #           fileToEdit.name + " around line " + str(lineIndex + 1), end = "")
        #     print(", Most likely a syntax error in the C file.")
        #     continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()
    return linesEdited


def main():
    VERSION_NUMBER = "0.1.9.2-alpha"
    NEW_CHANGES = "slight refactor"
    KNOWN_BUGS = """
    \t\terr 2: MACRO-error:  } added after \\
    \t\terr 3: SAME-LINE-PARENTHESES-error: {} added after last ) but must be added after (condition) parentheses
    \t\terr 5: KEYWORD-error: # error, mustnt add {} if next line after curlyBraceIndexLine has a Preprocesser
    \t\terr 7: PARENTH_AFTER_FOR_error: even if parenth are not immedieatly after, it gives error
    \t\terr 6: FUNCTION-error: after function ended, we see some lines added, something to do with double line if
    \t\t\t (VERY WEIRD ERROR!!)
    \t\terr N-1: If no endline at end of file, } is added on same line as the last ;
    \t\terr PREPROCESSER: if there is #if or #endif, ignore that condition/ loop
    \t\terr PARENTH_IMMEDIATE: not checking if the parentheses are immediately after for, causing detection of func declarations.
    \t\terr DOUBLE-COMMENT: if there are two comments on same line, one multiline end and one single line, desired result is not achieved, asd*/ for() as;//ads
    \t\terr DETECTION-ERROR: if the keyword is part of something else and it has (), it is detected as keyword, forall() as;
    \t\terr SEMICOLON-DETECTOR: some kind of error, please check, very weird, cant repro
    \t\t\t (VERY WEIRD ERROR!!)
    \t\t ONLY 11 ERRORS
    """
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'

    if (len(sys.argv) != 2):
        print("Usage: python3.7 codeStyliser.py <DIRECTORY_NAME>")
        print("DIRECTORY_NAME IS REQUIRED")
        sys.exit()
    else:
        DIR_NAME = sys.argv[1]
        fileNo = 0
        linesEdited = 0
        print("Welcome to CodeStyliser ver" + VERSION_NUMBER)
        print("\twith changes: " + NEW_CHANGES)
        print("\tand with the BEST INSECTS: " + KNOWN_BUGS)
        print("Made by Pranjal Rastogi, for and in Python 3.7.7 64Bit")
        print("Will fix (.c) code for files under " + DIR_NAME)
        print("you have three seconds to read the above data")
        time.sleep(3)
        print("\n\n")

        print("===== STARTING... =====")
        for root, subdirs, files in os.walk(DIR_NAME):

            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".", 1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c":
                    print ("writing ...", end="\r", flush=True)
                    time.sleep(0.2)
                    fileNo = fileNo + 1
                    try:
                        with open(file_path, 'rb') as open_file:
                            content = open_file.read()
                            content = content.replace(
                                WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
                        with open(file_path, 'wb') as open_file:
                            open_file.write(content)
                            open_file.close()
                    except:
                        e = sys.exc_info()[0]
                        print("runtime error: " + str(e) + " at file name: " +
                              filename + " while changing line endings")
                        continue
                    # try:
                    with open(file_path, "r+") as fileToStyle:
                        linesEdited = styliseCode(fileToStyle) + linesEdited
                    # except:
                    #     e = sys.exc_info()[0]
                    #     print("runtime error: " + str(e) + " at file name: " +
                    #           filename + " while opening file")
                    #     continue
                else:
                    continue
        print("\n")
        print("======= SUMMARY =======")
        print("Added braces " + str(linesEdited) +
              " times in " + str(fileNo) + " files")
        print("======== ENDED ========")


if __name__ == "__main__":
    main()
