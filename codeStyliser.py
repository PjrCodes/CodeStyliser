#!/usr/local/bin/python3
# Copyright (c) 2020 Pranjal Rastogi All Rights Reserved
# Do not copy this code.
# check LICENSE for more details
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

DEFINE_PATTERN = r"#\s*\b(define)\b"

def styliseCode(fileToEdit):
    # lines edited in this file
    linesEdited = 0
    # so that first line's index is 0

    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    lineIndex = -1
    while lineIndex < (len(lines) - 1):

        try:
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
                print("FATAL ERROR: in comment checking, at line " +
                    str(lineIndex) + " file: " + fileToEdit.name)
                continue
            
            firstCharIndex = utils.getFirstCharacterIndex(line)
            
            if re.search(DEFINE_PATTERN, line):
                isMacro = True
                if line.rfind("\\") != -1:
                    # found \ at the back of the line
                    pass
                else:
                    # ignore line
                    continue 
            else:
                isMacro = False

            # ---------------------------------------------------------------------------
            # find for loops
            forLoopMatch = re.search(r"\b(for)\b", line)
            if forLoopMatch:
                forLoopIndex = forLoopMatch.start()
            else:
                forLoopIndex = -1

            if forLoopIndex == firstCharIndex:
                forLoopHandler = utils.handleKeyword(KEYWORD="for", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, isMultiline=isMultiline, keywordIndex=forLoopIndex)
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
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=whileLoopIndex, isMultiline=isMultiline)
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
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=ifConditionIndex, isMultiline=isMultiline)
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
                                                isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=startingCurlyBraceIndex, isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    linesEdited = linesEdited + 1
            elif startingElseIndex == firstCharIndex and not lineStartsOnBrace:
                # we have an else
                elseConditionHandler = ifConditionHandler = utils.handleKeyword(KEYWORD="else -", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=startingElseIndex, isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    linesEdited = linesEdited + 1
            # ---------------------------------------------------------------------------
        except (KeyboardInterrupt, SystemExit):
            print("exiting...")
            sys.exit()
        except:
            e = sys.exc_info()[0]
            print("ERROR: " + str(e) + " in file name: " +
                  fileToEdit.name + " around line " + str(lineIndex + 1) + ", skipping line!!", end = "")
            continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()
    return linesEdited


def main():
    VERSION_NUMBER = "0.1.10.3-BETA "
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
        print("\n\n")
        print("{:=^80}".format(" Welcome to CodeStyliser ver" + VERSION_NUMBER))
        print("Made by Pranjal Rastogi, in Python 3.7.7 64-Bit")
        print("Copyright (C) Pranjal Rastogi, 2020")
        print("{:=^80}".format(""))
        print("Will stylise code in (.c) and (.h) files under " + DIR_NAME)
        print("INFO: only changes UTF-8 encoded files")
        print("INFO: changes \"\\r\\n\" to \"\\n\" for all files")
        print("\n")
        time.sleep(2)


        print("{:=^80}".format(" START "))
        startTime = time.time()

        for root, _, files in os.walk(DIR_NAME):

            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".", 1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c":
                    time.sleep(0.1)
                    fileNo = fileNo + 1
                    try:
                        with open(file_path, 'rb') as open_file:
                            content = open_file.read()
                            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
                        with open(file_path, 'wb') as open_file:
                            open_file.write(content)
                            open_file.close()
                    except:
                        e = sys.exc_info()[0]
                        print("ERROR: " + str(e) + " at file name: " +
                              filename + " while changing line endings")
                        continue
                    try:
                        with open(file_path, "r+", encoding="utf-8") as fileToStyle:
                            linesEdited = styliseCode(fileToStyle) + linesEdited
                    except UnicodeDecodeError as e:
                        print("ERROR: while decoding file " + file_path + " the file is NOT a UTF-8 encoded file, Skipping file.")
                        continue
                    except (KeyboardInterrupt, SystemExit):
                        print("exiting...")
                        sys.exit()
                else:
                    continue


        endTime = time.time()
        print("\n")
        print("{:=^80}".format(" SUMMARY "))
        print("Please check all macros once again, that is where most of the errors will be.")
        print("Added braces %d times in %d files." % (linesEdited, fileNo))

        timeInSec = time.gmtime(endTime - startTime).tm_sec
        if timeInSec == 0:
            timeTaken = int(round(endTime - startTime, 3)* 1000)
            print("{:=^80}".format(f" DONE in {timeTaken} milliseconds "))
        else:
            timeTaken = timeInSec
            print("{:=^80}".format(f" DONE in {timeTaken} seconds "))
        
        print("\n")

if __name__ == "__main__":
    main()
