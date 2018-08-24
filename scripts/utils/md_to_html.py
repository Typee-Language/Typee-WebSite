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
from scripts.utils.md_mark import *


#=============================================================================
class MDtoHTML:
    """
    This class helps translating Markdown texts in HTML texts specifically 
    for the "standard" MD specification.
    """    
    #-------------------------------------------------------------------------
    def __init__(self, md_text_lines:list=None):
        '''
        Constructor.
        If md_text is not None,  its translation is available in  attribute 
        `html_text` right after construction time,  else caller has to call 
        method `translate()` on created instance.
                
        Args:
            md_text: str
                A reference to the text to be translated from  Markdown  to
                HTML conforming with WordPress pages content.
        '''
        self.html_text = None if md_text_lines is None else self.translate( md_text_lines )

    #-------------------------------------------------------------------------
    def translate(self, md_text_lines:list) -> str:
        '''
        Translates Markdown text in HTML conforming WordPress pages content.
        '''
        self._parse_md( md_text_lines )       # first  phase of translation
        self._translate_md( md_text_lines )   # second phase of translation

    
    #=========================================================================
    #-------------------------------------------------------------------------
    def _parse_md(self, md_lines:str):
        '''
        Implementation of the first phase of the MD to HTML translation
        '''
        self._marks = list()
        self._refs  = dict()

        two_lines_header = False
        for num_line, line in enumerate( md_lines ):
            
            if two_lines_header:  ## set to True while checking for a MD header, see below
                two_lines_header = False
                continue
            
            # is this line an MD header?
            try:
                (header_level, two_lines_header) = self._check_header( line, md_lines[num_line+1] )
                if header_level > 0:
                    self._marks.append( MDHeader( LineColumn(num_line, header_level+1), header_level, two_lines_header ) )
                    continue  ## header text detected

                
            
            except:
                pass  ## we're parsing the last line of MD text

    #-------------------------------------------------------------------------
    def _translate_md(self, md_text_lines:str):
        '''
        Implementation of the second phase of the MD to HTML translation
        '''
        wp_text = ''
                
        # end of MD text translating
        return wp_text
    

    #=========================================================================
    #-------------------------------------------------------------------------
    def _check_emphasis_marks(self, line:str, emph_str:str) -> (bool, list):
        '''
        Returns True if an emphasis mark is detected, or False else. If True
        is  returned,  the line split into a list of strings separated by an 
        emphasis mark is returned also in the tuple.  If False is  returned, 
        None is return in place of list in the tuple.
        '''
        if emph_str in line:
            return (True, line.split(emph_str))
        else:
            return (False, None)
        
    #-------------------------------------------------------------------------
    def _check_emphasis(self, line:str) -> (bool, list):
        '''
        Returns True if an emphasis mark is detected, or False else. If True
        is  returned,  the line split into a list of strings separated by an 
        emphasis mark is returned also in the tuple.  If False is  returned, 
        None is return in place of list in the tuple.
        '''
        return self._check_emphasis_marks( line, '*' ) or \
               self._check_emphasis_marks( line, '_' )

    #-------------------------------------------------------------------------
    def _check_header(self, line:str, next_line:str=None) -> (int, bool):
        '''
        Returns the number of the header if some is found, or 0 if not header,
        plus a bool to specify that the header stood on two successive lines.
        
        MD syntax:
        # H1
        ## H2
        ### H3
        #### H4
        ##### H5
        ###### H6
        
        Alternatively, for H1 and H2, an underline-ish style:
        
        Alt-H1
        ======
        
        Alt-H2
        ------
        '''
        if line.ltrim()[0] == '#':
            splitted_line = line.ltrim().split( maxsplit=1 )
            hashes = splitted_line[0]
            count = hashes.count( '#' )
            if count == len( hashes ):
                return (count, False)
            else:
                return (0, False)
            
        elif next_line is None:
            return (0, False)
        
        else:
            #-------------------------------------------------------------
            def _my_check( hdr_char:str ) -> bool:
                count = next_line.count( hdr_char )
                if len(next_line) == count:
                    return len(line) <= count
            #-------------------------------------------------------------
            return ( 1 if _my_check('=') else 2 if _my_check('-') else 0, True )

    #-------------------------------------------------------------------------
    def _check_hrule(self, line:str) -> bool:
        '''
        Returns True if some horizontal rule is detected in line, or False else.
        '''
        #-----------------------------------------------------------------
        def _check(rule_char:str, line:str) -> bool:
            count = line.count( rule_char )
            return count >= 3 and count == len(line)
        #-----------------------------------------------------------------
        line = line.trim()
        return _check('*', line) or _check('_', line) or _check('-', line)

    #-------------------------------------------------------------------------
    def _check_links(self, line:str) -> (bool, list):
        '''
        Returns True if line contains links plus a list of these links, or 
        False plus None if not.
        '''
        if '[' in line and ']' in line:
            links = []
            start_index = line.find( '[ ')
            end_index   = line.find( '] ')
            while end_index != -1:
                try:
                    text = line[start_index+1:end_index]
                    if line[end_index+1] == '(':
                        start_index = end_index+1
                        end_index = line[start_index+1:].find(')')
                        links.append( self._Link(text, line[start_index:end_index]) )
                        
                    elif line[end_index+1] == '[':
                        start_index = end_index+1
                        end_index = line[start_index+1:].find(']')
                        links.append( self._RefLink(text, line[start_index:end_index]) )
                    
                    else:
                        links.append( self._RefLink(text) )
                    
                    start_index = line[end_index+1:].find( '[' )
                    end_index   = line[start_index+1:].find( ']' )
                    
                except:
                    break
            
            return (True, links)
        
        elif     
        else:
            return (False, None)

    #-------------------------------------------------------------------------
    def _check_list(self, line:str) -> (bool, bool, str):
        '''
        Returns a triplet:
          - first bool is True if line is an item of a list;
          - second bool is True if item is unordered;
          - last string contains the item text without the item head.
        '''
        item = line.ltrim().split( maxsplit=1 )
        head, content = item[0], item[1]
        
        if len(head) == 1 and head[0] in "-+*":
            return (True, True, content)
        elif head[-1] == '.':
            try:
                _ = int( head[:-1] )
                return (True, False, content)
            except:
                return (False, False, line)
        else:
            return (False, False, line)

    #-------------------------------------------------------------------------
    def _check_paragraph_break(self, next_line:str) -> bool:
        '''
        Returns True when next_line just contains '\n'
        '''
        return next_line == '\n'

    #-------------------------------------------------------------------------
    def _check_Reference(self, line) -> bool:
        '''
        Returns True if line is a reference, or False else.
        '''
        return line.ltrim()[0] == '[' and line.contains ']:'

    #-------------------------------------------------------------------------
    def _check_strike(self, line:str) -> (bool, list):
        '''
        Returns True if strikethrough is present in line, in which case line 
        is split into a list of strings that is returned in the tuple,  each 
        of them being separated by a mark.  Returns False else,  and None is 
        returned in place of list in the returned tuple.
        '''
        return self._check_emphasis_marks( line, '~~' )

    #-------------------------------------------------------------------------
    def _check_strong(self, line:str) -> (bool, list):
        '''
        Returns True if strong is present in line, in which case line is
        split into a list of strings that is returned in the tuple, each 
        of them being separated by a mark. Returns False else,  and None 
        is returned in place of list in the returned tuple.
        '''
        return self._check_emphasis_marks( line, '**' ) or self._check_emphasis_marks( line, '__' )

    #-------------------------------------------------------------------------
    def _check_urls(self, line:str) -> (bool, list):
        '''
        Returns True if line contains URLs plus a list of these URLs, or 
        False plus None if not.
        '''
        #---------------------------------------------------------------------
        urls = []
        if 'http://' in line or 'https://' in line:
            sublines = line.split( 'http' )
            i = 0
            while i < len(sublines):
                try:
                    if len(sublines[i]) == 0:
                        url = 'http{:s}'.format( sublines[i+1].split(' ', 1) )
                        urls.append( self._UrlLink( url ) )
                        i += 2
                    elif sublines[i][-1] in ' <':
                        pairing = { ' ': ' ',  '<': '>' }
                        end_url = sublines[i+1].find( pairing[sublines[i][-1]], 1)
                        url = 'http{:s}'.format( sublines[i+1][:end_url] )
                        urls.append( self._UrlLink( url ) )
                        i += 2
                    else:
                        i += 1
                except:
                    break
            return (True, urls)
        else:
            return (False, None)

    #-------------------------------------------------------------------------
    def _combined_emphasis(self, line:str) -> str:
        '''
        Modifies every MD emphasis mark with its HTML equivalent in a line.
        '''
        #-------------------------------------------------------------
        def _insert_emph(emph_start:str, txt:str, emph_end) -> str:
            return ''.join( ["{:s}{:s}{:s}{:s}".format(txt[k]   ,
                                                       emph_start,
                                                       txt[k+1] ,
                                                       emph_end ) for k in range(0, len(txt), 2)] )
        #-------------------------------------------------------------
        def _modify_em(sub_line:str) -> str:
            if self._check_emphasis( sub_line ):
                return _insert_emph( '<em>', sub_line, '</em>')
            else:
                return sub_line
        #-------------------------------------------------------------
        def _modify_strong(line:str) -> str:
            if self._check_strong( line ):
                return _insert_emph( '<strong>', line, '</strong>')
            else:
                return line
        #-------------------------------------------------------------
        def _modify_strikethrough(line:str) -> str:
            if self._check_strike( line ):
                return _insert_emph( '<span text-decorator="line-through">', line, '</span>')
        #-------------------------------------------------------------
        if self._check_strike(line):
            line = _modify_strikethrough( line )
        if self._check_strong(line):
            for i, txt in enumerate(line):
                line[i] = _modify_em( txt )
            return _modify_strong( line )
        else:
            return _modify_em( line )

    #-------------------------------------------------------------------------
    def _header(self, hdr_level:int, hdr_text:str) -> str:
        return "<h{:d}>{:s}</h{:d}>".format( hdr_level, hdr_text, hdr_level )


#=====   end of   scripts.utils.md_to_html   =====#

