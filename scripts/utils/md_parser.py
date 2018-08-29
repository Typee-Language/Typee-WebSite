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
    def _md_line(self) -> bool:
        #=======================================================================
        # <MD line> ::= <block element> | <space-starting elements> | <text with span elements>
        #=======================================================================
        return self._block_elements() or self._spacestarting_elements() or self._text_with_span_elements()


#=====   end of   scripts.utils.md_parser   =====#
