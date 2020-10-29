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

group.add_argument('-f', '--file', metavar=" file-name", dest="FILE_NAME", help="name of file to format", type=str)
group.add_argument('-d', '--directory', metavar=" directory-name",dest="DIR_NAME", help="directory name, under which to format all files", type=str)

DEFINE_PATTERN = r"#\s*\b(define)\b"


def styliseCode(fileToEdit):
    # lines edited in this file
    linesEdited = 0

    fileToEdit.seek(0)
    lines = fileToEdit.readlines()
    lineIndex = -1  # so that first line's index is 0

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
                print("Error while checking comments, at line " +
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
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, isMultiline=isMultiline, 
                                                    keywordIndex=forLoopIndex)[0]
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
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=whileLoopIndex, 
                                                    isMultiline=isMultiline)[0]
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
                ifConditionHandler, changedLines = utils.handleKeyword(KEYWORD="if", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                    isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=ifConditionIndex, isMultiline=isMultiline)
                # print("sdf", changedLines)
                # print(ifConditionHandler)
                if ifConditionHandler == None:
                    continue
                else:
                    lines = ifConditionHandler
                    if changedLines:
                        
                        # search for next curly... get it and merge } else
                        index = lineIndex
                        closing_brace = utils.getClosingBraceLineIndex(index, lines)
                        # print("line: ", lines[closing_brace])
                        if lines[index].find("}") != -1:
                            pass
                        else:
                            for x in lines[closing_brace+1:]:
                                x = utils.trimComment(x, lines.index(x), lines).line
                                # print("lin: ",x)

                                if x.isspace() or len(x) == 0:
                                    continue
                                elif x.find("else") == utils.getFirstCharacterIndex(x) and changedLines:
                                    # print(x) 
                                    lines[closing_brace - 1] = ""
                                    spaces = ""
                                    for i in x:
                                        if i.isspace():
                                            spaces += i
                                        else:
                                            break
                                    new_ln = spaces + "} " + x.lstrip()
                                    # print(new_ln)
                                    ind = lines.index(x)
                                    lines[ind] = ""
                                    lines.insert(ind, new_ln)
                                    break
                                elif not x.isspace() or len(x) != 0:
                                    # print("hereo hereo")
                                    break
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
                elseConditionHandler, changedLines = utils.handleKeyword(KEYWORD="else -", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, 
                                                keywordIndex=startingCurlyBraceIndex, isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    if line.find("if") != -1:
                        # print("else if honolul") 
                        if changedLines:
                            # search for next curly... get it and merge } else
                            index = lineIndex
                            closing_brace = utils.getClosingBraceLineIndex(index, lines)
                            # print("lineas: ", lines[closing_brace])
                            # print("lineas2.0: ", lines[index])

                            for x in lines[closing_brace+1:]:
                                x = utils.trimComment(x, lines.index(x), lines).line
                                # print("linas: ",x)
                                if x.isspace() or len(x) == 0:
                                    continue
                                elif x.find("else") == utils.getFirstCharacterIndex(x) and changedLines:
                                    # print("here")
                                    lines[closing_brace] = ""
                                    spaces = ""
                                    for i in x:
                                        if i.isspace():
                                            spaces += i
                                        else:
                                            break
                                    new_ln = spaces + "} " + x.lstrip()
                                    # print(new_ln)
                                    ind = lines.index(x)
                                    lines[ind] = ""
                                    lines.insert(ind, new_ln)
                                    break
                                elif not x.isspace() or len(x) != 0:
                                    # print("hereo hereo")
                                    break

                    linesEdited = linesEdited + 1
            elif startingElseIndex == firstCharIndex and not lineStartsOnBrace:
                # we have an else

                elseConditionHandler, changedLines = utils.handleKeyword(KEYWORD="else -", line=line, lineIndex=lineIndex, lines=lines, fileToEdit=fileToEdit,
                                                isMacro=isMacro,currentLineIsComment=currentLineIsComment, commentOfCurrentLine=commentOfCurrentLine, keywordIndex=startingElseIndex, 
                                                isMultiline=isMultiline)
                if elseConditionHandler == None:
                    continue
                else:
                    lines = elseConditionHandler
                    if line.find("if") != -1:
                        # print("else if honolul")
                        if changedLines:
                            # search for next curly... get it and merge } else
                            index = lineIndex
                            closing_brace = utils.getClosingBraceLineIndex(index, lines)
                            # print("line: ", lines[closing_brace])

                            for x in lines[closing_brace+1:]:
                                x = utils.trimComment(x, lines.index(x), lines).line
                                # print("lin: ",x)
                                if x.isspace() or len(x) == 0:
                                    continue
                                elif x.find("else") == utils.getFirstCharacterIndex(x) and changedLines:
                                    # print("here")
                                    # print(x)
                                    lines[closing_brace] = ""
                                    spaces = ""
                                    for i in x:
                                        if i.isspace():
                                            spaces += i
                                        else:
                                            break
                                    new_ln = spaces + "} " + x.lstrip()
                                    # print(new_ln)
                                    ind = lines.index(x)
                                    lines[ind] = ""
                                    lines.insert(ind, new_ln)
                                    break
                                elif not x.isspace() or len(x) != 0:
                                    # print("hereo hereo")
                                    break
                        linesEdited = linesEdited + 1
            # ---------------------------------------------------------------------------
        except utils.CommentError:
            print(f"Found a comment inside Parentheses in {fileToEdit.name} around line {lineIndex+1}, skipping line!")
            continue
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except:
            print(f"Error in file:{fileToEdit.name} around line:{str(lineIndex + 1)}, skipping line!")
            continue

    # write lines back to fileToEdit
    fileToEdit.seek(0)
    fileToEdit.writelines(lines)
    fileToEdit.close()

    return linesEdited


def main():
    VERSION_NUMBER = "0.12 "
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
    print("Made in Python 3.7.7 64-Bit")
    print("Copyright (c) 2020, Pranjal Rastogi\nAll Rights Reserved.")
    print("{:=^80}".format(""))
    if isFileGiven:
        print("Will stylise code in " + FILE_NAME + " if it is a C-Source (.c) file")
    else:
        print("Will stylise code in all C-Source code (.c) files under " + DIR_NAME)
    time.sleep(2)

    startTime = time.time()
    print("\n" + "{:=^80}".format(" START "))
    if isFileGiven:
        file_path = os.path.abspath(FILE_NAME)
        fileExtension = FILE_NAME.split(".", 1)
        if len(fileExtension) != 2:
            print("ERROR: Given file is not a (C) source code file")
            sys.exit()
        fileExt = fileExtension[1]
        if fileExt == "c" or fileExt == "h":
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
            except UnicodeDecodeError:
                print("ERROR: while decoding file " + FILE_NAME + " the file is NOT a UTF-8 encoded file, Skipping file!")
                sys.exit()
            except (KeyboardInterrupt, SystemExit):
                sys.exit()
            except:
                print("ERROR: at file name: " + FILE_NAME)
                sys.exit()
        else:
            print("ERROR: Given file is not a (C) source code file")
            sys.exit()
    else:
        for root, _, files in os.walk(DIR_NAME):
            for filename in files:
                file_path = os.path.join(root, filename)
                fileExtension = filename.split(".", 1)
                if len(fileExtension) != 2:
                    continue
                fileExt = fileExtension[1]
                if fileExt == "c" or fileExt == "h":
                    fileNo = fileNo + 1
                    try:
                        with open(file_path, 'rb') as open_file:
                            content = open_file.read()
                            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
                        with open(file_path, 'wb') as open_file:
                            open_file.write(content)
                            open_file.close()
                    except:
                        print("ERROR: at file name: " +
                                filename)
                        continue
                    try:
                        with open(file_path, "r+", encoding="utf-8") as fileToStyle:
                                linesEdited = styliseCode(fileToStyle) + linesEdited
                    except UnicodeDecodeError:
                        print("ERROR: while decoding file " + file_path + " the file is NOT a UTF-8 encoded file, Skipping file!")
                        continue
                    except (KeyboardInterrupt, SystemExit):
                        fileToStyle.close()
                        sys.exit()
                else:
                    continue


    endTime = time.time()
    print("\n")
    timeInSec = time.gmtime(endTime - startTime).tm_sec
    if timeInSec == 0:
        timeTaken = int(round(endTime - startTime, 3)* 1000)
        print(f"Took {timeTaken} milliseconds to add braces {linesEdited} time(s) in {fileNo} file(s)")
    else:
        timeTaken = timeInSec
        print(f"Took {timeTaken} seconds to add braces {linesEdited} time(s) in {fileNo} file(s)")
    print("\n")

if __name__ == "__main__":
    main()
