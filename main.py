# Copyright (c) 2020 Pranjal Rastogi
import sys
import re
SINGLELINE_COMMENT_PATTERN = r"\/\/.*"

def styliseCode(fileToEdit):
    
    # so that first line's index is 0
    lineIndex = -1
    
    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    
    for line in lines:
        lineIndex = lineIndex + 1

        # search for comments
        comment = re.search(SINGLELINE_COMMENT_PATTERN, line)
        multiLineComment = line.find("/*")
        if (comment):
            # found a comment that starts with //, see only before //
            line = line[0:comment.start()]
        elif multiLineComment != -1:
            #found a comment that starts with /*
            
            # check if comment ends on same line
            sameLineClose = line.find("*/")
            if sameLineClose != -1:
                # comment ends on same line, see only before /*
                line = line[0:(multiLineComment+1)]
            else:
                # comment doesnt end on same line, check through subsequent lines for */
                commentCheckerIndex = lineIndex + 1 
                while lines[commentCheckerIndex].find("*/") == -1:
                    # did not find */, still in comment
                    commentCheckerIndex = commentCheckerIndex + 1
                    
        
        # find for loops
        forLoopIndex = line.find("for")
        if forLoopIndex != -1:
            # found a for loop
            print("\nFOR loop at " + str(lineIndex + 1) + ":" + str(forLoopIndex))

            # check for OPEN curly Brace on THE SAME LINE as For loop.
            openCurlyBraceIndex = line.find("{")

            # check for Open brace on next few lines:
            nextLineIndex = lineIndex + 1
            while re.search(SINGLELINE_COMMENT_PATTERN,lines[nextLineIndex]) or lines[nextLineIndex].isspace():
                # next line is a "//"comment OR a space OR a "/*" comment
                nextLineIndex =  nextLineIndex + 1
            else:
                # next line is not a comment/ space, must find openBrace
                openCurlyBraceOnNxtLine = lines[nextLineIndex].find("{")
                # if no OpenCurlyBrace, this line HAS to be the statement line, so } must be on next line
                closingBraceLineIndex = nextLineIndex + 1
                
            
            if openCurlyBraceIndex == -1 and openCurlyBraceOnNxtLine == -1:
                # no open curly braces found
                print("NO open brace on same line and no CURLY on NEXT LINE")
                
                # add Curlybraces
                toAddLine = line[:-1] + " {\n" # len(line)-1 removes the last char
                del lines[lineIndex]
                lines.insert(lineIndex, toAddLine) # add toAddLine to currentLine
                spaces = " " * forLoopIndex
                print(closingBraceLineIndex)
                if lines[closingBraceLineIndex].isspace():
                    addClosingBraceLine = spaces + "}\n"
                else:
                    addClosingBraceLine = lines[closingBraceLineIndex][:-1] + spaces +"}\n"
                del lines[closingBraceLineIndex]
                lines.insert(closingBraceLineIndex, addClosingBraceLine)

    fileToEdit.seek(0)
    fileToEdit.writelines(lines)


def openFile():
    try:
        fileToEdit = open(FILE_NAME, "r+")
        styliseCode(fileToEdit)
        fileToEdit.close()
    except FileNotFoundError:
        print("Error file not found")
        sys.exit()


FILE_NAME = input(
    'Please enter file name to be edited\n File must be in same directory as main.py: ')
FILE_NAME = "sample-copy.c"
if FILE_NAME.find(".c") == -1:
    print("error, must be C file")
    sys.exit()
else:
    openFile()
