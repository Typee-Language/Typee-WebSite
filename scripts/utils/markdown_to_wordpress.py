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
    def __init__(self, md_text:str=None):
        '''
        Constructor.
        If md_text is not None, its translation is available in attribute 
        `translated_text`  right after construction time, else caller has
        to call method `translate` on created instance.
                
        Args:
            md_text: str
                A reference to the text to be translated from Markdown to
                HTML conforming with WordPress pages content.
        '''
        self.translated_text = None if md_text is None else self.translate( md_text )

    #-------------------------------------------------------------------------
    def translate(self, md_text:str) -> str:
        '''
        Translates Markdown text in HTML conforming WordPress pages content.
        '''
        wp_text = ''
        
        lines = md_text.split( '\n' )
        for num_line, line in enumerate( lines ):
            
            # is this line a header one?
            try:
                (header_level, header_text) = self._check_header( line, lines[num_line+1] )
                if header_level > 0:
                    wp_text = wp_text.append( self._header(header_level, header_text) )
                    continue  ## header text detected
            except:
                pass  ## we're parsing the last line of MD text
        
        # end of MD text translating
        return wp_text
    

    #=========================================================================
    #-------------------------------------------------------------------------
    def _check_header(self, line:str, next_line:str=None) -> (int, str):
        '''
        Returns the number of the header if some is found and the header text,
        or 0 if not header and the whole line as text.
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
                return (count, splitted_line[1])
            else:
                return (0, line)
            
        elif next_line is None:
            return (0, line)
        
        else:
            #-------------------------------------------------------------
            def _my_check( hdr_char:str ) -> bool:
                count = next_line.count( hdr_char )
                if len(next_line) == count:
                    return len(line) <= count
            #-------------------------------------------------------------
            return ( 1 if _my_check('=') else 2 if _my_check('-') else 0, line )

    #-------------------------------------------------------------------------
    def _header(self, hdr_level:int, hdr_text:str) -> str:
        return "<h{:d}>{:s}</h{:d}>".format( hdr_level, hdr_text, hdr_level )


#=====   end of   scripts.utils.markdown_to_wordpress   =====#

