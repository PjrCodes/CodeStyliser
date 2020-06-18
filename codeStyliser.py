#!/usr/local/bin/python3
# Made in python 3.7.7 64 bit, use only this version
# ---
# Copyright (c) 2020, Pranjal Rastogi
# All rights reserved.
# Do not copy this code without permission
# check LICENSE for more details
# ---
# Part of The codeStyliser utility
# ---
# codeStyliser.py
# Starting point of the application
# ---


import sys
import re
import os
import utilities as utils
import exceptions
import time
import handleKeyword
import constants as consts
import argparse

parser = argparse.ArgumentParser(description="The Code Styliser Utility, An utility that helps you add curly braces in "
                                             "C source code, wherever needed!",
                                 epilog="Copyright (c) 2020, Pranjal Rastogi. All rights reserved.")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-f', '--file', metavar="file-name",
                   dest="FILE_NAME", help="file name to format", type=str)
group.add_argument('-d', '--directory', metavar="directory-name",
                   dest="DIR_NAME", help="directory to format files under", type=str)


def stylise_code(file_to_edit):
    # lines edited in this file
    lines_edited = 0
    # so that first line's index is 0

    file_to_edit.seek(0)
    lines = file_to_edit.readlines()
    line_index = -1
    while line_index < (len(lines) - 1):

        # try:
        # increment line count
        line_index = line_index + 1
        current_line_is_comment = False
        is_multiline = False
        comment_of_current_line = ""
        # search for comments
        trimmed_comment_result = utils.trim_comment(
            lines[line_index], line_index, lines)
        line = trimmed_comment_result.line

        if trimmed_comment_result.hasComment is True and trimmed_comment_result.isMultiline is False:
            current_line_is_comment = True
            comment_of_current_line = trimmed_comment_result.comment
        elif trimmed_comment_result.isMultiline:
            is_multiline = trimmed_comment_result.isMultiline
            current_line_is_comment = trimmed_comment_result.hasComment
            comment_of_current_line = trimmed_comment_result.comment
            # if comment, jump
            line_index = trimmed_comment_result.multiLineJumpIndex
            line = trimmed_comment_result.line
        elif not trimmed_comment_result.hasComment:
            current_line_is_comment = False
            is_multiline = False
            comment_of_current_line = trimmed_comment_result.comment
        else:
            print("FATAL ERROR: in comment checking, at line " +
                  str(line_index) + " file: " + file_to_edit.name)
            continue

        first_char_index = utils.get_first_character_index(line)

        if re.search(consts.DEFINE_PATTERN, line):
            is_macro = True
            if line.rfind("\\") != -1:
                # found \ at the back of the line
                pass
            else:
                # ignore line
                continue
        else:
            is_macro = False

        # ---------------------------------------------------------------------------
        # find for loops
        for_loop_match = re.search(r"\b(for)\b", line)
        if for_loop_match:
            for_loop_index = for_loop_match.start()
        else:
            for_loop_index = -1

        if for_loop_index == first_char_index:
            for_loop_handler = handleKeyword.handle_keyword(keyword="for", line=line, line_index=line_index, lines=lines,
                                                            file_to_edit=file_to_edit,
                                                            is_macro=is_macro,
                                                            is_current_line_comment=current_line_is_comment,
                                                            comment_of_current_line=comment_of_current_line,
                                                            is_multiline=is_multiline, keyword_index=for_loop_index)
            if for_loop_handler is None:
                continue
            else:
                lines = for_loop_handler
                lines_edited = lines_edited + 1

        # ---------------------------------------------------------------------------

        # find while loops
        while_loop_match = re.search(r"\b(while)\b", line)
        if while_loop_match:
            while_loop_index = while_loop_match.start()
        else:
            while_loop_index = -1

        if while_loop_index == first_char_index:
            while_loop_handler = handleKeyword.handle_keyword(keyword="while", line=line, line_index=line_index,
                                                              lines=lines, file_to_edit=file_to_edit,
                                                              is_macro=is_macro,
                                                              is_current_line_comment=current_line_is_comment,
                                                              comment_of_current_line=comment_of_current_line,
                                                              keyword_index=while_loop_index, is_multiline=is_multiline)
            if while_loop_handler is None:
                continue
            else:
                lines = while_loop_handler
                lines_edited = lines_edited + 1

        # ---------------------------------------------------------------------------

        # find if conditions
        if_condition_match = re.search(r"\b(if)\b", line)
        if if_condition_match:
            if_condition_index = if_condition_match.start()
        else:
            if_condition_index = -1

        if if_condition_index == first_char_index:
            if_condition_handler = handleKeyword.handle_keyword(keyword="if", line=line, line_index=line_index,
                                                                lines=lines, file_to_edit=file_to_edit,
                                                                is_macro=is_macro,
                                                                is_current_line_comment=current_line_is_comment,
                                                                comment_of_current_line=comment_of_current_line,
                                                                keyword_index=if_condition_index,
                                                                is_multiline=is_multiline)
            if if_condition_handler is None:
                continue
            else:
                lines = if_condition_handler
                lines_edited = lines_edited + 1

        # ---------------------------------------------------------------------------
        # find else conditions
        starting_curly_brace_index = line.find("}")
        line_starts_on_brace = False
        else_condition_match = re.search(r"\b(else)\b", line)
        if else_condition_match:
            starting_else_index = else_condition_match.start()
        else:
            starting_else_index = -1

        if starting_curly_brace_index == first_char_index:
            # line starts on a }
            line_starts_on_brace = True

        if line_starts_on_brace and starting_else_index != -1:
            # we have a line with an } and an else after it
            # process else
            else_condition_handler = handleKeyword.handle_keyword(keyword="else -", line=line,
                                                                  line_index=line_index,
                                                                  lines=lines,
                                                                  file_to_edit=file_to_edit,
                                                                  is_macro=is_macro,
                                                                  is_current_line_comment=current_line_is_comment,
                                                                  comment_of_current_line=comment_of_current_line,
                                                                  keyword_index=starting_curly_brace_index,
                                                                  is_multiline=is_multiline)
            if else_condition_handler is None:
                continue
            else:
                lines = else_condition_handler
                lines_edited = lines_edited + 1
        elif starting_else_index == first_char_index and not line_starts_on_brace:
            # we have an else
            else_condition_handler = handleKeyword.handle_keyword(keyword="else -", line=line,
                                                                  line_index=line_index,
                                                                  lines=lines,
                                                                  file_to_edit=file_to_edit,
                                                                  is_macro=is_macro,
                                                                  is_current_line_comment=current_line_is_comment,
                                                                  comment_of_current_line=comment_of_current_line,
                                                                  keyword_index=starting_else_index,
                                                                  is_multiline=is_multiline)
            if else_condition_handler is None:
                continue
            else:
                lines = else_condition_handler
                lines_edited = lines_edited + 1
        # ---------------------------------------------------------------------------
        # except exceptions.CommentError:
        #     print(f"WARN: Found a comment inside Parentheses in {fileToEdit.name} around line {line_index+1}, \
        #     skipping line!!")
        #     continue
        # except (KeyboardInterrupt, SystemExit):
        #     sys.exit()
        # except:
        #     e = sys.exc_info()[0]
        #     print("FATAL ERROR: " + str(e) + " in file name: " +
        #           fileToEdit.name + " around line " + str(line_index + 1) + ", skipping line!!")
        #     continue

    # write lines back to fileToEdit
    file_to_edit.seek(0)
    file_to_edit.writelines(lines)
    file_to_edit.close()
    return lines_edited


