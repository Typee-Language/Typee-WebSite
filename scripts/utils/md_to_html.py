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
from scripts.utils.md_mark       import *
from scripts.utils.md_marks_list import MDMarksList


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
        self._marks = MDMarksList()
        self._refs  = dict()

        setext_header = False
        current_indent = 0
        lines_count = len( md_lines )
        for num_line, line in enumerate( md_lines ):
            
            if setext_header:  ## set to True while checking for a Setext MD header, see below
                setext_header = False
                continue
            
            ##--- first, parses block elements ---
            ## checks headers
            header_level, setext_header = self._check_header( line 
                                                              md_lines[num_line+1] if num_line + 1 < lines_count : None )
            if header_level > 0:
                self._marks.append( MDHeader( LineColumn(num_line, 0), header_level, setext_header ) )
            
            else:
                ## checks blockquotes (never present in headers)
                blockquote_level, my_line = self._check_blockquote( line, current_indent )
                if blockquote_level > 0:
                    self.marks.append( MDBlockQuote( LineColumn(num_line, 0), blockquote_level ) )
                
                ## checks list items (never present in headers)
                nested_level, start_item, is_unordered_list = self._check_list( my_line )
                if nested_level > 0:
                    if is_unordered_list:
                        self.marks.append( MDListItem(LineColumn(num_line, 0),
                                                      LineColumn(num_line, start_item-1), nested_level) )
                    else:
                        self.marks.append( MDListNumItem(LineColumn(num_line, 0),
                                                         LineColumn(num_line, start_item-1), nested_level) )
                    current_indent = nested_level * 4
                
                ## checks code line
                if self._check_code_line( my_line, current_indent ):
                    self.marks.append( MDCodeLine( LineColumn(num_line, 0) ) )
                
                ## checks horizontal roules (never present in headers)
                if self._check_hrule( line ):
                    self.marks.append( MDHRule( LineColumn(num_line, 0) ) )

            ##--- second, parses span elements ---
            self._automatic_links = MDMarksList()
            self._links           = MDMarksList()
            self._refs            = MDMarksList()
            self._backslashes     = MDMarksList()
            self._emphasis        = MDMarksList()
            self._inlined_code    = MDMarksList()
            self._images          = MDMarksList()


    #-------------------------------------------------------------------------
    def _translate_md(self, md_text_lines:str):
        '''
        Implementation of the second phase of the MD to HTML translation
        '''
        html_text = ''
                
        # end of MD text translating
        return html_text
    

    #=========================================================================
    #-------------------------------------------------------------------------
    def _check_blockquote(self, line:str, indent:int) -> (int, str):
        '''
        Returns the blockquote level,  even if set to 0 (i.e. no blockquote
        detected). Last returned value is the text of the line which is not 
        part of the blockquote MD tag,  or the whole line if no  blockquote
        has been detected.
        '''
        index = line[indent:].find( '>' )
        if 0 <= index <= 3:
            items = line.split( '> ' )
            bq_level = len( items ) - 1
            return (bq_level, items[-1])
        else:
            return (0, line)

    #-------------------------------------------------------------------------
    def _check_code_line(self, line:str, indent:int) -> bool:
        '''
        Returns True if line belongs to a block of code, or False else.
        '''
        start = self._count_leading_spaces( line )
        return start - indent >= 4        

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
        if line.lstrip()[0] == '#':
            splitted_line = line.lstrip().split( maxsplit=1 )
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
                if count > 0:
                    return len(next_line) == count:
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
        line = line.strip()
        return _check('*', line) or _check('_', line) or _check('-', line)

    #-------------------------------------------------------------------------
    def _check_linebreak(self, line:str) -> bool:
        '''
        Returns True if line ends with at least two spaces.
        '''
        return line[-2:] == '  ' 

    #-------------------------------------------------------------------------
    def _check_list(self, line:str) -> (int, int, bool):
        '''
        Returns a triplet:
          - first int is the nested level of list;
          - second int is the index in line of first character of the item content;
          - bool is True if item is unordered;
        '''
        nb_spaces = self._count_leading_spaces( line )
        item_level = nb_spaces // 4 + 1
        
        if line[nb_spaces] in  "-+*":
            return (item_level, nb_spaces, True)
        else:
            item = line[nb_spaces:].split( maxsplit=1 )
            head, content = item[0], item[1]
            if head[-1] == '.':
                try:
                    _ = int( head[:-1] )
                    return (item_level, nb_spaces, False)
                except:
                    return (0, 0, False)
            else:
                return (0, 0, False)

    #-------------------------------------------------------------------------
    def _check_paragraph_break(self, next_line:str) -> bool:
        '''
        Returns True when next_line just contains '\n'
        '''
        return next_line == '\n'

    #-------------------------------------------------------------------------
    def _check_reference(self, line) -> bool:
        '''
        Returns True if line is a reference, or False else.
        '''
        return line.lstrip()[0] == '[' and line.contains ']:'

    #-------------------------------------------------------------------------
    def _count_leading_spaces(self, line:str, tabs_length:int=4) -> int:
        '''
        Internal utility. Counts leading spaces in line.
        '''
        count = 0
        try:
            for c in line:
                if c == ' ':    count += 1
                elif c == '\t': count += tabs_length
                else:
                    break
        except:
            pass
        return count

    #-------------------------------------------------------------------------
    def evaluate_automatic_link_marks(self, num_line:int, line:str):
        '''
        Appends automatic links to attribute 'automatic_lins'.
        '''
        line_length = len( line )
        i = 0
        while i < line_length:
            if line[i] == '<':
                end = line[i:].find( '>' )
                if end != -1 and '://' in line[i:end] and ' ' not in line[i:end]:
                    self._automatic_links.append( MDLinkAuto( LineColumn(num_line, i),
                                                              LineColumn(num_line, end),
                                                              line[i+1:end] ) )

    #-------------------------------------------------------------------------
    def _evaluate_emphasis_marks(self, num_line:int, line:str):
        '''
        Appends all kinds of emphasis marks to attribute '_emphasis'.
        '''
        #-----------------------------------------------------------------
        def _append(indx:int, emph_car:str, count:int):
            end_point = LineColumn( num_line, indx+count )
            if emph_char == '~':
                if count == 2:
                    self._emphasis.append( MDStrikethrough( LineColumn(num_line, indx), end_point ) )
            elif count == 1:
                self._emphasis.append( MDEmphasis( LineColumn(num_line, indx), end_point ) )
            else:
                self._emphasis.append( MDStrong( LineColumn(num_line, indx), end_point ) )
        #-----------------------------------------------------------------
        def _check_spaces(indx:int, count:int, line_length:int)-> bool:
            if indx == 0 or indx+count >= line_length:
                return False
            else:
                return line[index-1] == line[index+count] == ' '
        #-----------------------------------------------------------------
        i = 0
        line_length = len( line )
        while i < line_length:
           if line[i] in ['*_~'] and (i == 0 or line[i-1] != '\\'):
               if i+1 < line_length and line[i+1] == line[i]:
                   if not _check_spaces(i, 2, line_length):
                       _append( i, line[i], 2 )
                       i += 1
               else:
                   if not _check_spaces(i, 1, line_length):
                       _append( i, line[i], 1 )
            i += 1

    #-------------------------------------------------------------------------
    def _evaluate_image_marks(self, num_line:int, line:str):
        '''
        Appends every image mark to attribute '_images'.
        '''
        start = 0
        excl_split = line.split( '!' )
        if len( excl_split ) > 1:
            i = 0
            try:
                while i < len( excl_split ):
                    if excl_split[i][-1] == '\\':
                        i += 1
                    
                    elif excl_split[i+1][0] == '[':
                        text = excl_split.split( ']', 1 )
                        alt_text = text[0]
                        length = len( alt_text ) + 3
                        
                        image_class = None
                        if text[1] == '(':
                            length += text[1].find( ')' ) + 1
                            image_class = MDImage
                        elif text[1] == '[':
                            length += text[1].find( ']' ) + 1
                            image_class = MDImageRef
                        
                        if image_class:
                            text = text[1].split( '"' )
                            if len(text) == 1:
                                link_txt = text
                                title_text = None
                            else:
                                link_txt = text[0].rstrip()
                                title_text = text[1]
                                
                            self._images.append( image_class( LineColumn(num_line, start),
                                                              LineColumn(num_line, start+length),
                                                              alt_text,
                                                              link_text,
                                                              title_text ) )
                            i += 2
                        else:
                            i += 1
            except:
                pass

    #-------------------------------------------------------------------------
    def _evaluate_inlined_code(self, num_line:int, line:str):
        '''
        Appends every inlined-code tags to attribute '_inlined_code'. 
        '''
        line_length = len( line )
        entering_double_backticks = True
        
        i = 0
        while i < line_length:
            if line[i] == '`' and (i == 0 or line[i-1] != '\\'):
                if i < line_length-1 and line[i+1] == '`':
                    if entering_double_backticks:
                        entering_double_backticks = False
                        self._inlined_code.append( MDCodeInlined( LineColumn(num_line, i), LineColumn(num_line, i+1) ) )
                        i += 1
                    else:
                        entering_double_backticks = True
                        self._inlined_code.append( MDCodeInlined( LineColumn(num_line, i-1), LineColumn(num_line, i) ) )
                        i += 1
                else:
                    if entering_double_backticks:
                        self._inlined_code.append( MDCodeInlined( LineColumn(num_line, i), LineColumn(num_line, i) ) )
            i += 1

    #-------------------------------------------------------------------------
    def _evaluate_links_and_refs(self, num_line:int, line:str):
        '''
        Appends  detected links to attribute '_links' 
        and detected references to attribute '_refs'.
        '''
        line_length = len( line )
        i = 0
        while i < line_length:
            if line[i] == '[' and (i == 0 or line[i-1] != '\\'):
                start = i
                end = line[i:].find( ']' )
                if end < 0:
                    i = line[i:].find( '[' )
                    if i <= -1:
                        break
                    else:
                        continue
                    
                elif i == line_length - 1:
                    break
                
                else:
                    brackets_text = line[i+1:end]
                    i = end+1
                    spaces = self._count_leading_spaces( line[i:] )
                    i += spaces
                    if i >= line_length:
                        break
                    if line[i] == '(':
                        # direct link
                        end = line[i:].find( ')' )
                        if end != -1:
                            splt = line[i+1:end].split( '"' )
                            link_text = splt[0]
                            title_text = splt[1] if len(splt) > 1 else None
                            self._links.append( MDLinkTitle( LineColumn(num_line, start),
                                                             LineColumn(num_line, end),
                                                             brackets_text,
                                                             link_text,
                                                             title_text ) )
                    elif line[i] == '[':
                        # link by reference
                        end = line[i:].find( ']' )
                        if end != -1:
                            ref_text = brackets_text if end == i+1 else line[i+1:end]
                            self.l_inks.append( MDLinkRef( LineColumn(num_line, start),
                                                           LineColumn(num_line, end),
                                                           brackets_text,
                                                           ref_text.lower() ) )
                    elif line[i] == ':' and spaces == 0:
                        # reference
                        if self._count_leading_spaces(line) < 3:
                            splt = line[i:].split()
                            if len( splt ) > 1:
                                url_ref = splt[1].strip( '<>' )
                                title = None
                                if len( splt ) >= 2:
                                    title_text = splt[2]
                                    if title_text[0] == title_text[-1] == '"' or \
                                       title_text[0] == title_text[-1] == "'" or \
                                       title_text[0] == '(' and title_text[-1] == ')':
                                        title = title_text[1:-1]
                                self._refs.append( MDReference( LineColumn(num_line, 0),
                                                                LineCOlumn(num_line, len(line)),
                                                                brackets_text.lower(),
                                                                url_ref,
                                                                title ) )
                                break
            i += 1

    #-------------------------------------------------------------------------
    def _tanslate_combined_emphasis(self, line:str) -> str:
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
    def _translate_header(self, hdr_level:int, hdr_text:str) -> str:
        return "<h{:d}>{:s}</h{:d}>".format( hdr_level, hdr_text, hdr_level )


#=====   end of   scripts.utils.md_to_html   =====#

