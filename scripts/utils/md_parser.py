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
    def parse(self, filepath:str) -> MDMarksList:
        '''
        Constructor.
        
        Parses Markdown texts from file.
        
        Args:
            filepath: str
                The path to the file to be parsed.
        
        Returns:
            The list of MD marks detected in the parsed text.

        Raises:
            Any IOError if any file is not found or is inaccessible.
        '''
        with open( filepath ) as fp:
            self._md_text = fp.read()
        
        return self._parse()
            

    #=========================================================================
    #-------------------------------------------------------------------------
    def _parse(self) -> MDMarksList:
        '''
        '''
        self._current_index = 0
        self._mem_index = None
        self._md_marks = MDMarksList()
        
        self._line_start = self._current_index
        while self._md_line():
            self._line_start = self._current_index
            #===================================================================
            # <MD text> ::= <MD line> <MD text> | EPS
            #===================================================================
        return sorted( self._md_marks )


    #=========================================================================
    #-------------------------------------------------------------------------
    def _any_chars_but(self, unaccepted_chars:str):
        while not self._end_of_text and self._current not in unaccepted_chars:
            self._next()
    
    #-------------------------------------------------------------------------
    def _automatic_link_end(self) -> bool:
        #=======================================================================
        # <automatic link end> ::= <any chars but space \> > <automatic link end'>
        #=======================================================================
        if self._any_chars_but( " >" ):
            return self._automatic_link_end_1()
        else:
            return False
    
    #-------------------------------------------------------------------------
    def _automatic_link_end_1(self) -> bool:
        #=======================================================================
        # <automatic link end'> ::= '>'
        #=======================================================================
        if self._current == '>':
            self._next()
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _block_elements(self) -> bool:
        #=======================================================================
        # <block elements> ::= <blockquote>
        #                   |  <header atx>
        #                   |  <header setext>
        #                   |  <list>
        #                   |  <horizontal rule>
        #                   |  <link or reference>
        #                   |  <image>
        #=======================================================================
        return self._blockquotes() or \
                self._header_atx() or \
                self._header_setext() or \
                self._list() or \
                self._horizontal_rule() or \
                self._link_or_reference() or \
                self._image()

    #-------------------------------------------------------------------------
    def _blockquotes(self) -> bool:
        #=======================================================================
        # <blockquotes> ::= "> " <blockquotes'>
        #=======================================================================
        if self._current_2 == "> ":
            self._blockquote_start = self._current_index    ## $bq.start=index;
            self._blockquote_level = 1                      ## bq.level=1;
            self._next( 2 )
            return self._blockquotes_1()
        else:
            return False
        
    #-------------------------------------------------------------------------
        #=======================================================================
        # <blockquotes'> ::= "> " <blockquotes'>
        #                 |  <text with span elements> <blockquotes">
        #=======================================================================
        while self._current_2 == "> ":
            self._blockquote_level += 1                     ## $bq.level++;
            self._next( 2 )
        self._blockquote_end = self._current_index          ## $bq.end=index;
        if self._text_with_span_elements():
            return self._blockquotes_2()
        else:
            return False

    #-------------------------------------------------------------------------
    def _blockquotes_2(self) -> bool:
        #=======================================================================
        # <blockquotes"> ::= <text with span elements> <blockquotes">
        #                 |  <line or paragraph end>
        #=======================================================================
        while self._text_with_span_elements():
            continue
        if self._line_or_paragraph_end():
            self._append_mark( MDBlockQuote(self._blockquote_start,
                                            self._blockquote_end  ,
                                            self._blockquote_level ) )  ## $mark(bq);
            return True
        else:
            return False 

    #-------------------------------------------------------------------------
    def _closing_html_tag(self) -> bool:
        #=======================================================================
        # <closing html tag> ::= <any chars but \> \\n > '>'
        #=======================================================================
        if self._any_chars_but( ">\n" ) and self._current == '>':
            self._next()
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _code_block(self) -> bool:
        #===============================================================================
        # <code block> ::= <text with span elements> <code block'>
        #===============================================================================
        if self._text_with_span_elements():
            return self._code_block_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _code_block_1(self) -> bool:
        #===============================================================================
        # <code block'> ::= <text with span elements> <code block'>
        #                |  <line or paragraph end>
        #===============================================================================
        while self._text_with_span_elements():
            continue
        return self._line_or_paragraph_end()

    #-------------------------------------------------------------------------
    def _emph_or_strong_star(self) -> bool:
        #=======================================================================
        # <emph or strong *> ::= '*' <any chars but *> "**"
        #                     |  <any chars but *> '*'
        #=======================================================================
        if self._current == '*':
            self._next()
            self._append_mark( MDStrongBegin(self._currrent_index-2) )      ## $mark(Strng(index-2));
            self._any_chars_but( '*' )
            self.next()
            if self._current_2 == "**":
                self._next( 2 )
                self._append_mark( MDStrongEnd(self._currrent_index-2))     ## $mark(Strng(index-2));
                return True
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _emph_or_strong_underscore(self) -> bool:
        #=======================================================================
        # <emph or strong _> ::= '_' <any chars but *> "__"
        #                     |  <any chars but _> '_'
        #=======================================================================
        if self._current == '_':
            self._next()
            self._append_mark( MDStrongBegin(self._currrent_index-2) )      ## $mark(Strng(index-2));
            self._any_chars_but( '_' )
            self.next()
            if self._current_2 == "__":
                self._next( 2 )
                self._append_mark( MDStrongEnd(self._currrent_index-2))     ## $mark(Strng(index-2));
                return True
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _emphasis_or_strong_style(self) -> bool:
        #=======================================================================
        # <emphasis or strong style> ::= '*' <emph or strong *>
        #                             |  '_' <emph or strong _>
        #=======================================================================
        if self._current == '*':
            return self._emph_or_strong_star()
        elif self._current == '_':
            return self._emph_or_strong_underscore()
        else:
            return False

    #-------------------------------------------------------------------------
    def _escape(self) -> bool:
        #=======================================================================
        # <escape>       ::= '\\' <escaped char>
        # <escaped char> ::= '\\'  |  '`'  |  '*'  |  '_'  |  '{'
        #                 |  '}'   |  '['  |  ']'  |  '('  |  ')'
        #                 |  '#'   |  '+'  |  '-'  |  '.'  |  '!'
        #=======================================================================
        if self._current == '\\':
            self._next()
            if self._current in "\\`*_{}[]()#+-.!":
                self._append_mark( MDEscape(self._current_index-1) )    ## $mark(Esc(index-1));
                self._next()
                return True
        return False

    #-------------------------------------------------------------------------
    def _header_atx(self) -> bool:
        #=======================================================================
        # <header atx> ::= '#' <header atx'>
        #=======================================================================
        if self._current == '#':
            self._hdr = MDHeader(self._current_index, 1, True, False )  ## $hdr=HdrAtx(index);
            self._next()
            return self._header_atx_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_atx_1(self) -> bool:
        #=======================================================================
        # <header atx'> ::= '#' <header atx'>
        #                |  ' ' <text with span elements>
        #=======================================================================
        while self._current == '#':
            self._hdr.hdr_num += 1  ## $hdr.level++;
            self._next()
        if self._current == ' ':
            self._append_mark( self._hdr )  ## $mark(hdr);
            if self._text_with_span_elements():
                self._append_mark( MDHeader(self._current_index, self._hdr.hdr_num, False, False) ) ## $mark(HdrEnd(index));
                return True
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_setext(self) -> bool:
        #=======================================================================
        # <header setext> ::= '=' <header setext h1>
        #                  |  '-' <header setext h2>
        #                  |  EPS
        #=======================================================================
        if self._current == '=':
            self._hdr = MDHeader(self._current_index, 1, False, True )  ## $mark(HdrStxH1(index));
            return self._header_setext_h1()
        elif self._current == '-':
            self._hdr = MDHeader(self._current_index, 2, False, True )  ## $mark(HdrStxH2(index));
            return self._header_setext_h2()
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_setext_h1(self) -> bool:
        #=======================================================================
        # <header setext h1> ::= '=' <skip spaces> <header setext h1'>
        #    ## CAUTION: previous line of MD text was then H1
        #=======================================================================
        if self._current == '=':
            self._next()
            self._skip_spaces()
            return self._header_setext_h1_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_setext_h1_1(self) -> bool:
        #=======================================================================
        # <header setext h1'> ::= '=' <skip spaces> <header setext h1'>
        #                      |  <line or paragraph end>
        #=======================================================================
        while self._current == '=':
            self._next()
            self._skip_spaces()
        if self._line_or_paragraph_end():
            self._append_mark( MDHeader(self._current_index, 1, True, True) ) ## $mark(HdrEndH1(index));
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_setext_h2(self) -> bool:
        #=======================================================================
        # <header setext h2> ::= '-' <skip spaces> <header setext h2'>
        #    ## CAUTION: previous line of MD text was then H2
        #=======================================================================
        if self._current == '-':
            self._next()
            self._skip_spaces()
            return self._header_setext_h2_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _header_setext_h2_1(self) -> bool:
        #=======================================================================
        # <header setext h2'> ::= '-' <skip spaces> <header setext h2'>
        #                      |  <line or paragraph end>
        #=======================================================================
        while self._current == '-':
            self._next()
            self._skip_spaces()
        if self._line_or_paragraph_end():
            self._append_mark( MDHeader(self._current_index, 2, True, True) ) ## $mark(HdrEndH2(index));
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _horizontal_rule(self) -> bool:
        #=======================================================================
        # <horizontal rule> ::= <hrule star>
        #                    |  <hrule hyphen'>
        #=======================================================================
        return self._hrule_star() or self._hrule_hyphen_1()

    #-------------------------------------------------------------------------
    def _hrule_hyphen(self) -> bool:
        #=======================================================================
        # <hrule hyphen> ::= '-' <skip spaces> '-' <skip spaces> '-' <hrule hyphen'>
        #=======================================================================
        if self._current == '-':
            self._next()
            self._skip_spaces()
            if self._current == '-':
                self._skip_spaces()
            if self._current == '-':
                self.next()
                return self._hrule_hyphen_1()
        return False

    #-------------------------------------------------------------------------
    def _hrule_hyphen_1(self) -> bool:
        #=======================================================================
        # <hrule hyphen'> ::= <skip spaces> '-' <hrule hyphen'>
        #                  |  <line or paragraph end>
        #=======================================================================
        while True:
            self._skip_spaces()
            if self._current == '-':
                continue
            elif self._line_or_paragraph_end():
                self._append_mark( MDHRule(self._line_start, self._current_index) )     ## $mark(HR(line.start,index);
                return True
            else:
                return False

    #-------------------------------------------------------------------------
    def _hrule_star(self) -> bool:
        #=======================================================================
        # <hrule star> ::= '*' <skip spaces> '*' <skip spaces> '*' <hrule star'>
        #=======================================================================
        if self._current == '*':
            self._next()
            self._skip_spaces()
            if self._current == '*':
                self._skip_spaces()
            if self._current == '*':
                self.next()
                return self._hrule_star_1()
        return False

    #-------------------------------------------------------------------------
    def _hrule_star_1(self) -> bool:
        #=======================================================================
        # <hrule star'> ::= <skip spaces> '-' <hrule star'>
        #                  |  <line or paragraph end>
        #=======================================================================
        while True:
            self._skip_spaces()
            if self._current == '-':
                continue
            elif self._line_or_paragraph_end():
                self._append_mark( MDHRule(self._line_start, self._current_index) )     ## $mark(HR(line.start,index);
                return True
            else:
                return False

    #-------------------------------------------------------------------------
    def _html_entity(self) -> bool:
        #=======================================================================
        # <html entity> ::= '&' <non space chars> ';'
        #=======================================================================
        if self._current == '&':
            self._he_start = self._current_index    ## $he.start=index;
            self._next()
            while self._current != ' ':
                self._next()
            if self._current == ';':
                self._next()
                self._append_mark( MDHtmlEntity(self._he_start, self._current_index) )  ## $he.end=index, mark(he);
                return True
        return False

    #-------------------------------------------------------------------------
    def _html_tag(self) -> bool:
        #=======================================================================
        # <html tag> ::= <any chars but / \> > <html tag'>
        #=======================================================================
        while self._current not in "/>" and not self._end_of_text:
            self._next()
        return self._html_tag_1()

    #-------------------------------------------------------------------------
    def _html_tag_1(self) -> bool:
        #===============================================================================
        # <html tag'> ::= '/' '>'
        #              |  '>' ## CAUTION: then, search for the paired HTML tag without parsing in-between text
        #===============================================================================
        if self._current == '>':
            self._next()
            self._current_index = self._search_html_end( self._he_start, self._current_index )  ## $htm.end=index, searchEnd(htm);
            self._append_mark( MDHtmlTag(self._he_start, self._current_index) )                 ## mark(htm);
            return True
        elif self._current_2 == "/>":
            self._next( 2 )
            self._append_mark( MDHtmlEntity(self._he_start, self._current_index) )              ## $htm.end=index, mark(htm);
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _html_tag_or_automatic_link(self) -> bool:
        #=======================================================================
        # <html tag or automatic link> ::= '<' <html tag or automatic link'>
        #=======================================================================
        if self._current == '<':
            self._html_start = self._current_index      ## $htm.start=index;
            self._html_open = True                      ## $htm.open=True;
            self._next()
            return self.__html_tag_or_automatic_link_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _html_tag_or_automatic_link_1(self) -> bool:
        #=======================================================================
        # <html tag or automatic link'> ::= '/' <any chars but \> '\n' > '>'
        #                                |  <any chars but : / \> > <html tag or automatic link">
        #=======================================================================
        if self._current == '/':
            self._next()
            self._any_chars_but( ">\n" )
            if self._current == '>':
                self._next()
                return True
            else:
                return False
        else:
            self._any_chars_but( ":/>" )
            return self.__html_tag_or_automatic_link_2()

    #-------------------------------------------------------------------------
    def _html_tag_or_automatic_link_2(self) -> bool:
        #=======================================================================
        # <html tag or automatic link"> ::= <url'> '>'
        #                                |  <html tag'>
        #=======================================================================
        if self._url_1():
            if self._current == '>':
                self._next()
                ## $url.start=htm.start, $url.end++, $mark(AutLnk(url));
                return True
            else:
                return False
        else:
            return self._html_tag_1()

    #-------------------------------------------------------------------------
    def _image(self) -> bool:
        #=======================================================================
        # <image> ::= '!' <link>
        #=======================================================================
        if self._current == '!':
            self._next()
            return self._link()
        else:
            return False

    #-------------------------------------------------------------------------
    def _inlined_code(self) -> bool:
        #=======================================================================
        # <inlined code ::= '`' <inlined code'>
        #=======================================================================
        if self._current == '`':
            self._next()
            return self._inlined_code_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _inlined_code_1(self) -> bool:
        #=======================================================================
        # <inlined code'> ::= <any char but `> '`'
        #                  |  '`' <inlined code''>
        #=======================================================================
        if self._current == '`':
            self._next()
            return self._inlined_code_2()
        else:
            self._any_chars_but( '`' )
            if self._current == '`':
                self._next()
                return True
        return False

    #-------------------------------------------------------------------------
    def _inlined_code_2(self) -> bool:
        #=======================================================================
        # <inlined code''> ::= <any chars but `> '`' <inlined code '''>
        #=======================================================================
        self._any_chars_but( '`' )
        if self._current == '`':
            return self._inlined_code_3()
        else:
            return False

    #-------------------------------------------------------------------------
    def _inlined_code_3(self) -> bool:
        #=======================================================================
        # <inlined code '''> ::= '`'
        #                     |  <inlined code''>
        #=======================================================================
        if self._current == '`':
            self._next()
            return True
        else:
            return self._inlined_code_2()

    #-------------------------------------------------------------------------
    def _inlined_link(self) -> bool:
        #=======================================================================
        # <inlined link> ::= '[' <url> <title> ']'
        #=======================================================================
        if self._current == '[':
            if self._url() and self._title():
                if self._current == ']':
                    return True
        return False

    #-------------------------------------------------------------------------
    def _line_or_paragraph_end(self) -> bool:
        #=======================================================================
        # <line or paragraph end> ::= '\n' <line or paragraph end'>
        #                          | <ENDOFTEXT>  ## line end
        #=======================================================================
        if self._current == '\n':
            self._next()
            return self._line_or_paragraph_end_1()
        elif self._end_of_text:
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _line_or_paragraph_end_1(self) -> bool:
        #=======================================================================
        # <line or paragraph end'> ::= '\n' <line or paragraph end'>
        #                           | <ENDOFTEXT>
        #                           |  EPS
        #=======================================================================
        b_paragraph_end = False
        while not self._end_of_text and self._current == '\n':
            b_paragraph_end = True
            self._next()
        if self._end_of_text:
            ## paragraph end
            return True
        elif b_paragraph_end:
            ## paragraph end
            return True
        else:
            ## line end
            return True

    #-------------------------------------------------------------------------
    def _link(self) -> bool:
        #=======================================================================
        # <link> ::= <inlined link>
        #         |  <referenced link>
        #=======================================================================
        return self._inlined_link() or self.referenced_link()

    #-------------------------------------------------------------------------
    def _link_or_reference(self) -> bool:
        #=======================================================================
        # <link or reference> ::= '[' <linked text> ']' <link or reference'>
        #=======================================================================
        if self._current == '[':
            self._next()
            self._linked_text()
            if self._current != ']':
                return False
            else:
                return self._link_reference_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _link_reference_1(self) -> bool:
        #=======================================================================
        # <link or reference'> ::= ':' <reference>
        #                       |  <link>
        #=======================================================================
        if self._current == ':':
            return self._reference()
        else:
            return self._link()

    #-------------------------------------------------------------------------
    def _linked_text(self) -> bool:
        #=======================================================================
        # <linked text> ::= <any chars but ]> 
        #=======================================================================
        return self._any_chars_but( ']' )

    #-------------------------------------------------------------------------
    def _list(self) -> bool:
        #=======================================================================
        # <list> ::= <ordered list>
        #         |  <unordered list> ## CAUTION: "paragraphed" list items are not addressed there
        #=======================================================================
        return self._ordered_list() or self._unordered_list()

    #-------------------------------------------------------------------------
    def _list_bullet(self) -> bool:
        #=======================================================================
        # <list bullet> ::= '*'
        #                | '+'
        #                | '-'
        #=======================================================================
        if self._current in "-+*":
            self._next()
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def _max_3_spaces(self) -> bool:
        #=======================================================================
        # <max 3 spaces> ::= ' ' <max 3'>
        #                 |  EPS
        #=======================================================================
        if self._current == ' ':
            self._next()
            return self._max_3_spaces_1()
        else:
            return True

    #-------------------------------------------------------------------------
    def _max_3_spaces_1(self) -> bool:
        #=======================================================================
        # <max 3'> ::= ' ' <max 3''>
        #           |  EPS
        #=======================================================================
        if self._current == ' ':
            self._next()
            return self._max_3_spaces_2()
        else:
            return True

    #-------------------------------------------------------------------------
    def _max_3_spaces_2(self) -> bool:
        #=======================================================================
        # <max 3''> ::= ' '
        #            |  EPS
        #=======================================================================
        if self._current == ' ':
            self._next()
        return True

    #-------------------------------------------------------------------------
    def _maybe_setext_header(self) -> bool:
        #=======================================================================
        # <maybe setext header> ::= '\n' <header setext>
        #=======================================================================
        if self._current == '\n':
            self._next()
            return self._header_setext()
        else:
            return False

    #-------------------------------------------------------------------------
    def _maybe_star(self) -> bool:
        #=======================================================================
        # <maybe star> ::= '*' <maybe star'>
        #=======================================================================
        if self._current == '*':
            self._next()
            return self._maybe_star_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _maybe_star_1(self) -> bool:
        #=======================================================================
        # <maybe star'> ::= ' '
        #                |  <text with span elements>
        #=======================================================================
        if self._current == ' ':
            self._next()
            return True
        else:
            return self._text_with_span_elements()

    #-------------------------------------------------------------------------
    def _maybe_underscore(self) -> bool:
        #=======================================================================
        # <maybe underscore> ::= '_' <maybe underscore'>
        #=======================================================================
        if self._current == '_':
            self._next()
            return self._maybe_underscore_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _maybe_underscore_1(self) -> bool:
        #=======================================================================
        # <maybe underscore'> ::= ' '
        #                      |  <text with span elements>
        #=======================================================================
        if self._current == ' ':
            self._next()
            return True
        else:
            return self._text_with_span_elements()

    #-------------------------------------------------------------------------
    def _md_line(self) -> bool:
        #=======================================================================
        # <MD line> ::= <block element> | <space-starting elements> | <text with span elements> | <line or paragraph end>
        #=======================================================================
        return self._block_elements() or \
                self._space_starting_elements() or \
                self._text_with_span_elements() or \
                self._line_or_paragraph_end()

    #-------------------------------------------------------------------------
    def _number(self) -> bool:
        b_num = False
        while self._current in "0123456789":
            self._next()
            b_num = True
        return b_num
        
    #-------------------------------------------------------------------------
    def _ordered_item(self) -> bool:
        #=======================================================================
        # <ordered item> ::= <number> '.' <text with span elements>
        #=======================================================================
        if self._number():
            if self._current == '.':
                self._next()
                return self._text_with_span_elements()
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _ordered_list(self) -> bool:
        #=======================================================================
        # <ordered list> ::= <ordered item> <ordered list'>
        #=======================================================================
        if self._ordered_item():
            return self._ordered_list_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _ordered_list_1(self) -> bool:
        #=======================================================================
        # <ordered list'> ::= <ordered item> <ordered list'>
        #                  | <line or paragraph end>
        #=======================================================================
        while self._ordered_item():
            continue
        return self._line_or_paragraph_end()

    #-------------------------------------------------------------------------
    def _reference(self) -> bool:
        #=======================================================================
        # <reference> ::= <skip spaces> <url> <skip spaces> <reference title> '\n'
        #=======================================================================
        self._skip_spaces()
        if self._url():
            self._skip_spaces()
            self._reference_title()
            if self._current == '\n':
                return True
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _referenced_link(self) -> bool:
        #=======================================================================
        # <referenced link> ::= <skip spaces> '[' <referenced link'> ']'
        #=======================================================================
        self._skip_spaces()
        if self._current == '[':
            self._next()
            self._referenced_link_1()
            if self._current == ']':
                self._next()
                return True
            else:
                return False
        else:
            return False

    #-------------------------------------------------------------------------
    def _referenced_link_1(self) -> bool:
        #=======================================================================
        # <reference linked'> ::= <any chars but ]>
        #                      |  EPS
        #=======================================================================
        self._any_chars_but( ']' )
        return True

    #-------------------------------------------------------------------------
    def _reference_title(self) -> bool:
        #=======================================================================
        # <reference title> ::= '\n' <max 3 spaces> <reference title'> ## CAUTION: may lead to backward scanning if no '"' in next 4 chars
        #                    |  <reference title'>
        #=======================================================================
        if self._current == '\n':
            self._next()
            self._max_3_spaces()
        return self._reference_title_1()

    #-------------------------------------------------------------------------
    def _reference_title_1(self) -> bool:
        #=======================================================================
        # <reference title'> ::= '"' <any chars but newline and "> '"' <skip spaces> '\n' ## (maybe end-of-line is not needed)
        #=======================================================================
        if self._current == '"':
            self._next()
        self._any_chars_but( '\n"' )
        if self._current == '"':
            return False
        self._next()
        self._skip_spaces()
        if self._current == '\n':
            self._next()
        return True

    #-------------------------------------------------------------------------
    def _skip_spaces(self):
        #=======================================================================
        # <skip spaces> ::= ' ' <skip spaces>
        #                |  EPS
        #=======================================================================
        while self._current == ' ':
            self._next()

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
            self._next()
            return self._space_elements_2()
        elif self._current == '\t':
            self._next()
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
            self._next()
            return self._space_elements_3()
        elif self._current == '\t':
            return self._code_block()
        elif self._current == '\n':
            self._next()
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
            self._next()
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
            self._next()
            return self._space_elements_1()
        elif self._current == '\t':
            self._next()
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
        #                            |  <any chars but & < * _ ` \\ \n> <maybe setext header>
        #=======================================================================
        if self._html_entity() or \
            self._html_tag_or_automatic_link() or \
            self._emphasis_or_strong_style() or \
            self._inlined_code() or \
            self._escape() or \
                self._any_chars_but( "&<*_`\\\n" ):
            return self._maybe_setext_header()
        else:
            return False
        
    #-------------------------------------------------------------------------
    def _title(self) -> bool:
        #=======================================================================
        # <title> ::= '"' <any chars but newline and "> '"'
        #=======================================================================
        if self._current == '"':
            self._next()
            self._any_chars_but( '\n"' )
            if self._current == '"':
                self._next()
                return True
        return False
        
    #-------------------------------------------------------------------------
    def _unordered_item(self) -> bool:
        #=======================================================================
        # <unordered item> ::= <list bullet> <text with span elements>
        #=======================================================================
        if self._list_bullet():
            return self._text_with_span_elements()
        else:
            return False

    #-------------------------------------------------------------------------
    def _unordered_list(self) -> bool:
        #=======================================================================
        # <unordered list> ::= <unordered item> <unordered list'>
        #=======================================================================
        if self._unordered_item():
            return self._unordered_list_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _unordered_list_1(self) -> bool:
        #=======================================================================
        # <unordered list'> ::= <unordered item> <unordered list'>
        #                    |  <line or paragraph end> 
        #=======================================================================
        while self._unordered_item():
            continue
        return self._line_or_paragraph_end()

    #-------------------------------------------------------------------------
    def _url(self) -> bool:
        #=======================================================================
        # <url> ::= <alphanum chars> <url'>
        #=======================================================================
        if 'a' <= self._current <= 'z' or \
            'A' <= self._current <= 'Z' or \
            '0' <= self._current <= '9':
            self._next()
            return self._url_1()
        else:
            return False

    #-------------------------------------------------------------------------
    def _url_1(self) -> bool:
        #=======================================================================
        # <url'> ::= "://" <any chars but ] and ">
        #=======================================================================
        if self._current_3 == "://":
            self._next( 3 )
            self._any_chars_but( ']"' )
            return True
        else:
            return False

    #=========================================================================
    #-------------------------------------------------------------------------
    def _append_mark(self, md_mark:MDMark):
        self._md_marks.append( md_mark )
    #-------------------------------------------------------------------------
    @property
    def _current(self) -> str:
        return '' if self._end_of_text else self._md_text[ self._current_index ]
    #-------------------------------------------------------------------------
    @property
    def _current_2(self) -> str:
        try:
            return self._md_text[ self._current_index:self._current_index+2 ]
        except:
            return ''
    #-------------------------------------------------------------------------
    @property
    def _current_3(self) -> str:
        try:
            return self._md_text[ self._current_index:self._current_index+3 ]
        except:
            return ''
    #-------------------------------------------------------------------------
    @property
    def _end_of_text(self) -> bool:
        return self._current_index == len( self._md_text )
    #-------------------------------------------------------------------------
    def _next(self, n:int=1):
        self._current_index += n
    #-------------------------------------------------------------------------
    def _search_html_end(self, start:int, end:int):
        html_tag = self._md_text[start:end].split(' ', 1)[0]
        html_end = self._md_text[end:].find( '</' + html_tag + '>')
        return html_end + len(html_tag) + 3
        
#=====   end of   scripts.utils.md_parser   =====#