def main():
    is_file_given = False
    args = parser.parse_args()
    given_dir_name = args.DIR_NAME
    given_file_name = args.FILE_NAME
    file_no = 0
    lines_edited = 0

    if given_file_name is not None:
        is_file_given = True
    else:
        is_file_given = False

    print("\n")
    print("{:=^80}".format(" Welcome to CodeStyliser ver" + consts.VERSION_NUMBER))
    print("EXPERIMENTAL VERSION. ERRORS MAY DEFINETLY ARISE")
    print("Made by Pranjal Rastogi, in Python 3.7.7 64-Bit")
    print("Copyright (c) 2020, Pranjal Rastogi\nAll Rights Reserved.")
    print("{:=^80}".format("EXPERIMENTAL"))

    if is_file_given:
        print("Will stylise code in " + given_file_name +
              " if it is a C-Source (.c) file/ a Header file(.h)")
    else:
        print("Will stylise code in C-Source code (.c)/ Header (.h) files under " + given_dir_name)
    time.sleep(2)

    start_time = time.time()
    print("\n" + "{:=^80}".format(" START "))
    if is_file_given:
        file_path = os.path.abspath(given_file_name)
        file_extension = given_file_name.split(".", 1)
        file_ext = file_extension[1]
        if len(file_extension) != 2:
            print("ERROR, Given file is not a (C) source code file")
            sys.exit()
        if file_ext == "c" or file_ext == "h":
            # try:
            file_no += 1
            with open(file_path, 'rb') as open_file:
                content = open_file.read()
                content = content.replace(
                    consts.WINDOWS_LINE_ENDING, consts.UNIX_LINE_ENDING)
            with open(file_path, 'wb') as open_file:
                open_file.write(content)
                open_file.close()
            with open(file_path, "r+", encoding="utf-8") as fileToStyle:
                lines_edited = stylise_code(fileToStyle) + lines_edited
            # except FileNotFoundError:
            #     print(f"ERROR: Given filename, {givenFileName} not found!")
            #     sys.exit()
            # except FileNotFoundError:
            #     print(f"ERROR: Given filename, {givenFileName} not found!")
            #     sys.exit()
            # except UnicodeDecodeError as e:
            #     print("ERROR: while decoding file " + givenFileName + " the file is NOT a UTF-8 encoded file,\
            #     Skipping file...")
            #     print(e)
            #     sys.exit()
            # except (KeyboardInterrupt, SystemExit):
            #     sys.exit()
            # except:
            #     e = sys.exc_info()[0]
            #     print("ERROR: " + str(e) + " at file name: " + givenFileName)
            #     sys.exit()
        else:
            print("ERROR, Given file is not a (C) source code/ (h) file file")
            sys.exit()
    else:
        for root, _, files in os.walk(given_dir_name):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_extension = filename.split(".", 1)
                if len(file_extension) != 2:
                    continue
                file_ext = file_extension[1]
                if file_ext == "c" or file_ext == "h":
                    file_no = file_no + 1
                    try:
                        with open(file_path, 'rb') as open_file:
                            content = open_file.read()
                            content = content.replace(
                                consts.WINDOWS_LINE_ENDING, consts.UNIX_LINE_ENDING)
                        with open(file_path, 'wb') as open_file:
                            open_file.write(content)
                            open_file.close()
                    except:
                        e = sys.exc_info()[0]
                        print("ERROR: " + str(e) + " at file name: " +
                              filename + " while changing line endings")
                        continue
                    # try:
                    with open(file_path, "r+", encoding="utf-8") as fileToStyle:
                        lines_edited = stylise_code(fileToStyle) + lines_edited
                    # except UnicodeDecodeError as e:
                    #     print("ERROR: while decoding file " + file_path + " the file is NOT a UTF-8 encoded file, \
                    #     Skipping file...")
                    #     print(e)
                    #     continue
                    # except (KeyboardInterrupt, SystemExit):
                    #     sys.exit()
                else:
                    continue

    end_time = time.time()
    print("\n")
    time_in_sec = time.gmtime(end_time - start_time).tm_sec
    if time_in_sec == 0:
        time_taken = int(round(end_time - start_time, 3) * 1000)
        print(
            f"Took {time_taken} milliseconds to add braces {lines_edited} time(s) in {file_no} file(s)")
    else:
        time_taken = time_in_sec
        print(
            f"Took {time_taken} seconds to add braces {lines_edited} time(s) in {file_no} file(s)")
    print("\n")


if __name__ == "__main__":
    main()
