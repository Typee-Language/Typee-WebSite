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
class LineColumn:
    """
    The class of line and column numbers in a text.
    """    
    #-------------------------------------------------------------------------
    def __init__(self, line:int=0, coln:int=0):
        '''
        Stores line and column numbers
        '''
        self.line, self.coln = line, coln
    #-------------------------------------------------------------------------
    def __add__(self, other):
        if isinstance( other, tuple ):
            return LineColumn( self.line + other[0], self.coln + other[1] )
        else:
            return LineColumn( self.line + other.line, self.coln + other.coln )
    #-------------------------------------------------------------------------
    def __gt__(self, other) -> bool:
        return self.line < other.line or (self.line == other.line and self.coln < other.coln)


#=============================================================================
class MDMark:
    """
    The class of detected marks in a Markdown text.
    """    
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        '''
        Constructor.
        
        Sets the starting and the ending point od Markdown marks in an MD text.
        
        Args:
            start: LineColumn
                the line number and the column index in this line of the
                starting point of the MD mark in the MD text.
            end: LineColumn
                the line number and the column index in this line of the
                ending point of the MD mark in the MD text.
        '''
        self.start, self.end = start, end
    #-------------------------------------------------------------------------
    def __gt__(self, other) -> bool:
        return self.start < other.start


#=============================================================================
class MDMarkText( MDMark ):
    '''
    The class of marked text.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end )
        self.txt = txt


#=============================================================================
class MDBlockQuote( MDMark ):
    '''
    The class of MD blockquotes.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, level:int):
        super().__init__( start, end )
        self.level = level
    #-------------------------------------------------------------------------
    CLASS = 'BLCK'


#=============================================================================
class MDBlockQuoteML( MDMark ):
    '''
    The class of GFM Multi-Lines blockquotes - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, level:int):
        super().__init__( start, end )
        self.level = level
    #-------------------------------------------------------------------------
    CLASS = 'BLCKML'


#=============================================================================
class MDBreakLine( MDMark ):
    '''
    The class of MD breaklines - i.e. two or more spaces at end of line.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'BRKLN'


#=============================================================================
class MDCodeBlock( MDMarkText ):
    '''
    The class of MD code - plus GFM specificity.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, code_source_language:str=None):
        super().__init__( start, end, code_source_language )
    #-------------------------------------------------------------------------
    @property
    def language(self): return self.txt  # GFM specific
    #-------------------------------------------------------------------------
    CLASS = 'CODBLK'


#=============================================================================
class MDCodeLine( MDMark ):
    '''
    The class of MD lines of code
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn):
        super().__init__( start, None )
    #-------------------------------------------------------------------------
    CLASS = 'CODLIN'


#=============================================================================
class MDCodeInlined( MDMark ):
    '''
    The class of MD inlined code.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'CODINL'


#=============================================================================
class MDEmphasis( MDMark ):
    '''
    The class of MD emphasis.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'EMPH'


#=============================================================================
class MDEscape( MDMark ):
    '''
    The class of MD escape sequences.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'ESC'


#=============================================================================
class MDFootnote( MDMarkText ):
    '''
    The class of GFM footnote tags.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt )
    #-------------------------------------------------------------------------
    CLASS = 'FOOTNT'


#=============================================================================
class MDFootnoteRef( MDMarkText ):
    '''
    The class of GFM footnote rference tags.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt )
    #-------------------------------------------------------------------------
    CLASS = 'FOOTNT'


#=============================================================================
class MDHeader( MDMark ):
    '''
    The class of MD headers.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, hdr_num:int, is_entering_point:bool, is_setext:bool ):
        if is_setext:
            end = LineColumn( start.line + 2, 0 )
        else:
            end = LineColumn( start.line, hdr_num+1 )
            
        super().__init__( start, end )
        self.hdr_num           = hdr_num
        self.is_setext         = is_setext
        self.is_entering_point = is_entering_point
    #-------------------------------------------------------------------------
    CLASS = 'HDR'


#=============================================================================
class MDHRule( MDMark ):
    '''
    The class of GFM horizontal rules - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn ):
        super().__init__( start, None )
    #-------------------------------------------------------------------------
    CLASS = 'HRUL'


#=============================================================================
class MDLinebreak( MDMark ):
    '''
    The class of MD line breaks.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn):
        super().__init__( start, None )
    #-------------------------------------------------------------------------
    CLASS = 'LINBRK'


#=============================================================================
class MDInlineAddition( MDMark ):
    '''
    The class of GFM additions - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'INLADD'


#=============================================================================
class MDInlineDeletion( MDMark ):
    '''
    The class of GFM deletions - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'INLDEL'


