# Copyright (c) 2020 Pranjal Rastogi
 #!/usr/local/bin/python3
 # python 3.7.7 64 bit
import sys
import re
SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"
VERSION_NUMBER = "0.0.2"

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
        # elif multiLineComment != -1:
        #     #found a comment that starts with /*
            
        #     # check if comment ends on same line
        #     sameLineClose = line.find("*/")
        #     if sameLineClose != -1:
        #         # comment ends on same line, see only before /*
        #         line = line[:multiLineComment]
        #     else:
        #         # comment doesnt end on same line, check through subsequent lines for */
        #         commentCheckerIndex = lineIndex + 1 
        #         while lines[commentCheckerIndex].find("*/") == -1:
        #             # did not find */, still in comment
        #             commentCheckerIndex = commentCheckerIndex + 1
        #         else: 
        #             # found */, this line is when comment ends
        #             line = line[commentCheckerIndex + 1]
    
        # find for loops
        forLoopIndex = line.find("for")
        openParenthCheckFor = line[forLoopIndex:].find("(")
        if forLoopIndex != -1 and openParenthCheckFor != -1:
            # found a for loop
            print("\nfor loop found at " + str(lineIndex + 1) + ":" + str(forLoopIndex))

            # check for OPEN curly Brace on THE SAME LINE as For loop.
            openCurlyBraceIndex = line.find("{")
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
                nextLineIndex = lineIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                        
                        # check for semicolons to add Closing brace
                        checkForSemiColonIndex = lineIndex + 1
                        while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                            # line has no semicolon or it is a comment
                            checkForSemiColonIndex = checkForSemiColonIndex + 1
                        else:
                            # line has a semicolon and is NOT a comment
                            # we must add closing brace on nxt line:
                            closingBraceLineIndex = checkForSemiColonIndex + 1
                        
                        # add closing braces at closingBraceLine (inserting a new ln)
                        spaces = " " * forLoopIndex # add indent
                        # if lines[closingBraceLineIndex].isspace():
                        #     del lines[closingBraceLineIndex]
                        #     addClosingBraceLine = "\n"+spaces + "}\n"
                        # else:
                        lines.insert(closingBraceLineIndex, " ")
                        addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                        lines.insert(closingBraceLineIndex, addClosingBraceLine)
        # find while loops
        whileLoopIndex = line.find("while")
        openParenthCheckWhile = line[whileLoopIndex:].find("(")
        if whileLoopIndex != -1 and openParenthCheckWhile != -1:
            # found a while loop
            print("\nwhile loop found at " + str(lineIndex + 1) + ":" + str(whileLoopIndex))
            
            # check for OPEN curly Brace on THE SAME LINE as While loop.
            openCurlyBraceIndex = line.find("{")
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
                nextLineIndex = lineIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                        
                        # check for semicolons to add Closing brace
                        checkForSemiColonIndex = lineIndex + 1
                        while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                            # line has no semicolon or it is a comment
                            checkForSemiColonIndex = checkForSemiColonIndex + 1
                        else:
                            # line has a semicolon and is NOT a comment
                            # we must add closing brace on nxt line:
                            closingBraceLineIndex = checkForSemiColonIndex + 1
                        
                        # add closing braces at closingBraceLine (inserting a new ln)
                        spaces = " " * whileLoopIndex # add indent
                        # if lines[closingBraceLineIndex].isspace():
                        #     del lines[closingBraceLineIndex]
                        #     addClosingBraceLine = "\n"+spaces + "}\n"
                        # else:
                        lines.insert(closingBraceLineIndex, " ")
                        addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                        lines.insert(closingBraceLineIndex, addClosingBraceLine)
        # find if conditions
        ifConditionIndex = line.find("if")
        openParenthCheckIf = line[ifConditionIndex:].find("(")
        if ifConditionIndex != -1 and openParenthCheckIf != -1:
            # found a while loop
            print("\nIF CONDITION found at " + str(lineIndex + 1) + ":" + str(whileLoopIndex))
            
            # check for OPEN curly Brace on THE SAME LINE as While loop.
            openCurlyBraceIndex = line.find("{")
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
                nextLineIndex = lineIndex + 1
                while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                    # next line is a singleLineComment OR a space, we must skip it
                    nextLineIndex =  nextLineIndex + 1
                else:
                    # next line is not a comment/ space, must find openBrace
                    if (lines[nextLineIndex].find("{") == -1):
                        # no open curly braces found
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                        del lines[lineIndex]
                        lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                        
                        # check for semicolons to add Closing brace
                        checkForSemiColonIndex = lineIndex + 1
                        while lines[checkForSemiColonIndex].find(";") == -1 or re.search(SINGLELINE_COMMENT_PATTERN,lines[checkForSemiColonIndex]):
                            # line has no semicolon or it is a comment
                            checkForSemiColonIndex = checkForSemiColonIndex + 1
                        else:
                            # line has a semicolon and is NOT a comment
                            # we must add closing brace on nxt line:
                            closingBraceLineIndex = checkForSemiColonIndex + 1
                        
                        # add closing braces at closingBraceLine (inserting a new ln)
                        spaces = " " * ifConditionIndex # add indent
                        # if lines[closingBraceLineIndex].isspace():
                        #     del lines[closingBraceLineIndex]
                        #     addClosingBraceLine = "\n"+spaces + "}\n"
                        # else:
                        lines.insert(closingBraceLineIndex, " ")
                        addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                        lines.insert(closingBraceLineIndex, addClosingBraceLine)
        # will also search for #if, not implementing!
    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)


def openFile():
    try:
        fileToEdit = open(FILE_NAME, "r+")
        print("Stylising code")
        styliseCode(fileToEdit)
        print("-- DONE -- Closing files")
        fileToEdit.close()
    except FileNotFoundError:
        print("Error file not found")
        sys.exit()

print("Welcome to CodeStyliser, Made in python 3.7.7 64-Bit, please use correct Intrepreter")
print("VERSION NUMBER: " + VERSION_NUMBER)
print("Made by Pranjal Rastogi")
print("Adds curly braces {} for all for loops/ while loops in (.c) files")
if (len(sys.argv) == 1):
    FILE_NAME = input('Please enter file name to be edited(File must be in same directory as main.py): ')
elif (len(sys.argv) == 2):
    FILE_NAME = sys.argv[1]
else:
    print("Usage: python3.7 main.py [filename]")
    print("File name is optional")

if FILE_NAME.find(".c") == -1:
    print("error, must be C file")
    sys.exit()
else:
    openFile()
