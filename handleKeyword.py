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
# handleKeyword.py
# The brain for CodeStyliser.py
# ---

import utilities as utils
import re
import models
import exceptions


def handle_keyword(keyword, line, line_index, lines, file_to_edit, is_macro, is_current_line_comment,
                   comment_of_current_line, is_multiline, keyword_index):
    # found a  "KEYWORD"
    error_print_data = (keyword, (line_index + 1), file_to_edit.name)
    has_hash = utils.check_for_hash(line_index, lines)
    if has_hash != -1:
        # has hash
        if line.find("{") != -1:
            # has {
            return None
        else:
            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line" % error_print_data)
        raise exceptions.HashIgnore

    # we must now skip over all parentheses to find the end of the (condition)
    if keyword == "else -":
        if line.find("if") != -1:
            # line is else if
            is_else_if = True
            check_parenth_result = utils.check_for_parentheses(line, line_index, lines, "p")
        else:
            is_else_if = False
            check_parenth_result = models.ParenthResult(True, line_index, None)
    else:
        is_else_if = False
        check_parenth_result = utils.check_for_parentheses(line, line_index, lines, "p")

    if check_parenth_result is None:
        print("ERROR: While checking parentheses: ignored %s loop/ condition at %d in file %s" % error_print_data)

        # raise ParenthesesCheckingError
        return None

    elif not check_parenth_result.isOnSameLine:
        # (condition) doesnt end on same line
        is_on_same_line = check_parenth_result.isOnSameLine
        nxt_ln_index = check_parenth_result.lineIndex
        next_line_index = nxt_ln_index
        open_curly_brace_index = lines[nxt_ln_index - 1][check_parenth_result.lastCloseParenthIndex:].find("{")
        if not is_else_if and keyword == "else -":
            last_close_parenth_index = 0
        else:
            last_close_parenth_index = check_parenth_result.lastCloseParenthIndex + 2

    else:
        # (condition) ends on same line
        is_on_same_line = check_parenth_result.isOnSameLine
        next_line_index = line_index + 1
        open_curly_brace_index = line[check_parenth_result.lastCloseParenthIndex:].find("{")
        if not is_else_if and keyword == "else -":
            last_close_parenth_re = re.search(r"\b(else)\b", line)
            if last_close_parenth_re:
                last_close_parenth_index = last_close_parenth_re.end()
            else:
                last_close_parenth_index = -1
        else:
            last_close_parenth_index = check_parenth_result.lastCloseParenthIndex + 1

    if open_curly_brace_index == -1 and utils.check_for_open_brace(next_line_index, lines)[0] == -1:

        # no { on same line and on subsequent lines, we must add {} if possible        

        if is_on_same_line:
            last_semi_colon_index = line[last_close_parenth_index:].find(";")
            is_back_slash_present = line.rstrip()[-1] == "\\"
            if is_back_slash_present:
                # backSLASH!
                if last_semi_colon_index != -1:
                    # semicolon found on same line
                    if is_current_line_comment:
                        if is_multiline:
                            to_add_line = comment_of_current_line + line[:last_close_parenth_index] + \
                                          " { " + line[
                                                  last_close_parenth_index:(last_semi_colon_index +
                                                                            len(line[:last_close_parenth_index]) + 1)] \
                                          + " } " + line[(last_semi_colon_index + len(line[:last_close_parenth_index])
                                                          + 1):].rstrip() + "\n"
                        else:
                            to_add_line = line[:last_close_parenth_index] + " { " + \
                                          line[last_close_parenth_index:(last_semi_colon_index
                                                                         + len(line[:last_close_parenth_index]) + 1)] \
                                          + " } " + line[(last_semi_colon_index + len(line[:last_close_parenth_index])
                                                          + 1):] + comment_of_current_line + "\n"
                    else:
                        to_add_line = line[:last_close_parenth_index] + " { " + \
                                      line[last_close_parenth_index:(last_semi_colon_index +
                                                                     len(line[:last_close_parenth_index]) + 1)] + \
                                      " } " + line[(last_semi_colon_index + len(line[:last_close_parenth_index]) +
                                                    1):].rstrip() + "\n"

                        # insert toAddLine and return
                    del lines[line_index]
                    lines.insert(line_index, to_add_line)
                    return lines
                elif last_semi_colon_index == -1:
                    if is_current_line_comment:
                        if is_multiline:
                            to_add_line = comment_of_current_line + line.rstrip()[:-1] + " { \\" + "\n"
                        else:
                            to_add_line = line.rstrip() + " { " + comment_of_current_line + "\\\n"
                    else:
                        to_add_line = line.rstrip()[:-1] + " { \\\n"
                    del lines[line_index]
                    lines.insert(line_index, to_add_line)
                    check_for_semi_colon_index = line_index + 1
                else:
                    # raise SemiColonError
                    return None

            elif not is_back_slash_present:
                if lines[line_index - 2].isspace() or len(lines[line_index - 2]) == 0:
                    pass
                else:
                    if lines[line_index - 2].rstrip()[-1] == "\\":
                        if last_semi_colon_index == -1:
                            # not semicolon ending
                            return None
                if last_semi_colon_index == -1:
                    # if there is nothing on line except the keyword()
                    if is_current_line_comment:
                        if is_multiline:
                            to_add_line = comment_of_current_line + line.rstrip() + " { " + "\n"
                        else:
                            to_add_line = line.rstrip() + " { " + comment_of_current_line + "\n"
                    else:
                        to_add_line = line.rstrip() + " {\n"

                    del lines[line_index]
                    lines.insert(line_index, to_add_line)
                    check_for_semi_colon_index = line_index + 1

                elif last_semi_colon_index != -1:
                    # semicolon found on same line
                    if is_current_line_comment:
                        if is_multiline:
                            to_add_line = comment_of_current_line + line[:last_close_parenth_index] + " { " \
                                          + line[last_close_parenth_index:(last_semi_colon_index +
                                                                           len(line[:last_close_parenth_index]) + 1)] \
                                          + " } " + line[(last_semi_colon_index + len(line[:last_close_parenth_index])
                                                          + 1):].rstrip() + "\n"
                        else:
                            to_add_line = line[:last_close_parenth_index] + " { " + line[last_close_parenth_index:(
                                    last_semi_colon_index + len(line[:last_close_parenth_index]) + 1)] + " } " \
                                          + line[(last_semi_colon_index + len(line[:last_close_parenth_index]) + 1):] \
                                          + comment_of_current_line + "\n"
                    else:
                        to_add_line = line[:last_close_parenth_index] + " { " + line[last_close_parenth_index:(
                                last_semi_colon_index + len(line[:last_close_parenth_index]) + 1)] + " } " \
                                      + line[(last_semi_colon_index
                                              + len(line[:last_close_parenth_index]) + 1):].rstrip() \
                                      + "\n"

                        # insert toAddLine and return
                    del lines[line_index]
                    lines.insert(line_index, to_add_line)
                    return lines
                else:
                    # raise SemiColonError
                    return None
            else:
                # raise BackSlashError
                return None
        else:
            # the (condition) doesnt end on same line
            is_back_slash_present = lines[nxt_ln_index - 1].rstrip()[-1] == "\\"
            last_semi_colon_index = lines[nxt_ln_index - 1][last_close_parenth_index:].find(";")
            if is_back_slash_present:

                if last_semi_colon_index != -1:
                    # same line semicolon
                    nxt_ln_trim_comment = utils.trim_comment(lines[nxt_ln_index - 1], (nxt_ln_index - 1), lines)

                    if nxt_ln_trim_comment.hasComment:
                        if nxt_ln_trim_comment.isMultiline:
                            to_add_line = nxt_ln_trim_comment.comment + \
                                          nxt_ln_trim_comment.line[:last_close_parenth_index] + \
                                          " { " + nxt_ln_trim_comment.line[last_close_parenth_index:].rstrip()[:-1] \
                                          + " } " + "\\\n"
                        else:
                            to_add_line = nxt_ln_trim_comment.line[:last_close_parenth_index] + \
                                          " { " + nxt_ln_trim_comment.line[last_close_parenth_index:].rstrip() + \
                                          " } " + nxt_ln_trim_comment.comment + "\\\n"
                    else:
                        to_add_line = lines[nxt_ln_index - 1][:last_close_parenth_index] + " { " + \
                                      lines[nxt_ln_index - 1][last_close_parenth_index:].rstrip()[:-1] + " } \\\n"

                    has_hash = utils.check_for_hash(nxt_ln_index - 1, lines)
                    if has_hash != -1:
                        # has hash
                        if lines[nxt_ln_index - 1].find("{") != -1:
                            # has {
                            # return CurlyBracesPresent
                            return None
                        else:
                            print("WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line"
                                  % error_print_data)
                        # return HashError
                        return None

                    del lines[nxt_ln_index - 1]
                    lines.insert(nxt_ln_index - 1, to_add_line)
                    return lines

                elif last_semi_colon_index == -1:
                    nxt_ln_trim_comment = utils.trim_comment(lines[nxt_ln_index - 1], (nxt_ln_index - 1), lines)

                    if nxt_ln_trim_comment.hasComment:
                        if nxt_ln_trim_comment.isMultiline:
                            to_add_line = nxt_ln_trim_comment.comment + nxt_ln_trim_comment.line.rstrip()[:-1] \
                                          + " { " + "\\\n"
                        else:
                            to_add_line = nxt_ln_trim_comment.line.rstrip() + " { " + nxt_ln_trim_comment.comment \
                                          + "\\\n"
                    else:
                        to_add_line = lines[nxt_ln_index - 1].rstrip()[:-1] + " { \\\n"

                    has_hash = utils.check_for_hash(nxt_ln_index - 1, lines)
                    if has_hash != -1:
                        # has hash
                        if lines[nxt_ln_index - 1].find("{") != -1:
                            # has {
                            # raise CurlyBracePresent
                            return None
                        else:
                            print(
                                "WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line"
                                % error_print_data)
                            # return HashError
                            return None

                    del lines[nxt_ln_index - 1]
                    lines.insert(nxt_ln_index - 1, to_add_line)
                    check_for_semi_colon_index = nxt_ln_index
            elif not is_back_slash_present:

                if lines[nxt_ln_index - 2].isspace() or len(lines[nxt_ln_index - 2]) == 0:
                    pass
                else:
                    if lines[nxt_ln_index - 2].rstrip()[-1] == "\\":
                        if last_semi_colon_index == -1:
                            # not semicolon ending
                            return None

                if last_semi_colon_index == -1:
                    nxt_ln_trim_comment = utils.trim_comment(lines[nxt_ln_index - 1], (nxt_ln_index - 1), lines)

                    if nxt_ln_trim_comment.hasComment:
                        if nxt_ln_trim_comment.isMultiline:
                            to_add_line = nxt_ln_trim_comment.comment + nxt_ln_trim_comment.line.rstrip() + " { " + "\n"
                        else:
                            to_add_line = nxt_ln_trim_comment.line.rstrip() + " { " + nxt_ln_trim_comment.comment + "\n"
                    else:
                        to_add_line = lines[nxt_ln_index - 1].rstrip() + " {\n"

                    has_hash = utils.check_for_hash(nxt_ln_index - 1, lines)
                    if has_hash != -1:
                        # has hash
                        if lines[nxt_ln_index - 1].find("{") != -1:
                            # has {
                            # raise HasCurlyBrace
                            return None
                        else:
                            print(
                                "WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line"
                                % error_print_data)
                            # raise HashError
                            return None

                    del lines[nxt_ln_index - 1]
                    lines.insert(nxt_ln_index - 1, to_add_line)
                    check_for_semi_colon_index = nxt_ln_index

                elif last_semi_colon_index != -1:
                    nxt_ln_trim_comment = utils.trim_comment(lines[nxt_ln_index - 1], (nxt_ln_index - 1), lines)

                    if nxt_ln_trim_comment.hasComment:
                        if nxt_ln_trim_comment.isMultiline:
                            to_add_line = nxt_ln_trim_comment.comment + \
                                          nxt_ln_trim_comment.line[:last_close_parenth_index] + \
                                          " { " + nxt_ln_trim_comment.line[last_close_parenth_index:].rstrip() \
                                          + " } " + "\n"
                        else:
                            to_add_line = nxt_ln_trim_comment.line[:last_close_parenth_index] + \
                                          " { " + nxt_ln_trim_comment.line[last_close_parenth_index:].rstrip() + \
                                          " } " + nxt_ln_trim_comment.comment + "\n"
                    else:
                        to_add_line = lines[nxt_ln_index - 1][:last_close_parenth_index] + " { " + \
                                      lines[nxt_ln_index - 1][last_close_parenth_index:].rstrip() + " }\n"

                    has_hash = utils.check_for_hash(nxt_ln_index - 1, lines)
                    if has_hash != -1:
                        # has hash
                        if lines[nxt_ln_index - 1].find("{") != -1:
                            # has {
                            # raise CurlyBracePresent
                            return None
                        else:
                            print(
                                "WARN: Ignored %s loop/ condition at line %d in %s as \'#\' found in next line"
                                % error_print_data)
                            # raise HashError
                            return None

                    del lines[nxt_ln_index - 1]
                    lines.insert(nxt_ln_index - 1, to_add_line)
                    return lines
                else:
                    # raise SemiColonError
                    return None
            else:
                # raise SemiColonError
                return None

        closing_brace_line_index = utils.get_closing_brace_line_index(check_for_semi_colon_index, lines)
        if closing_brace_line_index is None:
            print("FATAL ERROR: ignored %s loop/ condition at %d in file %s" % error_print_data)
            # raise FatalError
            return None
        else:
            # nxt_ln_else = False
            # add closing braces at closingBraceLine (inserting a new ln) with indentation
            if is_multiline:
                spaces = " " * (keyword_index + len(comment_of_current_line))
            else:
                spaces = " " * keyword_index
            if len(lines[closing_brace_line_index - 1].strip()) == 0 or \
                    len(lines[closing_brace_line_index - 2].strip()) == 0:
                # line be empty
                add_closing_brace_line = spaces + "}\n"
            else:
                if lines[closing_brace_line_index - 1].rstrip()[-1] == "\\":
                    # we found \
                    add_closing_brace_line = spaces + "} \\\n"
                elif lines[closing_brace_line_index - 2].rstrip()[-1] == "\\":
                    to_add_back_slash = lines[closing_brace_line_index - 1].rstrip() + " \\\n"
                    del lines[closing_brace_line_index - 1]
                    lines.insert(closing_brace_line_index - 1, to_add_back_slash)
                    add_closing_brace_line = spaces + "}\n"
                else:
                    add_closing_brace_line = spaces + "}\n"
                    # if lines[closing_brace_line_index].find("else") != -1:
                    #     add_closing_brace_line = spaces + "} "
                    #     add_closing_brace_line = add_closing_brace_line + lines[closing_brace_line_index][
                    #                                                       (len(add_closing_brace_line) - 2):]
                    #     nxt_ln_else = True

            # if not nxt_ln_else:
            lines.insert(closing_brace_line_index, "")
            lines.insert(closing_brace_line_index, add_closing_brace_line)
            # else:
            #     del lines[closing_brace_line_index]
            #     lines.insert(closing_brace_line_index, add_closing_brace_line)
            return lines
