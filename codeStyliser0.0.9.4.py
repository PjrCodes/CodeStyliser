# Copyright (c) 2020 Pranjal Rastogi
#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, please use only this version

import sys
import re
import os
import utils as utils

#TODO: same line for/ while/ if
#TODO: error handler
#TODO: utf-8

SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"
VERSION_NUMBER = "0.0.9.4-alpha"
NEW_CHANGES = " added recursive folder searching and stylising, fixed extension"
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'



def styliseCode(fileToEdit):
    
    # so that first line's index is 0
    lineIndex = -1
    
    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    
    for line in lines:
        try:
            lineIndex = lineIndex + 1
            currentLineIsComment = False
            # search for comments
            comment = re.search(SINGLELINE_COMMENT_PATTERN,line)
            if (comment):
                # found a Single line comment
                currentLinesComment = line[comment.start():]
                line = line[:comment.start()]
                currentLineIsComment = True
            firstCharIndex = utils.getFirstCharacterIndex(line)

            # ---------------------------------------------------------------------------

            # find for loops
            forLoopIndex = line.find("for")
            if forLoopIndex == firstCharIndex:
                # found a for loop

                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(line, lineIndex, lines)
                if checkParenthResult == None:
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex + 1
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")

                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln and on subsequent lines

                    # add brace
                    if isOnSameLine:

                        if currentLineIsComment:
                            toAddLine = line[:-1] + " { " + currentLinesComment[:-1] + "\n"
                        else:
                            toAddLine = line[:-1] + " {\n"
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine)
                        checkForSemiColonIndex = lineIndex + 1
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                        del lines[nxtLnIndex - 1]
                        lines.insert(nxtLnIndex - 1, toAddLine)
                        checkForSemiColonIndex = nxtLnIndex + 1

                    # check for semicolons to add Closing brace
                    while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                        # line has no semicolon or it is a comment
                        checkForSemiColonIndex = checkForSemiColonIndex + 1
                    else:
                        # line has a semicolon and is NOT a comment
                        closingBraceLineIndex = checkForSemiColonIndex + 1
                    
                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    spaces = " " * forLoopIndex 

                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)
            
            # ---------------------------------------------------------------------------

            # find while loops
            whileLoopIndex = line.find("while")
            if whileLoopIndex == firstCharIndex:
                # found a while loop

                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(line, lineIndex, lines)
                if checkParenthResult == None:
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex + 1
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                
                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln on same line or subsequent lines

                    # add braces                        
                    if isOnSameLine:
                        if currentLineIsComment:
                            toAddLine = line[:-1] + " { " + currentLinesComment[:-1] + "\n"
                        else:
                            toAddLine = line[:-1] + " {\n"
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine)
                        checkForSemiColonIndex = lineIndex + 1
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                        del lines[nxtLnIndex - 1]
                        lines.insert(nxtLnIndex - 1, toAddLine)
                        checkForSemiColonIndex = nxtLnIndex + 1

                    # check for semicolons to add Closing brace
                    while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                        # line has no semicolon or it is a comment
                        checkForSemiColonIndex = checkForSemiColonIndex + 1
                    else:
                        # line has a semicolon and is NOT a comment
                        closingBraceLineIndex = checkForSemiColonIndex + 1
                    
                    # add closing braces at closingBraceLine (inserting a new ln), with indentation
                    spaces = " " * whileLoopIndex
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)
            
            # ---------------------------------------------------------------------------
            
            # find if conditions
            ifConditionIndex = line.find("if")
            if ifConditionIndex == firstCharIndex:
                # found an if comndion

                # we must now skip over all parentheses to find the end of the (condition)
                # we must now skip over all parentheses to find the end of the (condition)
                checkParenthResult = utils.checkForParentheses(line, lineIndex, lines)
                if checkParenthResult == None:
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex + 1
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                
                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln and on subsequent lines
                    
                    # add open CURLY on same line
                    if (isOnSameLine):
                        if currentLineIsComment:
                            toAddLine = line[:-1] + " { " + currentLinesComment[:-1] + "\n"
                        else:
                            toAddLine = line[:-1] + " {\n"
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine)
                        checkForSemiColonIndex = lineIndex + 1
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                        del lines[nxtLnIndex - 1]
                        lines.insert(nxtLnIndex - 1, toAddLine)
                        checkForSemiColonIndex = nxtLnIndex + 1
                    # check for semicolons to add Closing brace
                    
                    while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                        # line has no semicolon or it is a comment
                        checkForSemiColonIndex = checkForSemiColonIndex + 1
                    else:
                        # line has a semicolon and is NOT a comment
                        closingBraceLineIndex = checkForSemiColonIndex + 1
                    
                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    spaces = " " * ifConditionIndex 
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
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
                checkParenthResult = utils.checkForParentheses(line, lineIndex, lines)
                if checkParenthResult == None:
                    continue
                elif checkParenthResult[0] == False:
                    isOnSameLine = checkParenthResult[0]
                    nxtLnIndex = checkParenthResult[1]
                    nextLineIndex = nxtLnIndex + 1
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                elif checkParenthResult[0] == True:
                    isOnSameLine = checkParenthResult[0]
                    nextLineIndex = lineIndex + 1
                    openCurlyBraceIndex = line.find("{")
                
                if openCurlyBraceIndex == -1 and utils.checkForOpenBrace(nextLineIndex, lines) == -1:
                    # no { on same ln or on subsequent lines

                    # add open CURLY on same line
                    if (isOnSameLine):
                        if currentLineIsComment:
                            toAddLine = line[:-1] + " { " + currentLinesComment[:-1] + "\n"
                        else:
                            toAddLine = line[:-1] + " {\n"
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine)
                        checkForSemiColonIndex = lineIndex + 1
                    else:
                        toAddLine = lines[nxtLnIndex - 1][:-1] + " {\n"
                        del lines[nxtLnIndex - 1]
                        lines.insert(nxtLnIndex - 1, toAddLine)
                        checkForSemiColonIndex = nxtLnIndex + 1
                    # check for semicolons to add Closing brace
                    
                    while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                        # line has no semicolon or it is a comment
                        checkForSemiColonIndex = checkForSemiColonIndex + 1
                    else:
                        # line has a semicolon and is NOT a comment
                        closingBraceLineIndex = checkForSemiColonIndex + 1
                    
                    # add closing braces at closingBraceLine (inserting a new ln) with indentation
                    if lineStartsOnBrace:
                        spaces = " " * startingCurlyBraceIndex
                    elif not lineStartsOnBrace:
                        spaces = " " * startingAtElseIndex 
                    lines.insert(closingBraceLineIndex, " ")
                    addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                    lines.insert(closingBraceLineIndex, addClosingBraceLine)

            # --------------------------------------------------------------------------- 


        except:
            e = sys.exc_info()[0]
            print("error: "+ str(e) + " at file name: " + fileToEdit.name)
            print(sys.exc_info()[1])
            continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()


