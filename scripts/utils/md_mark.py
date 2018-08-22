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
    def __add__(self, other:(LineColumn,tuple)) -> LineColumn:
        if isinstance( other, tuple ):
            return LineColumn( self.line + other[0], self.coln + other[1] )
        else:
            return LineColumn( self.line + other.line, self.coln + other.coln )
   
    #-------------------------------------------------------------------------
    def __gt__(self, other:LineColumn) -> bool:
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
    def __gt__(self, other:MDMark) -> bool:
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
class MDBlockQuote( MDMarkText ):
    '''
    The class of MD blocquotes - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, mark_text:MDMarkText):
        super().__init__( mark_text.start, mark_text.end )
        self.block = [ mark_text ]
    #-------------------------------------------------------------------------
    def add_text(self, mark_text:MDMarkText):
        self.block.append( mark_text )
        self.start = min( self.start, mark_text.start )
        self.end   = max( self.end  , mark_text.end   )
    #-------------------------------------------------------------------------
    CLASS = 'BLCK'


#=============================================================================
class MDCode( MDMarkText ):
    '''
    The class of MD code - plus GFM specificity.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, code_source_language:str=None):
        super().__init__( start, end, code_source_language )
    #-------------------------------------------------------------------------
    @property
    def language(self): return self.txt
    #-------------------------------------------------------------------------
    CLASS = 'COD'


#=============================================================================
class MDCodeInlined( MDMarkText ):
    '''
    The class of MD inlined code.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt )
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
class MDHeader( MDMarkText ):
    '''
    The class of MD headers.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, hdr_num:int, txt:str ):
        super().__init__( start, start+(0,len(txt)), txt )
        self.hdr_num = hdr_num
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
class MDLinkRef( MDMarkText ):
    '''
    The class of MD links by reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, ref:str):
        super().__init__( start, end, txt )
        self.ref =  ref
    #-------------------------------------------------------------------------
    CLASS = 'LNKREF'


#=============================================================================
class MDLinkText( MDLinkRef ):
    '''
    The class of MD links by text reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str):
        super().__init__( start, end, txt, txt )
    #-------------------------------------------------------------------------
    CLASS = 'LNKTXT'


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
class MDList( MDMark ):
    '''
    The class of MD lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'LST'


#=============================================================================
class MDListItem( MDMark ):
    '''
    The class of MD items of lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'LSTITM'


#=============================================================================
class MDNumberedList( MDMark ):
    '''
    The class of MD numbered lists.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn):
        super().__init__( start, end )
    #-------------------------------------------------------------------------
    CLASS = 'NBLST'


#=============================================================================
class MDReference( MDLink ):
    '''
    The class of MD links by reference.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, ref:str):
        super().__init__( start, end, txt, ref )
    #-------------------------------------------------------------------------
    CLASS = 'RFR'


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
    def __init__(self, start:LineColumn, end:LineColumn, nb_colns:int):
        super().__init__( start, end )
        self.nb_colns = nb_colns
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
class MDTableHeader( MDMark ):
    '''
    The class of GFM headers of tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:int, end:int, colns_txt:list=None ):
        super().__init__( start, end )
        self.txt = colns_txt if colns_txt else []
    #-------------------------------------------------------------------------
    def add_coln_txt(self, txt:str):
        self.txt.append( txt )
    #-------------------------------------------------------------------------
    CLASS = 'TBLHDR'


#=============================================================================
class MDTableRow( MDTableHeader ):
    '''
    The class of GFM headers of tables - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:int, end:int, colns_txt:list=None ):
        super().__init__( start, end, colns_txt )
    #-------------------------------------------------------------------------
    CLASS = 'TBLROW'


#=============================================================================
class MDImage( MDLinkTitle ):
    '''
    The class of MD images - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, link:str, title:str):
        super().__init__( start, end, txt, link, title )
    #-------------------------------------------------------------------------
    CLASS = 'IMG'


#=============================================================================
class MDImageRef( MDImage ):
    '''
    The class of MD images set by reference - GFM specific.
    '''
    #-------------------------------------------------------------------------
    def __init__(self, start:LineColumn, end:LineColumn, txt:str, ref:str, title:str):
        super().__init__( start, end, txt, ref, title )
    #-------------------------------------------------------------------------
    @property
    def ref(self):  return self.link
    #-------------------------------------------------------------------------
    CLASS = 'IMGREF'

        
#=====   end of   scripts.utils.md_mark   =====#

