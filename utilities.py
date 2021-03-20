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
    """Returns a line wo comment object, Tells if line is_empty, returns line in all cases!"""
    search_for_single_line_comment = re.search(consts.SINGLE_LINE_COMMENT_PATTERN, line)
    if search_for_single_line_comment:
        if search_for_single_line_comment.group()[0:2] == "/*":
            # keep searching for */
            same_line_end = line.find("*/")
            if same_line_end != -1:
                # ends on same line
                # TODO: ALSO CHECK IF THERE IS ANYTHING ON THE LINE BEFORE THE COMMENT, IN WHICH CASE WE NEED TO DIE
                # FIXME: THIS WILL FAIL IF THERE IS SOMETHING AFTER COMMENT
                # BUG: THIS IS A BUG AS IT CAUSES AN ERROR IN COMMENT HANDLING, AND PARENTHESES COUNTING,
                #      RAISING INDEX ERROR's
                if line[(same_line_end + 1):].isspace():
                    return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                                  search_for_single_line_comment.group(), False, None, is_empty=True)
                else:
                    # there is something after comment on line
                    return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                                  search_for_single_line_comment.group(), False, None, is_empty=False)
            else:
                # iterate for line in lines till we get */
                index = line_no + 1
                while True:
                    multi_comment_end = lines[index].find("*/")
                    if multi_comment_end != -1:
                        # multi line comment has ended
                        if line[(multi_comment_end + 1):].isspace():
                            return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                                          search_for_single_line_comment.group(), False, None,
                                                          is_empty=True)
                        else:
                            return models.LineWithComment(lines[index][(multi_comment_end + 2):], True,
                                                          lines[index][:(multi_comment_end+2)], True, index,
                                                          is_empty=False)
                    else:
                        # no multi line comment end found, keep looping till found.
                        index = index + 1

        # found a single line comment of type //
        if line[:search_for_single_line_comment.start()].isspace():
            return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                          search_for_single_line_comment.group(), False, None, is_empty=True)
        else:
            return models.LineWithComment(line[:search_for_single_line_comment.start()], True,
                                          search_for_single_line_comment.group(), False, None, is_empty=False)
    else:
        # no comment
        return models.LineWithComment(line, False, "", False, None, is_empty=False)


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
                print("ISSUE")
                if line_without_comment.isMultiline:
                    # go after multiline comments
                    next_line_index = line_without_comment.multiLineJumpIndex
                    continue
                else:

                    next_line_index += 1
                    if re.search(consts.OPEN_BRACE_PATTERN, line_without_comment.line):
                        # if the line before comment has {
                        break
                    else:
                        # there is something before line, but it is not an open brace
                        break

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
    skipper = skip_nests(keyword_line_check_index, lines)
    # recursively call:
    while True:
        if skipper.hasKeyword:
            skipper = skip_nests(index=skipper.lineIndex, lines=lines)
        else:
            break
        print("True")

    if not skipper.hasKeyword:
        # didn't find a keyword
        return get_next_semi_colon_line_index(index, lines) + 1  # we found semicolon
    else:
        return skipper.lineIndex