#=============================================================================
class MDIsolatedAmpersand( MDMark ):
    '''
    The class of HTML isolated ampersand characters.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn):
        super().__init__( start, None )
    #-------------------------------------------------------------------------
    CLASS = 'ISLAMP'


#=============================================================================
class MDIsolatedLT( MDMark ):
    '''
    The class of HTML isolated '<' characters.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn):
        super().__init__( start, None )
    #-------------------------------------------------------------------------
    CLASS = 'ISLLT'


#=============================================================================
class MDLink( MDMarkText ):
    '''
    The class of MD links.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, link:str):
        super().__init__( start, end, txt )
        self.link = link
    #-------------------------------------------------------------------------
    CLASS = 'LNK'


#=============================================================================
class MDLinkAuto( MDLink ):
    '''
    The class of MD automatic links.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt, txt )
    #-------------------------------------------------------------------------
    CLASS = 'LNKAUT'


#=============================================================================
class MDLinkTitle( MDLink ):
    '''
    The class of MD links with title.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, link:str, title:str):
        super().__init__( start, end, txt, link )
        self.title = title
    #-------------------------------------------------------------------------
    CLASS = 'LNKTITL'


#=============================================================================
class MDLinkRef( MDLink ):
    '''
    The class of MD links by reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, ref:str):
        super().__init__( start, end, txt, ref )
    #-------------------------------------------------------------------------
    @property
    def ref(self): return self.link
    #-------------------------------------------------------------------------
    CLASS = 'LNKREF'


#=============================================================================
class MDLinkAutoRef( MDLinkRef ):
    '''
    The class of MD auto links by text reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt, txt )
    #-------------------------------------------------------------------------
    CLASS = 'LNKARF'


#=============================================================================
class MDList( MDMark ):
    '''
    The class of MD lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, nested_level:int):
        super().__init__( start, end )
        self.nested_level = nested_level
    #-------------------------------------------------------------------------
    CLASS = 'LST'


#=============================================================================
class MDListItem( MDList ):
    '''
    The class of MD items of lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, nested_level:int):
        super().__init__( start, end, nested_level )
    #-------------------------------------------------------------------------
    CLASS = 'LSTITM'


#=============================================================================
class MDListNumItem( MDList ):
    '''
    The class of MD numbered lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, nested_level:int):
        super().__init__( start, end, nested_level )
    #-------------------------------------------------------------------------
    CLASS = 'LSTNUM'


#=============================================================================
class MDReference( MDLinkTitle ):
    '''
    The class of MD links by reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, ref:str, title:str=None):
        super().__init__( start, end, txt, ref, title )
    #-------------------------------------------------------------------------
    CLASS = 'RFR'


#=============================================================================
class MDStrikethrough( MDMark ):
    '''
    The class of MD strikethrough.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'STRKT'


#=============================================================================
class MDStrong( MDMark ):
    '''
    The class of MD strong.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'STRNG'


#=============================================================================
class MDTable( MDMark ):
    '''
    The class of GFM tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'TABL'


#=============================================================================
class MDTableAlign( MDMark ):
    '''
    The class of columns alignment in GFM tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, nb_colns:int=None):
        super().__init__( start, end )
        self.aligns = [MDTableAlign.LEFT]*nb_colns if nb_colns else []
    #-------------------------------------------------------------------------
    def set_align(self, align:int, index:int=None):
        try:
            self.aligns[index] = align
        except:
            self.aligns.append( align )
    #-------------------------------------------------------------------------
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2
    #-------------------------------------------------------------------------
    CLASS = 'TBLALGN'


#=============================================================================
class MDTableRow( MDMark ):
    '''
    The class of GFM headers of tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:int, end:int, colns_txt:str ):
        super().__init__( start, end )
        self.txt = [ row_txt.trim() for row_txt in colns_txt.split('|') if row_txt.trim() != '' ]
    #-------------------------------------------------------------------------
    CLASS = 'TBLROW'


#=============================================================================
class MDTableHeader( MDTableRow ):
    '''
    The class of GFM headers of tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:int, end:int, colns_txt:str ):
        super().__init__( start, end, colns_txt )
    #-------------------------------------------------------------------------
    CLASS = 'TBLHDR'


#=============================================================================
class MDImage( MDLinkTitle ):
    '''
    The class of MD images - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, alt_txt:str, link:str, title:str=None):
        super().__init__( start, end, alt_txt, link, title )
    #-------------------------------------------------------------------------
    CLASS = 'IMG'


#=============================================================================
class MDImageRef( MDImage ):
    '''
    The class of MD images set by reference - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, alt_txt:str, ref:str, title:str=None):
        super().__init__( start, end, alt_txt, ref, title )
    #-------------------------------------------------------------------------
    @property
    def ref(self):  return self.link
    #-------------------------------------------------------------------------
    CLASS = 'IMGREF'

        
#=====   end of   scripts.utils.md_mark   =====#

