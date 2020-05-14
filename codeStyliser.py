# Copyright (c) 2020 Pranjal Rastogi
 #!/usr/local/bin/python3
 # python 3.7.7 64 bit
import sys
import re
SINGLELINE_COMMENT_PATTERN = r"(\/\*.*?\*\/)|(\/\/[^\n]*)"
VERSION_NUMBER = "0.0.3-alpha"

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
        """ 
        elif multiLineComment != -1:
            #found a comment that starts with /*
            
            # check if comment ends on same line
            sameLineClose = line.find("*/")
            if sameLineClose != -1:
                # comment ends on same line, see only before /*
                line = line[:multiLineComment]
            else:
                # comment doesnt end on same line, check through subsequent lines for */
                commentCheckerIndex = lineIndex + 1 
                while lines[commentCheckerIndex].find("*/") == -1:
                    # did not find */, still in comment
                    commentCheckerIndex = commentCheckerIndex + 1
                else: 
                    # found */, this line is when comment ends
                    line = line[commentCheckerIndex + 1]
        """
    
        firstCharIndex = len(line) - len(line.lstrip())

        # find for loops
        forLoopIndex = line.find("for")
        # openParenthCheckFor = line[forLoopIndex:].find("(")
        if forLoopIndex == firstCharIndex:
            # found a for loop
            print("\nfor loop found at " + str(lineIndex + 1) + ":" + str(forLoopIndex))

            # we must now skip over all parentheses to find the end of the (condition)
            allOpenParenth = re.findall(r"\(", line)
            allCloseParenth = re.findall(r"\)", line)
            print(len(allOpenParenth))
            print(len(allCloseParenth))
            openParenthNo = len(allOpenParenth)
            closeParenthNo = len(allCloseParenth)
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses
                # we must find till len(allOpenParenth) = closeParenth count
                nxtLnIndex = lineIndex + 1

                while closeParenthNo != openParenthNo:
                    
                    newOpenParenth = re.findall(r"\(", lines[nxtLnIndex])
                    newCloseParenth = re.findall(r"\)", lines[nxtLnIndex])
                    openParenthNo = len(newOpenParenth) + openParenthNo
                    closeParenthNo = len(newCloseParenth) + closeParenthNo
                    nxtLnIndex = nxtLnIndex + 1
                else:
                    # closeParenthNo = openParenthNo
                    # nxtLnIndex must be where openCurlyBrace should be.
                    # check for OPEN curly Brace on THE SAME LINE as for loop
                    print("BROKE LOOP")
                    openCurlyBraceIndex = lines[nxtLnIndex - 1].find("{")
            else:
                openCurlyBraceIndex = line.find("{")
                isOnSameLine = True

            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
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
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        #TODO: change this part
                        # if line is the for line, then add at lineINdex or add { at nxtLnIndex
                        
                        if (isOnSameLine):
                            toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                            checkForSemiColonIndex = lineIndex + 1

                        elif (isOnSameLine == False):
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
        # openParenthCheckWhile = line[whileLoopIndex:].find("(")
        if whileLoopIndex == firstCharIndex:
            # found a while loop
            print("\nwhile loop found at " + str(lineIndex + 1) + ":" + str(whileLoopIndex))
            
            # we must now skip over all parentheses to find the end of the (condition)
            allOpenParenth = re.findall(r"\(", line)
            allCloseParenth = re.findall(r"\)", line)
            openParenthNo = len(allOpenParenth)
            closeParenthNo = len(allCloseParenth)
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses
                # we must find till len(allOpenParenth) = closeParenth count
                nxtLnIndex = lineIndex + 1
                while closeParenthNo != openParenthNo:
                    
                    newOpenParenth = re.findall(r"\(", lines[nxtLnIndex])
                    newCloseParenth = re.findall(r"\)", lines[nxtLnIndex])
                    openParenthNo = len(newOpenParenth) + openParenthNo
                    closeParenthNo = len(newCloseParenth) + closeParenthNo
                    nxtLnIndex = nxtLnIndex + 1
                else:
                    
                    # closeParenthNo = openParenthNo
                    # nxtLnIndex must be where openCurlyBrace should be.
                    # check for OPEN curly Brace on THE SAME LINE as while loop
                    openCurlyBraceIndex = lines[nxtLnIndex].find("{")
            else:
                isOnSameLine = True
                openCurlyBraceIndex = line.find("{")
            
            
            if openCurlyBraceIndex == -1:
                # no { on same ln
                # check for Open brace on next few lines:
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
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        if (isOnSameLine):
                            toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                            checkForSemiColonIndex = lineIndex + 1
                        elif (isOnSameLine == False):
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
        # openParenthCheckIf = line[ifConditionIndex:].find("(")
        if ifConditionIndex == firstCharIndex:
            # found a if condition
            print("\nIF CONDITION found at " + str(lineIndex + 1) + ":" + str(ifConditionIndex))
            # we must now skip over all parentheses to find the end of the (condition)
            allOpenParenth = re.findall(r"\(", line)
            allCloseParenth = re.findall(r"\)", line)
            openParenthNo = len(allOpenParenth)
            closeParenthNo = len(allCloseParenth)
            if openParenthNo != closeParenthNo:
                isOnSameLine = False
                # the line doesnt have same amt of close and open parentheses
                # we must find till len(allOpenParenth) = closeParenth count
                nxtLnIndex = lineIndex + 1
                while closeParenthNo != openParenthNo:
                    newOpenParenth = re.findall(r"\(", lines[nxtLnIndex])
                    newCloseParenth = re.findall(r"\)", lines[nxtLnIndex])
                    openParenthNo = len(newOpenParenth) + openParenthNo
                    closeParenthNo = len(newCloseParenth) + closeParenthNo
                    nxtLnIndex = nxtLnIndex + 1
                else:
                    # closeParenthNo = openParenthNo
                    # nxtLnIndex must be where openCurlyBrace should be.
                    # check for OPEN curly Brace on THE SAME LINE as if condition
                    openCurlyBraceIndex = lines[nxtLnIndex].find("{")
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
                        print("No open brace on same line or next line, adding curly braces")
                        # add open CURLY on same line
                        if (isOnSameLine):
                            toAddLine = line[:-1] + " {\n" # line:-1 removes the last char
                            del lines[lineIndex]
                            lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                            checkForSemiColonIndex = lineIndex + 1
                        elif (isOnSameLine == False):
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
    FILE_NAME = input('Please enter file name to be edited(File must be in same directory as codeStyliser.py): ')
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
