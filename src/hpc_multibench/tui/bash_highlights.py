#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A tree-sitter query for highlighting bash.

Query string derived from:
https://github.com/nvim-treesitter/nvim-treesitter/blob/f95ffd09ed35880c3a46ad2b968df361fa592a76/queries/bash/highlights.scm

Which is aligned with the approach taken for Textual builtin languages, for example:
https://github.com/Textualize/textual/blob/main/src/textual/tree-sitter/highlights/python.scm

The Nvim treesitter library from which this is derived is licensed under the
Apache 2.0 license, which allows modification and distribution for both public
and private use. The original version of the grammar used was written by
TravonteD on GitHub.
"""

BASH_HIGHLIGHTS = """
(simple_expansion) @none
(expansion
  "${" @punctuation.special
  "}" @punctuation.special) @none
[
 "("
 ")"
 "(("
 "))"
 "{"
 "}"
 "["
 "]"
 "[["
 "]]"
 ] @punctuation.bracket

[
 ";"
 ";;"
 (heredoc_start)
 ] @punctuation.delimiter

[
 "$"
] @punctuation.special

[
 ">"
 ">>"
 "<"
 "<<"
 "&"
 "&&"
 "|"
 "||"
 "="
 "=~"
 "=="
 "!="
 ] @operator

[
 (string)
 (raw_string)
 (ansi_c_string)
 (heredoc_body)
] @string @spell

(variable_assignment (word) @string)

[
 "if"
 "then"
 "else"
 "elif"
 "fi"
 "case"
 "in"
 "esac"
 ] @conditional

[
 "for"
 "do"
 "done"
 "while"
 ] @repeat

[
 "declare"
 "export"
 "local"
 "readonly"
 "unset"
 ] @keyword

"function" @keyword.function

(special_variable_name) @constant

; trap -l
((word) @constant.builtin
 (#match? @constant.builtin "^SIG(HUP|INT|QUIT|ILL|TRAP|ABRT|BUS|FPE|KILL|USR[12]|SEGV|PIPE|ALRM|TERM|STKFLT|CHLD|CONT|STOP|TSTP|TT(IN|OU)|URG|XCPU|XFSZ|VTALRM|PROF|WINCH|IO|PWR|SYS|RTMIN([+]([1-9]|1[0-5]))?|RTMAX(-([1-9]|1[0-4]))?)$"))

((word) @boolean
  (#match? @boolean "^(true|false)$"))

(comment) @comment @spell
(test_operator) @string

(command_substitution
  [ "$(" ")" ] @punctuation.bracket)

(process_substitution
  [ "<(" ")" ] @punctuation.bracket)


(function_definition
  name: (word) @function)

(command_name (word) @function.call)

((command_name (word) @function.builtin)
 (#any-of? @function.builtin
    "alias" "cd" "clear" "echo" "eval" "exit" "getopts" "popd"
    "pushd" "return" "set" "shift" "shopt" "source" "test"))

(command
  argument: [
             (word) @parameter
             (concatenation (word) @parameter)
             ])

((word) @number
  (#lua-match? @number "^[0-9]+$"))

(file_redirect
  descriptor: (file_descriptor) @operator
  destination: (word) @parameter)

(expansion
  [ "${" "}" ] @punctuation.bracket)

(variable_name) @variable

((variable_name) @constant
 (#lua-match? @constant "^[A-Z][A-Z_0-9]*$"))

(case_item
  value: (word) @parameter)

(regex) @string.regex

((program . (comment) @preproc)
  (#match? @preproc "^#!/"))
"""
