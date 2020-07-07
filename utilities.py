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
# utilities.py
# utility functions for the codeStyliser utility
# ---


# TODO: use logger
# TODO: use EXCEPTIONS in a SMARTER WAY!!!

# HACK:FIXME: EVERYTHING IS A HACK!!!


import re
import sys
import exceptions
import models
import constants as consts


def trim_comment(line, line_no, lines):
    search_for_single_line_comment = re.search(consts.SINGLE_LINE_COMMENT_PATTERN, line)
    if search_for_single_line_comment:
        if search_for_single_line_comment.group()[0:2] == "/*":
            # keep searching for */
            same_line_end = line.find("*/")
            if same_line_end != -1:
                # ends on same line
                # TODO: ALSO CHECK IF THERE IS ANYTHING ON THE LINE AFTER THE COMMENT, IN WHICH CASE WE NEED TO DIE
                # FIXME: THIS WILL FAIL IF THERE IS SOMETHING AFTER COMMENT
                # BUG: THIS IS A BUG AS IT CAUSES AN ERROR IN COMMENT HANDLING, AND PARENTHESES COUNTING,
                #      RAISING INDEX ERROR's
                if line[(same_line_end + 1):].isspace():
                    return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                                  search_for_single_line_comment.group(), False, None)
                else:
                    # there is something after comment on line
                    return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                                  search_for_single_line_comment.group(), False, None)
            else:
                # iterate for line in lines till we get */
                index = line_no + 1
                while True:
                    multi_comment_end = lines[index].find("*/")
                    if multi_comment_end != -1:
                        # multi line comment has ended
                        return models.LineWithComment(lines[index][(multi_comment_end + 2):], True,
                                                      lines[index][:(multi_comment_end+2)], True, index)
                    else:
                        # no multi line comment end found
                        index = index + 1
                    
        # found a single line comment of type //
        return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                      search_for_single_line_comment.group(), False, None)
    else:
        # no comment
        return models.LineWithComment(line, False, "", False, None)


def get_first_character_index(given_str):
    return len(given_str) - len(given_str.lstrip())


def check_for_parentheses(line, line_index, lines, type_of_parenth):
    if type_of_parenth == "p":
        starting_parenth = '('
        ending_parenth = ')'
    if type_of_parenth == "b":
        starting_parenth = '{'
        ending_parenth = "}"
    open_parenth_no = 0
    close_parenth_no = 0
    index = 0

    while index < len(line):
        if line[index] == starting_parenth:
            open_parenth_no += 1
        if line[index] == ending_parenth:
            close_parenth_no += 1
        if open_parenth_no == close_parenth_no and open_parenth_no != 0:
            return models.ParenthResult(True, line_index, index)
        index += 1
    
    if open_parenth_no != close_parenth_no:
        # the line doesnt have same amt of close and open parentheses
        # loop through till we reach same no. of parentheses.

        nxt_ln_index = line_index + 1
        while close_parenth_no != open_parenth_no:
            if nxt_ln_index > (len(lines) - 1):
                # we never found a parentheses match!
                # this can only happen if there is syntax error, which there isn't.
                # We have already ignored Macros where this can happen
                # so, we must HAVE HIT A COMMENT!
                raise exceptions.CommentError
            # check for {} on the line
            for char in lines[nxt_ln_index]:
                if char == starting_parenth:
                    open_parenth_no += 1
                elif char == ending_parenth:
                    close_parenth_no += 1
            else:
                # after iterating through line
                nxt_ln_index += 1
        else:
            # closeParenthNo = openParenthNo
            if open_parenth_no == 0:
                return None
            # not on same line!!!
            # index is no. of characters seen, so cant return index.
            close_index = lines[nxt_ln_index - 1].find(ending_parenth)
            return models.ParenthResult(False, nxt_ln_index, close_index)


def check_for_open_brace(next_line_index, lines):

    while next_line_index < (len(lines)):
        line_without_comment = trim_comment(lines[next_line_index], next_line_index, lines)
        if line_without_comment.hasComment:
            # line has comment
            if line_without_comment.line.isspace():
                next_line_index += 1
                continue
            else:
                if re.search(consts.OPEN_BRACE_PATTERN, line_without_comment.line):
                    # if the line before comment has {
                    break
                else:
                    # there is something before line, but it is not an open brace
                    break
            if line_without_comment.isMultiline == True:
                # go after multiline comments
                next_line_index = line_without_comment.multiLineJumpIndex
                continue
            else:
                next_line_index = next_line_index + 1
                continue
        elif line_without_comment.line.isspace():
            # line is blank
            next_line_index += 1
            continue
        else:
            # line is not blank and isn't a comment
            break
    
    if re.search(consts.OPEN_BRACE_PATTERN, line_without_comment.line):
        return re.search(consts.OPEN_BRACE_PATTERN, line_without_comment.line).end(), next_line_index
    else:
        return -1, None


