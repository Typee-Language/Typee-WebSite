#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Philippe Schmouker, Typee project, http://www.typee.ovh

Permission is hereby granted,  free of charge,  to any person obtaining a copy
of this software and associated documentation files (the "Software"),  to deal
in the Software without restriction, including  without  limitation the rights
to use,  copy,  modify,  merge,  publish,  distribute, sublicense, and/or sell
copies of the Software,  and  to  permit  persons  to  whom  the  Software  is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS",  WITHOUT WARRANTY OF ANY  KIND,  EXPRESS  OR
IMPLIED,  INCLUDING  BUT  NOT  LIMITED  TO  THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT  SHALL  THE
AUTHORS  OR  COPYRIGHT  HOLDERS  BE  LIABLE  FOR  ANY CLAIM,  DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT,  TORT OR OTHERWISE, ARISING FROM,
OUT  OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#=============================================================================
# no import.


#=============================================================================
class MDParser:
    """
    A parser for standard Markdown texts.
    See https://tools.ietf.org/html/rfc7764 for Markdown specs.
    """    
    #-------------------------------------------------------------------------
    def __init__(self, filepath:str=None):
        '''
        Constructor.
        
        Parses automatically files if some are passed  as  argument  at 
        construction time, or just prepares the further parsing of such 
        files - in which case method `parse()` will have to be called.
        
        Args:
            filepath: str
                The path to the file to be parsed.  If None, no parsing 
                takes place at construction time. Defaults to None.

        Raises:
            Any IOError if any file is not found or is inaccessible.
        '''
        if filepath is not None:
            self.parse( filepath )
   
    #-------------------------------------------------------------------------
    def parse(self, filepath:str) -> str:
        '''
        Constructor.
        
        Parses Markdown texts from file.
        
        Args:
            filepath: str
                The path to the file to be parsed.
        
        Returns:
            The parsed text.

        Raises:
            Any IOError if any file is not found or is inaccessible.
        '''
        with open( filepath ) as fp:
            self._md_text = fp.read()
        
        return self._parse()
            

    #=========================================================================
    #-------------------------------------------------------------------------
    def _parse(self) -> str:
        '''
        '''
        self._parsed_text = ''
        self._current_index = 0
        self._mem_index = None
        
        while self._md_line():
            continue
            #===================================================================
            # <MD text> ::= <MD line> <MD text> | EPS
            #===================================================================
        return self._parsed_text


    #=========================================================================
    #-------------------------------------------------------------------------
    def _block_element(self) -> bool:
        #=======================================================================
        # <block elements> ::= <blockquote>
        #                   |  <header atx>
        #                   |  <header setext>
        #                   |  <list>
        #                   |  <horizontal rule>
        #                   |  <link or reference>
        #                   |  <image>
        #=======================================================================
        return self._blockquote() or \
                self._header_atx() or \
                self._header_setext() or \
                self._list() or \
                self._horizontal_rule() or \
                self._link_or_reference() or \
                self._image()

    #-------------------------------------------------------------------------
    def _md_line(self) -> bool:
        #=======================================================================
        # <MD line> ::= <block element> | <space-starting elements> | <text with span elements>
        #=======================================================================
        return self._block_elements() or \
                self._spacestarting_elements() or \
                self._text_with_span_elements() or \
                not self._end_of_text()

    #-------------------------------------------------------------------------
    def _space_element_1(self) -> bool:
        #=======================================================================
        # <space elements'> ::= ' ' <space elements''>
        #                    |  '\t' <code block>
        #                    |  <maybe star>
        #                    |  <maybe underscore>
        #                    |  <text with span elements>
        #=======================================================================
        if self._current == ' ':
            return self._space_elements_2()
        elif self._current == '\t':
            return self._code_block()
        else:
            return self._maybe_star() or \
                    self._maybe_underscore() or \
                    self._text_with_span_elements()

    #-------------------------------------------------------------------------
    def _space_element_2(self) -> bool:
        #=======================================================================
        # <space elements''> ::= ' ' <space elements'''>
        #                     |  '\t' <code block>
        #                     |  '\n' ## breakline! - CAUTION: maybe context sensitive...
        #                     |  <maybe star>
        #                     |  <maybe underscore>
        #                     |  <text with span elements>
        #=======================================================================
        if self._current == ' ':
            return self._space_elements_3()
        elif self._current == '\t':
            return self._code_block()
        elif self._current == '\n':
            self.breakline()  ## breakline! - CAUTION: maybe context sensitive...
            return True
        else:
            return self._maybe_star() or \
                    self._maybe_underscore() or \
                    self._text_with_span_elements()

    #-------------------------------------------------------------------------
    def _space_element_3(self) -> bool:
        #=======================================================================
        # <space elements'''> ::= ' ' <code block>                
        #                      |  '\t' <code block>
        #                      |  <maybe star>
        #                      |  <maybe underscore>
        #                      |  <text with span elements>
        #=======================================================================
        if self._current in " \t":
            return self._code_block()
        else:
            return self._maybe_star() or \
                    self._maybe_underscore() or \
                    self._text_with_span_elements()

    #-------------------------------------------------------------------------
    def _space_starting_elements(self) -> bool:
        #=======================================================================
        # <space-starting elements> ::= ' ' <space elements'>
        #                            |  '\t' <code block>
        #=======================================================================
        if self._current == ' ':
            return self._space_elements_1()
        elif self._current == '\t':
            return self._code_block()
        else:
            return False
        
    #-------------------------------------------------------------------------
    def _text_with_span_elements(self) -> bool:
        #=======================================================================
        # <text with span elements> ::= <html entity> <maybe setext header>
        #                            |  <html tag or automatic link> <maybe setext header>
        #                            |  <emphasis or strong style> <maybe setext header>
        #                            |  <inlined code> <maybe setext header>
        #                            |  <escape> <maybe setext header>
        #                            |  <line or paragraph end>
        #                            |  <any chars but & < * _ ` \\ \n> <maybe setext header>
        #=======================================================================
        if self._html_entity() or \
            self._html_tag_or_automatic_link() or \
            self._emphasis_or_strong_style() or \
            self._inlined_code() or \
            self._escape() or \
                self._any_chars_but_1():
            return self._maybe_setext_header()
        else:
            return self._line_or_paragraph_end()
            return True


#=====   end of   scripts.utils.md_parser   =====#