def skip_nests(index, lines: list):
    """Skips nests and return the last line's index. In a NestResult.  None is returned in failure cases"""

    # check for keyword
    found_key = ""
    has_key = False
    i = index
    tmp_line = ""
    last_tm = i
    while i < len(lines):
        # main checking loop

        tmp_comm = trim_comment(lines[i], i, lines)

        # tmp_line is the line after trimming comment!
        tmp_line = tmp_comm.line
        first_char_of_ln = get_first_character_index(tmp_line)

        if tmp_comm.isEmpty and tmp_comm.hasComment:
            # an empty line with comment (only comment)
            if tmp_comm.isMultiline:
                i = tmp_comm.multiLineJumpIndex
                continue
            else:
                i += 1
                continue
        elif tmp_line.isspace() or len(tmp_line) == 0:
            # same thing basically. We should never reach here anyhow.
            i += 1
            continue
        else:
            # valid line w/o comment or with comment, not matter
            # if tmp_line.find("*/") != -1:
            #     i += 1
            cont = True
            for key in consts.KEYWORDS:
                key_re = re.search(key, tmp_line)
                if key_re:
                    if key_re.start() == first_char_of_ln:
                        # we found keyword in beginning of sentence
                        found_key = key
                        cont = False  # break outer
                        has_key = True  # yes son, yes
                        break
                    else:
                        # not on first char
                        has_key = False
                else:
                    # no keyword
                    has_key = False
            else:
                # looping over
                if has_key:
                    cont = False
                    break
                else:
                    # not has key after loop, and also is not blank
                    # must be a statement!!!
                    cont = False
                    has_key = False
                    break
            if cont:
                i += 1
                continue  # next line please
            else:
                break

    if not has_key:
        # no keyword
        return models.NestResult(None, False)

    # else: (WE FOUND A KEYWORD on tmp_line)

    # re-declare (useless, but still doing!)
    tmp_comm = trim_comment(lines[i], i, lines)
    tmp_line = tmp_comm.line

    # set parentheses
    if found_key == r"\b(else)\b" or found_key == r"\b(do)\b":
        # line is else - or do
        if tmp_line.find("if") != -1:
            # line is else if, it has parentheses.
            p_check = check_for_parentheses(tmp_line, i, lines, "p")
        else:
            # line has no parentheses.
            p_check = models.ParenthResult(True, i, None)
    else:
        # line has parentheses.
        p_check = check_for_parentheses(tmp_line, i, lines, "p")

    # error occurred:
    if p_check is None:
        return None

    # get open_curly_brace_index
    if not p_check.isOnSameLine:
        # (condition) doesnt end on same line.

        nxt_ln_index = p_check.lineIndex
        open_curly_brace_index = lines[nxt_ln_index-1][p_check.lastCloseParenthIndex:].find("{")
    else:
        # (condition) doesnt end on same line.

        nxt_ln_index = i + 1
        open_curly_brace_index = tmp_line[p_check.lastCloseParenthIndex:].find("{")

    nxt_line_curly_index = check_for_open_brace(nxt_ln_index, lines)
    global answer
    answer = 0
    # handle the {}{}{} and the if-else nests.
    # TODO: Fix the "if-else if" case (if ending with elseif)
    if found_key == r"\b(if)\b":
        # check for if-else-if-else

        tm = nxt_ln_index - 1
        if open_curly_brace_index == -1:
            # has no curly on same line
            # check for nxt ln curly
            if nxt_line_curly_index[0] == -1:
                # no brace on later line also
                tm = get_next_semi_colon_line_index(nxt_ln_index, lines) + 1
            else:
                # brace was there on nxt-line-curly-index
                # TODO: handle comments
                # loop for em
                res = check_for_parentheses(lines[nxt_line_curly_index[1]], nxt_line_curly_index[1], lines, "b")
                if res is None:
                    return None
                else:
                    tm = res.lineIndex - 1

        else:
            # there was a curly on same line.
            res = check_for_parentheses(lines[nxt_ln_index - 1], nxt_ln_index - 1, lines, "b")
            if res is None:
                return None
            else:
                tm = res.lineIndex - 1

        while tm < len(lines):
            if lines[tm].find("}") != -1 and lines[tm].find("else") == -1:
                # it is at end of if with a }, search from next line
                tm += 1

            tmp_comm = trim_comment(lines[tm], tm, lines)
            tm_line = tmp_comm.line

            # handle comment based
            if tmp_comm.hasComment:
                if tmp_comm.isMultiline:
                    tm = tmp_comm.multiLineJumpIndex
                    continue
                if tm_line.isspace() or len(tm_line) == 0:
                    # TODO: replace with isempty
                    tm += 1
                    continue

            # line had else (after an if)
            if re.search(r"\b(else)\b", tm_line):
                # found else..
                if tm_line.find("if") != -1:
                    # else if
                    ch_paren = check_for_parentheses(tm_line, tm, lines, "p")

                    if not ch_paren.isOnSameLine:
                        tmp2 = ch_paren.lineIndex
                        tm = tmp2 + 1
                        continue
                    else:
                        tm = get_next_semi_colon_line_index(tm, lines)
                        continue

                    # TODO: stop looping at some point (else if case)
                else:
                    # not an else if, its an else.
                    if tm_line.find("{") == -1:
                        # no same line curly
                        if check_for_open_brace(tm + 1, lines)[0] == -1:
                            # no later curly

                            answer = get_next_semi_colon_line_index(tm+1, lines) + 1
                        else:
                            res = check_for_parentheses(tm_line, tm, lines, "b")
                            if res is None:
                                return None
                            else:
                                answer = res.lineIndex
                    else:
                        # Same line curly
                        res = check_for_parentheses(tm_line, tm, lines, "b")
                        if res is None:
                            return None
                        else:
                            answer = res.lineIndex

            elif not tm_line.isspace():
                answer = tm
            else:
                tm += 1
                continue
        # else:
        #     answer = tm
            # NOTE: the above has a bug in which if the program ends on
            #  ```
            #  for()\
            #     if()\
            #         asd;
            #         ```
            #         The program will never end. HOWEVER, this will never happen as the program will always end
            #           on a `}`, as it is C code. Hence we can safely ignore

    elif (open_curly_brace_index != -1 or nxt_line_curly_index[0] != -1) and found_key != r"\b(if)\b":
        # we found open curly brace related to this other keyword
        # we must go on to find the close }
        close_curly_index = tmp_line.find("}")
        if close_curly_index == -1:
            # search for matching {},
            #   if match, return!!!
            #   else, raise, DEATH-ERROR.
            if open_curly_brace_index == -1:
                result = check_for_parentheses(lines[nxt_line_curly_index[1]], nxt_line_curly_index[1],
                                               lines, type_of_parenth="b")
            else:
                result = check_for_parentheses(lines[nxt_ln_index - 1], nxt_ln_index - 1, lines, type_of_parenth="b")

            if result is None:
                return None
            else:
                answer = result.lineIndex
        else:
            # same line
            answer = get_next_semi_colon_line_index(last_tm + 1, lines) + 1
    else:
        answer = get_next_semi_colon_line_index(last_tm + 1, lines) + 1

    return models.NestResult(answer, has_keyword=has_key)