def main():
    if (len(sys.argv) != 2):
        print("Usage: python3.7 codeStyliser.py [DIRECTORY_NAME]")
        print("DIRECTORY_NAME IS REQUIRED")
        sys.exit()
    else:
        DIR_NAME = sys.argv[1]
        print("Welcome to CodeStyliser ver" + VERSION_NUMBER)
        print("Made by Pranjal Rastogi")
        print("Made for python 3.7.7 64-Bit")
        print("NEW CHANGES IN ver" + VERSION_NUMBER + NEW_CHANGES)
        print("Will add curly braces where they are supposed to be for all (.C) files in " + DIR_NAME)

        for root, subdirs, files in os.walk(DIR_NAME):

            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".",1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c":
                    try:
                        with open(file_path, 'rb') as open_file:
                            content = open_file.read()
                            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
                        with open(file_path, 'wb') as open_file:
                            open_file.write(content)
                            open_file.close()
                    except:
                        e = sys.exc_info()[0]
                        print("error: " + str(e) + " at file name: " + filename + " while changing line endings")
                        continue
                    try:
                        with open(file_path, "r+") as fileToStyle:
                            styliseCode(fileToStyle)
                    except:
                        e = sys.exc_info()[0]
                        print("error: "+ str(e) + " at file name: " + filename + " while opening file")
                        continue
                else:
                    continue
                
        print("Done for all files, now exitting")

if __name__ == "__main__":
    main()