def check_for_hash(index, lines):
    index = index + 1
    while index < (len(lines)):
        line_without_comment = trim_comment(lines[index], index, lines)
        if line_without_comment.hasComment is True or lines[index].isspace():
            # line has comment or is blank
            if line_without_comment.isMultiline:
                # go after multiline comments
                if line_without_comment.line.find("#") != -1:
                    break
                index = line_without_comment.multiLineJumpIndex
                
            index = index + 1
        else:
            break
    return line_without_comment.line.find("#")


def get_next_semi_colon_line_index(index, lines):
    semi_colon_line_index = index
    while semi_colon_line_index < (len(lines)):
        line_without_comment = trim_comment(lines[semi_colon_line_index], semi_colon_line_index, lines)
        if line_without_comment.isMultiline:
            semi_colon_index = line_without_comment.line.find(";")
            semi_colon_line_index = line_without_comment.multiLineJumpIndex
        else:
            semi_colon_index = line_without_comment.line.find(";")
            
        if semi_colon_index == -1:
            # the line without Comment has NO semicolon
            semi_colon_line_index += 1
        else:
            # line has a semicolon and is NOT a comment
            break
    return semi_colon_line_index


def get_closing_brace_line_index(index, lines):

    # run operations on line
    keyword_line_check_index = index
    has_keyword = False
    while keyword_line_check_index < (len(lines)):

        current_line_wo_comment = trim_comment(lines[keyword_line_check_index], keyword_line_check_index, lines)
        line = current_line_wo_comment.line
        first_char_of_ln = get_first_character_index(line)
        if line.isspace() or len(line) == 0:
            if current_line_wo_comment.isMultiline:
                # jump line to after multiline comment
                keyword_line_check_index = current_line_wo_comment.multiLineJumpIndex
                continue
            else:
                keyword_line_check_index += 1
                continue
        else:
            
            if current_line_wo_comment.hasComment:
                if current_line_wo_comment.isMultiline:
                    for keyword in consts.KEYWORDS:
                        keyword_check_re = re.search(keyword, line)
                        if keyword_check_re:
                            if keyword_check_re.start() == first_char_of_ln:
                                # we found a keyword
                                cont = False
                                has_keyword = True
                                break
                            else:
                                # keyword not on first char
                                has_keyword = False
                                continue
                        else:
                            # didn't find KEYWORD
                            has_keyword = False
                            continue
                    if cont:
                        continue
                    else:
                        keyword_line_check_index = current_line_wo_comment.multiLineJumpIndex
                        break
                    keyword_line_check_index = current_line_wo_comment.multiLineJumpIndex
                    continue

                if current_line_wo_comment.line.isspace():
                    continue
                else:
                    if line.find("*/") != -1:
                        keyword_line_check_index += 1
                    for keyword in consts.KEYWORDS:
                        keyword_check_re = re.search(keyword, line)
                        if keyword_check_re:
                            if keyword_check_re.start() == first_char_of_ln:
                                # we found a keyword
                                cont = False
                                has_keyword = True
                                break
                            else:
                                # keyword not on first char
                                has_keyword = False
                                continue
                        else:
                            # didn't find KEYWORD
                            has_keyword = False
                            continue
                    else:
                        # no keyword was found or line is a statement
                       
                        if current_line_wo_comment.line.isspace() or len(current_line_wo_comment.line) == 0:
                            if current_line_wo_comment.isMultiline:
                                keyword_line_check_index = current_line_wo_comment.multiLineJumpIndex
                                continue
                            else:
                                keyword_line_check_index += 1
                                continue
                        else:
                            
                            has_keyword = False
                            cont = False
                            break
                if cont:
                    continue
                else:
                    break

            elif not current_line_wo_comment.hasComment:
                
                if line.find("*/") != -1:
                    keyword_line_check_index += 1
                line = lines[keyword_line_check_index]
                if line.isspace():
                    continue
                else:
                    for keyword in consts.KEYWORDS:
                        keyword_check_re = re.search(keyword, line)
                        if keyword_check_re:
                            if keyword_check_re.start() == first_char_of_ln:
                                # we found a keyword
                                cont = False
                                has_keyword = True
                                break
                            else:
                                cont = False
                                has_keyword = False
                                continue
                        else:
                            # didn't find KEYWORD
                            cont = False
                            has_keyword = False
                            continue
                    else:
                        # didn't find any keyword
                        has_keyword = False

                    if cont:
                        continue
                    else:
                        break

    if not has_keyword:
        # didn't find a keyword
        return get_next_semi_colon_line_index(index, lines) + 1  # we found semicolon
    else:
        # here we reach only if it is KEYWORD found
        if keyword == r"\b(else)\b" or keyword == r"\b(do)\b":
            if line.find("if") != -1:
                # line is else if
                check_parenth_result = check_for_parentheses(line, keyword_line_check_index, lines, "p")
            else:
                check_parenth_result = models.ParenthResult(True, keyword_line_check_index, None)
        else:
            check_parenth_result = check_for_parentheses(line, keyword_line_check_index, lines, "p")
        if check_parenth_result is None:
            return None

        elif not check_parenth_result.isOnSameLine:
            # (condition) doesnt end on same line
            nxt_ln_index = check_parenth_result.lineIndex
            next_line_index = nxt_ln_index
            open_curly_brace_index = lines[nxt_ln_index - 1][check_parenth_result.lastCloseParenthIndex:].find("{")
            
        else:
            # (condition) ends on same line
            next_line_index = keyword_line_check_index + 1
            nxt_ln_index = keyword_line_check_index + 1
            open_curly_brace_index = line[check_parenth_result.lastCloseParenthIndex:].find("{")

        # don't touch me!
        open_next_line_curly_brace_index = check_for_open_brace(next_line_index, lines)

        # TODO: Fix the "if-else if" case (if ending with elseif)
        if keyword == r"\b(if)\b":
            tmp = nxt_ln_index - 1
            if lines[nxt_ln_index - 1].find("{") == -1:
                # has no curly on same line
                tmp = get_next_semi_colon_line_index(nxt_ln_index, lines) + 1
                if check_for_open_brace(nxt_ln_index, lines)[0] == -1:
                    tmp = get_next_semi_colon_line_index(nxt_ln_index, lines) + 1
                else:
                    res = check_for_parentheses(lines[nxt_ln_index - 1], nxt_ln_index - 1, lines, "b")
                    if res is None:
                        return None
                    else:
                        tmp = res.lineIndex - 1
                        # if lines[tmp].find("}") != -1 and lines[tmp].find("else") == -1:
                        #     tmp = res.lineIndex
            else:
                res = check_for_parentheses(lines[nxt_ln_index - 1], nxt_ln_index - 1, lines, "b")
                if res is None:
                    return None
                else:
                    tmp = res.lineIndex - 1
                    # if lines[tmp].find("}") != -1 and lines[tmp].find("else") == -1:
                    #     tmp = res.lineIndex

            while tmp < len(lines):
                if lines[tmp].find("}") != -1 and lines[tmp].find("else") == -1:
                    tmp += 1
                tmp_comment = trim_comment(lines[tmp], tmp, lines)
                tmp_line = lines[tmp]
                if tmp_comment.hasComment:
                    if tmp_comment.isMultiline:
                        tmp = tmp_comment.multiLineJumpIndex
                        continue
                    tmp_line = tmp_comment.line
                    if tmp_line.isspace():
                        tmp += 1
                        continue
                        
                if re.search(r"\b(else)\b", tmp_line):
                    # found else!
                    if tmp_line.find("if") != -1:
                        # else if
                        chk_parenth = check_for_parentheses(tmp_line, tmp, lines, "p")

                        if not chk_parenth.isOnSameLine:
                            tmp2 = chk_parenth.lineIndex
                            tmp = tmp2 + 1
                            continue
                        else:
                            tmp = get_next_semi_colon_line_index(tmp, lines)
                            continue
                    else:
                        if tmp_line.find("{") == -1:
                            # no same line curly
                            if check_for_open_brace(tmp + 1, lines)[0] == -1:
                                # no later curly
                                return get_next_semi_colon_line_index(tmp+1, lines) + 1
                            else:
                                res = check_for_parentheses(tmp_line, tmp, lines, "b")
                                if res is None:
                                    return None
                                else:
                                    return res.lineIndex
                        else:
                            res = check_for_parentheses(tmp_line, tmp, lines, "b")
                            if res is None:
                                return None
                            else:
                                return res.lineIndex

                elif not tmp_line.isspace():
                    return get_next_semi_colon_line_index(tmp, tmp_line) + 1
                else:
                    tmp += 1
                    continue
                # NOTE: the above has a bug in which if the program ends on
                #  ```
                #  for()\
                #     if()\
                #         asd;
                #         ```
                #         The program will never end. HOWEVER, this will never happen as the program will always end
                #           on a `}`, as it is C code. Hence we can safely ignore

        elif (open_curly_brace_index != -1 or open_next_line_curly_brace_index[0] != -1) and keyword != r"\b(if)\b":
            # we found open curly brace related to this other keyword
            # we must go on to find the close }
            close_curly_brace_index = line.find("}")
            if close_curly_brace_index == -1:
                # run the code
                # search for matching {},
                #   if match, return that line ki index.
                #   else, raise, DEATH-ERROR.
                if open_curly_brace_index == -1:
                    result = check_for_parentheses(lines[open_next_line_curly_brace_index[1]],
                                                   open_next_line_curly_brace_index[1], lines, type_of_parenth="b")
                else:
                    result = check_for_parentheses(lines[nxt_ln_index - 1], nxt_ln_index - 1, lines,
                                                   type_of_parenth="b")
                if result is None:
                    return None

                else:
                    return result.lineIndex
            else:
                # same line has the thingy
                return get_next_semi_colon_line_index(keyword_line_check_index, lines) + 1
        else:
            # we didn't find it.
            # we must return semicolon index again!
            return get_next_semi_colon_line_index(keyword_line_check_index, lines) + 1
