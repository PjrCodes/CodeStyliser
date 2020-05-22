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
# constants.py
# constants
# ---


VERSION_NUMBER = "0.1.11.1-DEV "
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
DEFINE_PATTERN = r"#\s*\b(define)\b"

SINGLELINE_COMMENT_PATTERN = r"(\/\*[^\n]*)|(\/\/[^\n]*)"
OPENBRACE_PATTERN = r"^(\s*\{)|^(\{)"
KEYWORDS = [r'\b(for)\b', r'\b(while)\b', r'\b(do)\b', r'\b(switch)\b', r'\b(if)\b', r'\b(else)\b']
