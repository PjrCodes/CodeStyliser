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
import argparse

parser = argparse.ArgumentParser(description='The Code Styliser Utility,\nCreated by Pranjal Rastogi. Copyright (c) 2020, Pranjal Rastogi\n All rights Reserved')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-f', '--file', metavar=" file-name", dest="FILE_NAME", help="file name to format", type=str)
group.add_argument('-d', '--directory', metavar=" directory-name",dest="DIR_NAME", help="directory to format files under", type=str)



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
        except utils.CommentError:
            print(f"WARN: Found a comment inside Parentheses in {fileToEdit.name} around line {lineIndex+1}, skipping line!!")
            continue
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except:
            e = sys.exc_info()[0]
            print("FATAL ERROR: " + str(e) + " in file name: " +
                  fileToEdit.name + " around line " + str(lineIndex + 1) + ", skipping line!!")
            continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()
    return linesEdited


def main():
    VERSION_NUMBER = "0.1.10.4-BETA "
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    isFileGiven = False
    args = parser.parse_args()
    DIR_NAME = args.DIR_NAME
    FILE_NAME = args.FILE_NAME
    fileNo = 0
    linesEdited = 0

    if FILE_NAME != None:
        isFileGiven = True
    else:
        isFileGiven = False



    print("\n")
    print("{:=^80}".format(" Welcome to CodeStyliser ver" + VERSION_NUMBER))
    print("Made by Pranjal Rastogi, in Python 3.7.7 64-Bit")
    print("Copyright (c) 2020, Pranjal Rastogi\n All rights Reserved")
    print("{:=^80}".format(""))
    if isFileGiven:
        print("Will stylise code in " + FILE_NAME + " if it is a C-Source (.c) file")
    else:
        print("Will stylise code in C-Source code (.c) files under " + DIR_NAME)
    time.sleep(2)

    startTime = time.time()
    print("\n" + "{:=^80}".format(" START "))
    if isFileGiven:
        file_path = os.path.abspath(FILE_NAME)
        fileExtension = FILE_NAME.split(".", 1)
        if len(fileExtension) != 2:
            print("ERROR, Given file is not a (C) source code file")
            sys.exit()
        fileExt = fileExtension[1]
        if fileExt == "c":
            try:
                fileNo += 1
                with open(file_path, 'rb') as open_file:
                    content = open_file.read()
                    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
                with open(file_path, 'wb') as open_file:
                    open_file.write(content)
                    open_file.close()
                with open(file_path, "r+", encoding="utf-8") as fileToStyle:
                    linesEdited = styliseCode(fileToStyle) + linesEdited
            except FileNotFoundError:
                print(f"ERROR: Given filename, {FILE_NAME} not found!")
                sys.exit()
            except FileNotFoundError:
                print(f"ERROR: Given filename, {FILE_NAME} not found!")
                sys.exit()
            except UnicodeDecodeError as e:
                print("ERROR: while decoding file " + FILE_NAME + " the file is NOT a UTF-8 encoded file, Skipping file...")
                print(e)
                sys.exit()
            except (KeyboardInterrupt, SystemExit):
                sys.exit()
            except:
                e = sys.exc_info()[0]
                print("ERROR: " + str(e) + " at file name: " + FILE_NAME)
                sys.exit()
        else:
            print("ERROR, Given file is not a (C) source code file")
            sys.exit()
    else:
        for root, _, files in os.walk(DIR_NAME):
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
                        print("ERROR: while decoding file " + file_path + " the file is NOT a UTF-8 encoded file, Skipping file...")
                        print(e)
                        continue
                    except (KeyboardInterrupt, SystemExit):
                        sys.exit()
                else:
                    continue


    endTime = time.time()
    print("\n")
    timeInSec = time.gmtime(endTime - startTime).tm_sec
    if timeInSec == 0:
        timeTaken = int(round(endTime - startTime, 3)* 1000)
        print(f"Took {timeTaken} milliseconds to add braces {linesEdited} times in {fileNo} files")
    else:
        timeTaken = timeInSec
        print(f"Took {timeTaken} seconds to add braces {linesEdited} times in {fileNo} files")
    print("\n")

if __name__ == "__main__":
    main()
