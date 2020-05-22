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

    def __init__(self, line, hasComment, comment, isMultiline, multiLineJumpIndex):
        self.line = line
        self.hasComment = hasComment
        self.comment = comment
        self.isMultiline = isMultiline
        self.multiLineJumpIndex = multiLineJumpIndex

class ParenthResult:
    
    def __init__(self, isOnSameLine, lineIndex, lastCloseParenthIndex):
        self.isOnSameLine = isOnSameLine
        self.lineIndex = lineIndex
        self.lastCloseParenthIndex = lastCloseParenthIndex