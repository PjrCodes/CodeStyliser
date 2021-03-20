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
# models.py
# custom models/ classes
# ---


class LineWithComment:

    def __init__(self, line, has_comment, comment, is_multiline, multi_line_jump_index, is_empty):
        self.line = line
        self.hasComment = has_comment
        self.comment = comment
        self.isMultiline = is_multiline
        self.multiLineJumpIndex = multi_line_jump_index
        self.isEmpty = is_empty


class ParenthResult:
    
    def __init__(self, is_on_same_line, line_index, last_close_parenth_index):
        self.isOnSameLine = is_on_same_line
        self.lineIndex = line_index
        self.lastCloseParenthIndex = last_close_parenth_index


class NestResult:

    def __init__(self,  line_index, has_keyword):
        self.lineIndex = line_index
        self.hasKeyword = has_keyword
