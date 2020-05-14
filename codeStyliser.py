# Copyright (c) 2020 Pranjal Rastogi
#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, please use only this version

import sys
import re

SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"
VERSION_NUMBER = "0.0.7-alpha"

def getFirstCharacterIndex(str):
    return len(str) - len(str.lstrip())

def styliseCode(fileToEdit):
    
    # so that first line's index is 0
    lineIndex = -1
    
    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    
    for line in lines:
        lineIndex = lineIndex + 1
        # search for comments
        comment = re.search(SINGLELINE_COMMENT_PATTERN,line)
        if (comment):
            # found a Single line comment
            line = line[:comment.start()]
        firstCharIndex = getFirstCharacterIndex(line)

        # ---------------------------------------------------------------------------

        # find for loops
        forLoopIndex = line.find("for")
        if forLoopIndex == firstCharIndex:
            # found a for loop

            # we must now skip over all parentheses to find the end of the (condition)
            
            openParenthNo = len(re.findall(r"\(", line))
            closeParenthNo = len(re.findall(r"\)", line))

            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses

                nxtLnIndex = lineIndex + 1

                while closeParenthNo != openParenthNo:
                    forChecker = lines[nxtLnIndex].find("for")
                    firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
                    if forChecker == firstCharOfNxtLn:
                        # another for has been found before () number got equal, Cancel case
                        break
                    openParenthNo = len(re.findall(r"\(", lines[nxtLnIndex])) + openParenthNo
                    closeParenthNo = len(re.findall(r"\)", lines[nxtLnIndex])) + closeParenthNo
                    nxtLnIndex = nxtLnIndex + 1
                else:
                    # closeParenthNo = openParenthNo
                    # check for OpenCurlyBrace on same line as (condition)
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                continue
            else:
                openCurlyBraceIndex = line.find("{")
                isOnSameLine = True

            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for open brace on next few lines:
                if isOnSameLine:
                    nextLineIndex = lineIndex + 1
                else:
                    nextLineIndex = nxtLnIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found

                        # add open curly brace
                        if (isOnSameLine):
                            #TODO: change this to allow inline comments to stay
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

            openParenthNo = len(re.findall(r"\(", line))
            closeParenthNo = len(re.findall(r"\)", line))
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses

                nxtLnIndex = lineIndex + 1
                while closeParenthNo != openParenthNo:
                    whileChecker = lines[nxtLnIndex].find("while")
                    firstCharOfNxtLn = getFirstCharacterIndex(lines[nxtLnIndex])
                    if whileChecker == firstCharOfNxtLn:
                        # another while has been found before () number got equal, Cancel case
                        break
                    else:
                        openParenthNo = len(re.findall(r"\(", lines[nxtLnIndex])) + openParenthNo
                        closeParenthNo = len(re.findall(r"\)", lines[nxtLnIndex])) + closeParenthNo
                        nxtLnIndex = nxtLnIndex + 1
                else:
                    # closeParenthNo = openParenthNo
                    # check for OpenCurlyBrace on same line as (condition)
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                continue
            else:
                isOnSameLine = True
                openCurlyBraceIndex = line.find("{")
            
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for open brace on next few lines:
                if isOnSameLine:
                    nextLineIndex = lineIndex + 1
                else:
                    nextLineIndex = nxtLnIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find open brace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found, add braces

                        if (isOnSameLine):
                            #TODO: change this to allow inline comments to stay
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
            openParenthNo = len(re.findall(r"\(", line))
            closeParenthNo = len(re.findall(r"\)", line))
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses
                nxtLnIndex = lineIndex + 1
                while closeParenthNo != openParenthNo:
                    ifChecker = lines[nxtLnIndex].find("if")
                    firstCharOfNxtLn = len(lines[nxtLnIndex]) - len(lines[nxtLnIndex].lstrip())
                    if ifChecker == firstCharOfNxtLn:
                        # another if has been found before () number got equal, Cancel case
                        break
                    else:
     
                        openParenthNo = len(re.findall(r"\(", lines[nxtLnIndex])) + openParenthNo
                        closeParenthNo = len(re.findall(r"\)", lines[nxtLnIndex])) + closeParenthNo
                        nxtLnIndex = nxtLnIndex + 1
                else:
                    # nxtLnIndex must be where openCurlyBrace should be.
                    # check for OPEN curly Brace on THE SAME LINE as if condition
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                continue
            else:
                isOnSameLine = True
                openCurlyBraceIndex = line.find("{")
            
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
                if(isOnSameLine):
                    nextLineIndex = lineIndex + 1
                else:
                    nextLineIndex = nxtLnIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found
                        # add open CURLY on same line
                        if (isOnSameLine):
                            #TODO: change this to allow inline comments to stay
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
        lineStartsOnBrace = False;
        if startingCurlyBraceIndex == firstCharIndex:
            # line starts on a }
            lineStartsOnBrace = True
        if (lineStartsOnBrace and line[startingCurlyBraceIndex:].find("else") != -1) or (startingAtElseIndex == firstCharIndex and lineStartsOnBrace == False):
            # we have a line with an } and an else after it
            # process else

            # we must now skip over all parentheses to find the end of the (condition)
            openParenthNo = len(re.findall(r"\(", line))
            closeParenthNo = len(re.findall(r"\)", line))
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses
                nxtLnIndex = lineIndex + 1
                while closeParenthNo != openParenthNo:
                    ifChecker = lines[nxtLnIndex].find("if")
                    firstCharOfNxtLn = len(lines[nxtLnIndex]) - len(lines[nxtLnIndex].lstrip())
                    if ifChecker == firstCharOfNxtLn:
                        # another if has been found before () number got equal, Cancel case
                        break
                    else:
                        openParenthNo = len(re.findall(r"\(", lines[nxtLnIndex])) + openParenthNo
                        closeParenthNo = len(re.findall(r"\)", lines[nxtLnIndex])) + closeParenthNo
                        nxtLnIndex = nxtLnIndex + 1
                else:
                    # nxtLnIndex must be where openCurlyBrace should be.
                    # check for OPEN curly Brace on THE SAME LINE as if condition
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
                continue
            else:
                isOnSameLine = True
                openCurlyBraceIndex = line.find("{")
            
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
                if(isOnSameLine):
                    nextLineIndex = lineIndex + 1
                else:
                    nextLineIndex = nxtLnIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found
                        # add open CURLY on same line
                        if (isOnSameLine):
                            #TODO: change this to allow inline comments to stay
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

    # write lines back to fileToEdit

    fileToEdit.seek(0)
    fileToEdit.writelines(lines)


def openFile():
    try:
        fileToEdit = open(FILE_NAME, "r+")
        print("Stylising code in " + FILE_NAME)
        styliseCode(fileToEdit)
        print("DONE")
        fileToEdit.close()
    except FileNotFoundError:
        print("Error file not found")
        sys.exit()

print("Welcome to CodeStyliser VERSION " + VERSION_NUMBER)
print("Adds curly braces {} for all single line if, for, while, else statements in (.c) files")
print("Made by Pranjal Rastogi")
print("Made in python 3.7.7 64-Bit, please use correct Interpreter")
if (len(sys.argv) == 1):
    FILE_NAME = input('Please enter file name to be edited(File must be in same directory as codeStyliser.py): ')
elif (len(sys.argv) == 2):
    FILE_NAME = sys.argv[1]
else:
    print("Usage: python3.7 main.py [filename]")
    print("File name is optional")

if FILE_NAME.find(".c") == -1:
    print("Error, " + FILE_NAME + " is not a \".c\" file.")
    sys.exit()
else:
    openFile()

