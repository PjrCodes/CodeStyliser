# Copyright (c) 2020 Pranjal Rastogi
#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, please use only this version
# code Styliser- run this file

import sys
import re
import os
import utils as utils
import time

def styliseCode(fileToEdit):
    linesEdited = 0
    # so that first line's index is 0
    lineIndex = -1
    
    fileToEdit.seek(0)
    lines = fileToEdit.readlines()

    while lineIndex < (len(lines) - 1):

        try:
            lineIndex = lineIndex + 1
            line = lines[lineIndex]
            currentLineIsComment = False
            firstCharIndex = utils.getFirstCharacterIndex(line)


            # search for comments
            trimmedCommentResult = utils.trimComment(line, lineIndex, lines)
            line = trimmedCommentResult.line
            if trimmedCommentResult.hasComment == True and trimmedCommentResult.isMultiline == False:
                currentLineIsComment = True
                commentOfCurrentLine = trimmedCommentResult.comment
            elif trimmedCommentResult.isMultiline == True:
                currentLineIsComment = trimmedCommentResult.hasComment
                commentOfCurrentLine = "" #TODO: change
                # if comment, jump
                line = trimmedCommentResult.line
                lineIndex = trimmedCommentResult.multiLineJumpIndex + 1

            # ---------------------------------------------------------------------------

            # find for loops
            forLoopIndex = line.find("for")
            if forLoopIndex == firstCharIndex:
                # found a for loop
                hasHash = utils.checkForHash(lineIndex, lines)
                if hasHash != -1:
                    # has hash
                    print("hash ignore: ignored for loop at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # check for keyword
                if utils.hasKeyword(lineIndex, lines) == True:
                    print("keyword ignore: ignored for loop at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(
                    line, lineIndex, lines)
                if checkParenthResult == None:
                    print("keyword in parenth ignore: ignored for loop at " + str(lineIndex+1) + " in file " + fileToEdit.name)
                    continue
                elif checkParenthResult[0] == False:
                    # doesnt end on same line
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                    lastCloseParenthIndex = lines[nxtLnIndex - 1].rfind(")")  + 1
                elif checkParenthResult[0] == True:
                    # ends on same line
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                    lastCloseParenthIndex = line.rfind(")")  + 1

                
                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    
                    # no { on same ln and on subsequent lines

                    # check if it has stuff on same line
                    # add brace
                    linesEdited = linesEdited + 1
                    if isOnSameLine:
                        if line[lastCloseParenthIndex:].isspace():
                            if currentLineIsComment:
                                toAddLine = line[:-1] + \
                                    " { " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line[:-1] + " {\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            checkForSemiColonIndex = lineIndex + 1
                        elif line[lastCloseParenthIndex:].find(";") != -1:
                            # semicolon found on same line
                            print("same line ignore: ignored for loop at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                    else:
                        if lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace():
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line[:-1] + \
                                    " { " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            checkForSemiColonIndex = nxtLnIndex
                        elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1:
                            print("same line ignore: ignored for loop at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue

                    # check for semicolons to add Closing brace
                    closingBraceLineIndex = utils.getNextSemiColonLine(
                        checkForSemiColonIndex, lines) + 1

                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    spaces = " " * forLoopIndex

                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-
                                                                       1] + spaces + "}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

            # ---------------------------------------------------------------------------

            # find while loops
            whileLoopIndex = line.find("while")
            if whileLoopIndex == firstCharIndex:
                # found a while loop
                hasHash = utils.checkForHash(lineIndex, lines)
                if hasHash != -1:
                    # has hash
                    print("hash ignore: ignored While loop at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # check for keyword
                if utils.hasKeyword(lineIndex, lines) == True:
                    print("keyword ignore: ignored While loop at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue

                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(
                    line, lineIndex, lines)
                if checkParenthResult == None:
                    print("keyword in parenth ignore: ignored while loop at " + str(lineIndex+1) + " in file " + fileToEdit.name)
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                    lastCloseParenthIndex = lines[nxtLnIndex - 1].rfind(")")  + 1
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                    lastCloseParenthIndex = line.rfind(")")  + 1

                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln on same line or subsequent lines
                    # add braces
                    linesEdited = linesEdited + 1
                    if isOnSameLine:
                        if line[lastCloseParenthIndex:].isspace():
                            if currentLineIsComment:
                                toAddLine = line[:-1] + \
                                    " { " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line[:-1] + " {\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            checkForSemiColonIndex = lineIndex + 1
                        elif line[lastCloseParenthIndex:].find(";") != -1:
                            # semicolon found on same line
                            print("same line ignore: ignored WHILE loop at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                    else:
                        if lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace():
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line[:-1] + \
                                    " { " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            checkForSemiColonIndex = nxtLnIndex
                        elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1:
                            print("same line ignore: ignored while loopy at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue

                    # check for semicolons to add Closing brace
                    closingBraceLineIndex = utils.getNextSemiColonLine(
                        checkForSemiColonIndex, lines) + 1

                    # add closing braces at closingBraceLine (inserting a new ln), with indentation
                    spaces = " " * whileLoopIndex
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-
                                                                       1] + spaces + "}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

            # ---------------------------------------------------------------------------

            # find if conditions
            ifConditionIndex = line.find("if")
            if ifConditionIndex == firstCharIndex:
                # found an if comndion
                # FIND "#" in the NEXT FEW LINES:s
                hasHash = utils.checkForHash(lineIndex, lines)
                if hasHash != -1:
                    # has hash
                    print("hash ignore: ignored if condition at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # check for keyword
                if utils.hasKeyword(lineIndex, lines) == True:
                    print("keyword ignore: ignored if Condition at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(
                    line, lineIndex, lines)
                if checkParenthResult == None:
                    print("keyword in parenth ignore: ignored if condition at " + str(lineIndex+1) + " in file " + fileToEdit.name)
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex
                    lastCloseParenthIndex = lines[nxtLnIndex - 1].rfind(")") + 1
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                    lastCloseParenthIndex = line.rfind(")") + 1
                    
                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln and on subsequent lines
                    # add open CURLY on same line
                    linesEdited = linesEdited + 1
                    
                    if isOnSameLine:
                        if line[lastCloseParenthIndex:].isspace():
                            if currentLineIsComment:
                                toAddLine = line[:-1] + \
                                    " { " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line[:-1] + " {\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            checkForSemiColonIndex = lineIndex + 1
                            
                        elif line[lastCloseParenthIndex:].find(";") != -1:
                            
                            # semicolon found on same line
                            print("same line ignore: ignored IF CONDITON at " + str(lineIndex) + " in file " + fileToEdit.name)
                            
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                    else:
                        if lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace():
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line[:-1] + \
                                    " { " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            checkForSemiColonIndex = nxtLnIndex
                        elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1:
                            print("same line ignore: ignored IF at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                    # check for semicolons to add Closing brace
                    closingBraceLineIndex = utils.getNextSemiColonLine(
                        checkForSemiColonIndex, lines) + 1
                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    spaces = " " * ifConditionIndex
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-
                                                                       1] + spaces + "}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

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
                if hasHash != -1:
                    # has hash
                    print("hash ignore: ignored else/ else if at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                # check for keyword
                if utils.hasKeyword(lineIndex, lines) == True:
                    print("keyword ignore: ignored else/ else if at " + str(lineIndex + 1) + " in file " + fileToEdit.name)
                    continue
                if line.find("if") != -1:
                    # line is else if
                    checkParenthResult = utils.checkForParentheses(
                        line, lineIndex, lines)
                else:
                    # no need to call checkForParentheses
                    checkParenthResult = (True,)

                if checkParenthResult == None:
                    print("keyword in parenth ignore: ignored else/ else if at " + str(lineIndex+1) + " in file " + fileToEdit.name)
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                    lastCloseParenthIndex = lines[nxtLnIndex - 1].rfind(")") + 1
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                    lastCloseParenthIndex = lines[nxtLnIndex - 1].rfind(")") + 1

                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln or on subsequent lines
                    # add open CURLY on same line
                    linesEdited = linesEdited + 1
                    if isOnSameLine:
                        if line[lastCloseParenthIndex:].isspace():
                            if currentLineIsComment:
                                toAddLine = line[:-1] + \
                                    " { " + commentOfCurrentLine + "\n"
                            else:
                                toAddLine = line[:-1] + " {\n"
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine)
                            checkForSemiColonIndex = lineIndex + 1
                        elif line[lastCloseParenthIndex:].find(";") != -1:
                            # semicolon found on same line
                            print("same line ignore: ignored ELSe/ Else ifi at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                    else:
                        if lines[nxtLnIndex - 1][lastCloseParenthIndex:].isspace():
                            nxtLnTrimComment = utils.trimComment(
                                lines[nxtLnIndex - 1], (nxtLnIndex - 1), lines)
                            if nxtLnTrimComment.hasComment:
                                toAddLine = nxtLnTrimComment.line[:-1] + \
                                    " { " + nxtLnTrimComment.comment + "\n"
                            else:
                                toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                            del lines[nxtLnIndex - 1]
                            lines.insert(nxtLnIndex - 1, toAddLine)
                            checkForSemiColonIndex = nxtLnIndex
                        elif lines[nxtLnIndex - 1][lastCloseParenthIndex:].find(";") != -1:
                            print("same line ignore: ignored elseie/ else ifi at " + str(lineIndex) + " in file " + fileToEdit.name)
                            linesEdited = linesEdited - 1
                            continue
                        else:
                            print("I AM A CANCELLLE!" + str(lineIndex) + "::" + fileToEdit.name)
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
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-
                                                                       1] + spaces + "}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

            # ---------------------------------------------------------------------------

        except:
            e = sys.exc_info()[0]
            print("runtime error: " + str(e) + " in file name: " +
                  fileToEdit.name + " around line " + str(lineIndex + 1), end = "")
            print(", Most likely a syntax error in the C file.")
            continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()
    return linesEdited


def main():
    VERSION_NUMBER = "0.1.8-alpha"
    NEW_CHANGES = "fixed sameline error"
    KNOWN_BUGS = """
    \tfailure 2: macros.. there are some macros in cfiles also. like conffileapi.c
    \tfailure NO-1: comment in ()
    """
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'


    if (len(sys.argv) != 2):
        print("Usage: python3.7 codeStyliser.py [DIRECTORY_NAME]")
        print("DIRECTORY_NAME IS REQUIRED")
        sys.exit()
    else:
        DIR_NAME = sys.argv[1]
        fileNo = 0
        linesEdited = 0
        print("Welcome to CodeStyliser ver" + VERSION_NUMBER)
        print("\twith changes: " + NEW_CHANGES)
        print("\t and with amazing bugs: " + KNOWN_BUGS)
        print("Made by Pranjal Rastogi, for and in Python 3.7.7 64Bit")
        print("Fixing code in (.c) files under " + DIR_NAME + "\n")
        print("Giving 1 second to read above things")
        time.sleep(1)
        print("started...")
        for root, subdirs, files in os.walk(DIR_NAME):

            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".", 1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c":
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
                    try:
                        with open(file_path, "r+") as fileToStyle:
                            linesEdited = styliseCode(fileToStyle)  + linesEdited
                    except:
                        e = sys.exc_info()[0]
                        print("runtime error: " + str(e) + " at file name: " +
                              filename + " while opening file")
                        continue
                else:
                    continue
        print("Added braces " + str(linesEdited) + " times in " +  str(fileNo) + " files")
        print("Done for all files, now exiting")


if __name__ == "__main__":
    main()
