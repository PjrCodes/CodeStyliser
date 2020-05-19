#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# Do not copy this code.
# DO NOT RE-DISTRIBUTE
# ---
# THE codeStyliser Utility
# ---
# Made in python 3.7.7 64 bit, use only this version
# ---
# codeStyliser.py
# code Styliser, starting main file
# ---


import sys
import re
import os
import utilities as utils
import time



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
            currentLineIsComment = False
            isMultiline = False
            commentOfCurrentLine = ""
            # search for comments
            trimmedCommentResult = utils.trimComment(lines[lineIndex], lineIndex, lines)
            line = trimmedCommentResult.line

            if trimmedCommentResult.hasComment == True and trimmedCommentResult.isMultiline == False:
                currentLineIsComment = True
                commentOfCurrentLine = trimmedCommentResult.comment
            elif trimmedCommentResult.isMultiline == True:
                isMultiline = trimmedCommentResult.isMultiline
                currentLineIsComment = trimmedCommentResult.hasComment
                commentOfCurrentLine = trimmedCommentResult.comment
                # if comment, jump
                lineIndex = trimmedCommentResult.multiLineJumpIndex
                line = trimmedCommentResult.line
            elif trimmedCommentResult.hasComment == False:
                currentLineIsComment = False
                isMultiline = False
                commentOfCurrentLine = trimmedCommentResult.comment
            else:
                print("FATAL error in comment checking, at line " +
                    str(lineIndex) + " file: " + fileToEdit.name)
                continue

            firstCharIndex = utils.getFirstCharacterIndex(line)
            # ---------------------------------------------------------------------------
            # find for loops
            forLoopMatch = re.search(r"\b(for)\b", line)
            if forLoopMatch:
                forLoopIndex = forLoopMatch.start()
            else:
                forLoopIndex = -1

            if forLoopIndex == firstCharIndex:
                forLoopHandler = utils.handleKeyword(KEYWORD="for", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, isMultiline=isMultiline,keywordIndex=forLoopIndex)
                if forLoopHandler == None:
                    continue
                else:
                    lines = forLoopHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------

            # find while loops
            whileLoopMatch = re.search(r"\b(while)\b", line)
            if whileLoopMatch:
                whileLoopIndex = whileLoopMatch.start()
            else:
                whileLoopIndex = -1
            
            if whileLoopIndex == firstCharIndex:
                whileLoopHandler = utils.handleKeyword(KEYWORD="while", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=whileLoopIndex, isMultiline=isMultiline)
                if whileLoopHandler == None:
                    continue
                else:
                    lines = whileLoopHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------

            # find if conditions
            ifConditionMatch = re.search(r"\b(if)\b", line)
            if ifConditionMatch:
                ifConditionIndex = ifConditionMatch.start()
            else:
                ifConditionIndex = -1

            if ifConditionIndex == firstCharIndex:
                ifConditionHandler = utils.handleKeyword(KEYWORD="if", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=ifConditionIndex, isMultiline=isMultiline)
                if ifConditionHandler == None:
                    continue
                else:
                    lines = ifConditionHandler
                    linesEdited = linesEdited + 1

            # ---------------------------------------------------------------------------
            # find else conditions
            startingCurlyBraceIndex = line.find("}")
            elseConditionMatch = re.search(r"\b(else)\b", line)
            if elseConditionMatch:
                startingElseIndex = elseConditionMatch.start()
            else:
                startingElseIndex = -1
            lineStartsOnBrace = False
            if startingCurlyBraceIndex == firstCharIndex:
                # line starts on a }
                lineStartsOnBrace = True
            
            if lineStartsOnBrace and startingElseIndex != -1:
                # we have a line with an } and an else after it
                # process else
                elseConditionHandler = ifConditionHandler = utils.handleKeyword(KEYWORD="else -", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=startingCurlyBraceIndex, isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    linesEdited = linesEdited + 1
            elif startingElseIndex == firstCharIndex and not lineStartsOnBrace:
                # we have an else
                elseConditionHandler = ifConditionHandler = utils.handleKeyword(KEYWORD="else -", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=startingElseIndex, isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    linesEdited = linesEdited + 1
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
    VERSION_NUMBER = "0.1.9.5-alpha"
    NEW_CHANGES = "fixed multiline comment error"
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
        print("\tand with the BEST INSECTS as on github.com")
        print("Made by Pranjal Rastogi, for and in Python 3.7.7 64Bit")
        print("Will fix (.c) code for files under " + DIR_NAME)
        print("you have three seconds to read the above data")
        time.sleep(3)
        print("\n\n")

        print("{:=^40}".format(" STARTING... "))
        
        for root, _, files in os.walk(DIR_NAME):

            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".", 1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c":
                    
                    print ("working ...", end="\r", flush=True)
                    time.sleep(0.2)
                    fileNo = fileNo + 1
                    # file_example = open (file_path, "r")
                    # for line in file_example:
                    #     print(line)
                    #     print("HI")
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
                            linesEdited = styliseCode(fileToStyle) + linesEdited
                    except UnicodeDecodeError as e:
                        with open(file_path,"r+", encoding="ISO-8859-1") as fileToStyle:
                            linesEdited = styliseCode(fileToStyle) + linesEdited
                        
                else:
                    continue
        print("\n")
        print("{:=^40}".format(" SUMMARY "))
        print("Added braces " + str(linesEdited) + " times in " + str(fileNo) + " files")
        print("{:=^40}".format(" ENDED "))

if __name__ == "__main__":
    main()
