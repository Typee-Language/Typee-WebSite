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
class MarkdownToWordpress:
    """
    This class helps translating Markdown texts in HTML texts specifically 
    for WordPress utility.
    """    
    #-------------------------------------------------------------------------
    def __init__(self, md_text:str=None, gfm_mode:bool=False):
        '''
        Constructor.
        If md_text is not None,  its translation is available in  attribute 
        `translated_text`  right  after construction time,  else caller has
        to call method `translate` on created instance.
                
        Args:
            md_text: str
                A reference to the text to be translated from  Markdown  to
                HTML conforming with WordPress pages content.
            gfm_mode: bool
                Set to True if translation is done from GFM Mardown reader,
                else set to False. Defauts to False.
                In GFM mode, break-lines are '\n',  while in  not-GFM  mode 
                (i.e. in standard MD mode), break-lines are set by at least
                two spaces at end of line.
        '''
        self._gfm_mode = gfm_mode
        self.translated_text = None if md_text is None else self.translate( md_text )

    #-------------------------------------------------------------------------
    def translate(self, md_text:str) -> str:
        '''
        Translates Markdown text in HTML conforming WordPress pages content.
        '''
        wp_text = ''
        
        lines = md_text.split( '\n' )
        two_lines_header = False
        
        for num_line, line in enumerate( lines ):
            
            if two_lines_header:
                two_lines_header = False
                continue
            
            # is this line a header one?
            try:
                (header_level, header_text, two_lines_header) = self._check_header( line, lines[num_line+1] )
                if header_level > 0:
                    wp_text = wp_text.append( self._header(header_level, header_text) )
                    continue  ## header text detected
            except:
                pass  ## we're parsing the last line of MD text
        
        # end of MD text translating
        return wp_text
    

    #=========================================================================
    #-------------------------------------------------------------------------
    def _check_emphasis_marks(self, line:str, emph_str:str) -> bool:
        '''
        Returns True if an emphasis mark is detected, or False else. If 
        True is returned, line is split into a list of strings, each of 
        them being separated by an emphasis mark.
        '''
        if emph_str in line:
            line = line.split( emph_str )
            return True
        else:
            return False
        
    #-------------------------------------------------------------------------
    def _check_emphasis(self, line:str) -> bool:
        '''
        Returns True if emphasis is present in line, in which case line is
        split  into  a list of strings,  each of them being separated by a
        mark. Returns False else, and line is unchanged.
        '''
        return self._check_emphasis_marks( line, '*' ) or self._check_emphasis_marks( line, '_' )

    #-------------------------------------------------------------------------
    def _check_header(self, line:str, next_line:str=None) -> (int, str, bool):
        '''
        Returns the number of the header if some is found and the header text,
        or 0 if not header,  plus the whole line as text and a bool to specify
        that the header stood on two successive lines.
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
                return (count, splitted_line[1], False)
            else:
                return (0, line, False)
            
        elif next_line is None:
            return (0, line, False)
        
        else:
            #-------------------------------------------------------------
            def _my_check( hdr_char:str ) -> bool:
                count = next_line.count( hdr_char )
                if len(next_line) == count:
                    return len(line) <= count
            #-------------------------------------------------------------
            return ( 1 if _my_check('=') else 2 if _my_check('-') else 0, line, True )

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
    def _check_list(self, line:str) -> (bool, bool, str):
        '''
        Returns a triplet:
          - first bool is True if line is an item of a list;
          - second bool is True if item is unordered;
          - last string contains the item text without the item head.
        '''
        item = line.ltrim().split( maxsplit=1 )
        head, content = item[0], item[1]
        
        if len(head) == 1 and head[0] in ['-', '*', '+']:
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
    def _check_strike(self, line:str) -> bool:
        '''
        Returns True if strikethrough is present in line, in which case line 
        is split  into a list of strings,  each of them being separated by a
        mark. Returns False else, and line is unchanged.
        '''
        return self._check_emphasis_marks( line, '~~' )

    #-------------------------------------------------------------------------
    def _check_strong(self, line:str) -> bool:
        '''
        Returns True if strong is present in line, in which case line is
        split into a list of strings,  each of them being separated by a
        mark. Returns False else, and line is unchanged.
        '''
        return self._check_emphasis_marks( line, '**' ) or self._check_emphasis_marks( line, '__' )

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


#=====   end of   scripts.utils.markdown_to_wordpress   =====#

