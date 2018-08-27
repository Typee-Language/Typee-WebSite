# Markdown to HTML Translator - Design

This document presents the design of the translator of Markdown documents into 
HTML content.

We had to code this translator by our own because we didn't find any Open 
Source tool accepting every Markdown tags and goodies that GitHub accepts. 
Even the Markdown excellent tool available on PyPi could not be used for our 
purpose (we unsuccessfully tried to).

Notably, GitHub uses an extended Markdown specification, the 
[GitHub Flavored Markdown Spec][GFM syntax] (or _GFM_). This spec extends MD 
with __Tables__, __Tasklists__, __Strikethrough__, __Autolinks__ and specifies 
some __disallowed raw HTML__ tags. GitHub allows also some other goodies 
__that we do not coded in our tool__. For instance, 
[Mermaid](https://mermaidjs.github.io/) JavaScript goodies for drawing 
flowcharts adn diagrams __is not__ integrated in our tool.

The curious reader will get access to the specs of initial Markdown syntax on 
its [project Web page][standard MD syntax].


## 1. Two translating classes and the associated scripts and utilities

GFM being extending MD, we first designed a `MDtoHTML` class that fully 
translates standard Markdown text.

A second class, `GFMtoHTML`, inherits from MDtoHTML and augments it with GFM 
adds (i.e tables alignment, etc.) or modifies its behavior (e.g. about the 
break-lines specs which are different between MD and GFM).

Both classes definitions are grouped in a single Python module: 
`scripts/utils/md_to_html.py`. We describe these two classes in a next 
section.

Scripts are also provided to ease their use on directories content. They can 
be accessed in directory `scripts/`. We describe their usage in a dedicated 
further section also.

Finally, two utility modules have been developed.

- `scripts/utils/md_mark.py` describes all the MD marks that can be detected 
   in MD texts and helps locating them in this text;
- `scripts/utils/md_marks_list.py` defines a class for lists of MD marks and 
   their operations.

They both are imported and classes they define are used in classes `MDtoHTML` 
and `GFMtoHTML`. We discuss the two modules and the classes they define in 
next section.



## 2. Utility Modules and Classes

As is said above, two modules define utilities for the translation of MD or 
GFM in HTML. They both can be found in directory `scripts/utils/`. We discuss 
them in the two next sub-sections.


### 2.1 `md_mark.py`

This module defines classes that are each associated with a Markdown tag.

A base class, `MDMark`, stores the starting and ending points of a detected MD 
tag in an MD text. These points are instances of class `LineColumn` which 
remebers the line number and the column index in this line for any "point". 
`LineColumn` can be compared or added.

For each MD tag, a dedicated class is defined. Standard MD defines two kinds 
of tags: Block elements and Span elements.

Notice: every MD mark class gets a unique tag-attribute: `CLASS`. It may be 
used to characterize the class of the mark without having to test the class 
it is an instance of (via Python built-in funcion `isinstanceof()`).


#### Block Elements

We list here the classes dedicated to the block elements of MD.

`MDHeader` describes header tags. These are of two kinds: _Setext_ or _atx_. 
They all are characterized by the "point" where they are detected in the MD 
text. Remember, such a point is of class `LineColumn` and stores the line 
number and the column index in this line of the first character of the MD tag. 
_Setext_ headers are defined with two lines of MD text, while _atx_ ones are 
defined with a single line of MD text. This is an important information to 
keep in memory, since for _Setext_ headers the second defining line must be 
skipped and not put in the resulting HTML text. For _Setext_ headers, the 
start point of the header is set to column zero of current line and end point 
is set to current line +2 and column 0. For _atx_ headers, the start point is 
set to current line and column equal to header level+1 and the end point is 
set to the end of line. The text of the header is the text within current 
line, from which every preceeding and ending hashes are removed. Finally, 
instances of class `MDHeader` embed the level of the header.  
(_atx headers are from \<H1> to \<H6>; Setext ones are either \<H1> or 
\<H2>_)
Please notice that for every detected header, two marks are generated. The 
first one marks the starting point of the header, the second one marks its 
ending point. A boolean remembers this status.

`MDBlockQuote` memorizes blockquote MD tags. Start and end of related tag is 
stored in there, plus the level of nesting of the quote.

`MDListItem` stores the starting end ending points of the MD tag of an item 
belonging to an unordered list. It stores also the nested level of the item.

`MDListNumItem` stores also the starting and ending points of the MD tag of an 
item belonging to an ordered list. It stores also the nested level of the 
item.

`MDCodeBlock` represents a GFM tag. It stores its starting point in the MD 
line text and its ending point in the same line. It also stores the computer 
language of the displayed code when it is available in the source text.

`MDCodeLine` represents a line of code. It stores the starting point of the 
code line in the MD line text.

`MDHRule` describes horizontal rules. The only thing to remeber here is the 
line number of the MD text where their different tags are appearing. This is 
done with the sole starting point of the mark. Ten ending points is set to 
`None`.


#### Span Elements

Span elements are MD tags that are directly embedded in the text.

Links are such elements of MD. They can be of different types.

`MDIsolatedAmpersand` stores the exact position of isolated character '&' in 
the MD text, when this character is not the starting point of an HTML tag. 
This class inherits from `MDMark`.

`MDIsolatedLT` stores the exact position of isolated character '<' in 
the MD text, when this character is not the starting point of an HTML tag. 
This class inherits from `MDMark`.

`MDLink` is a base class that stores starting and ending points of the link MD 
tag plus the link text that is associated with it and the source text that 
will have to be put in the resulting HMTL file.

`MDLinkTitle` is a link MD tag that contains also a _title_ information. This 
added title is also stored by this class. This class inherits from `MDLink`.

`MDLinkAuto` is the class of links that are shown as-is in the MD text. In 
standard MD, they are enclosed in pairs of `<` and `>`. In GFM, it is extended 
to URLs preceded and succeded by spaces. This MD tag duplicates the as-is text 
into the text adn the link that are associated with this MD tag. Automatic 
links remember the point of their starting tag (i.e. either `<` or ` `), the 
point of their ending tag (i.e. either `>` or ` `) and the text in-between. 
This class inherits from `MDLink`.  
Notice: MD and GFM specifications for automatic links differ.

`MDLinkRef` represents links taht are specified by reference in MD text. The 
refrence is stored in place of the attribute `link` of class `MDLink` from 
which class `MDLinkRef` inherits.

`MDLinkAutoRef` inherits from class `MDLinkRef`. It describes link MD tags 
whose text is also the reference of the link to be ued in the final HTML text.

`MDEmphasis` stores the point in MD text where an emphasis tag has been 
detected. There are two such marks for any emphasised text. The first one 
describes the entry point of the emphasised text in the MD text. The second 
one describes the end of the emphasised text. For each of these marks, the 
starting point and the ending point of the tag are stored.

`MDStrong` stores the point in MD text where a strong tag has been detected. 
There are two such marks for any strongified text. The first one describes the 
entry point of the strongified text in the MD text. The second one describes 
the end of the strongified text. For each of these marks, the starting point 
and the ending point of the tag are stored.

`MDCodeInlined` describes inlined code text tags. There are two such marks for 
any code-ified text. The first one describes the entry point of the code-ified 
text in the MD text. The second one describes the end of the code-ified text. 
For each of these marks, the starting point and the ending point of the tag 
are stored.

`MDImage` stores information about image MD tags. These are the starting point 
of this tag in the MD text, the alternative text to be displayed in browsers, 
the text of the link to the image and an optional title for the image
(defaults to None). this class inherits from class `MDLinkTitle`.

`MDImageRef` inherits from class `MDImage`. It defines a reference to a link 
rather than the text of the link to the image.

`MDEscape` defines the point in the MD text of an escape sequence of 
characters. In standard MD, not all characters are escaped. Only the ones in 
this next string are: ``" \ ` * _ { } [ ] ( ) # + - . ! "``.


#### GFM Extensions

GitHub Flavored Markdown extends the standard Markdown with new tags or with 
extended MD tags.

`MDBlockQuoteML` describes Multi-Lines Blockquotes. The starting point of this 
tag indicates the line where it appears in the GFM text. The ending point 
indicates the line where the same tag appears a second time. The in-between 
text is the blockquoted text. This class inherits from `MDMark`.

`MDInlineAddition` describes text to be displayed with "addition" 
characteristics (i.e. mainly displayed with green background). The starting 
point indicates the position of the first character of GFM entering tag within 
the GFM text. The ending point indicates the position of the first character 
of the paired GFM tag. The in-between text in the GFM text is the text to be 
colored in the tareget HTML text. This class inherits from `MDMark`.

`MDInlineDeletion` describes text to be displayed with "deletion" 
characteristics (i.e. mainly displayed with pink background). The starting 
point indicates the position of the first character of GFM entering tag within 
the GFM text. The ending point indicates the position of the first character 
of the paired GFM tag. The in-between text in the GFM text is the text to be 
colored in the target HTML text. This class inherits from `MDMark`.

`MDTable` stores the starting point of a table and the ending point of it. 
Those points correspond to the first char describing the table and to the last 
character of its description. Those characters may be _pipes (\|) as well as 
any other character corresponding to the text to be HTML-ed. This class 
inherits from `MDMark`.

`MDTableRow` describes a row of a table. The start and end points correspond 
to the row starting point and the row ending point in the GFM text. They are 
not used because the main info that `MDTableRow` contains is the list of texts 
to be inserted in the cells of this row. Argument `colns_txt` passed at 
construction time is the text to be split into indivdual cells. It is split 
internally and attribute `txt` finally contains the content of every cells. 
This class inherits from `MDMark`.

`MDTableHeader` indicates the starting point and the ending point of the row 
that describes the headers of the columns of the table. After construction 
time, attribute `txt` contains the header text of every column of the table. 
This class inherits from `MDTableRow`.

`MDTableAlign` describes the alignment of text in the cells of every columns. 
If this information is available in the GFM description of the table, it has 
to be evaluated by an external parser that can initialize the corresponding 
alignment for each row by calling method `set_align()` with alignment tag, 
described with constants `MDTableAlign.LEFT`, `MDTableAlign.CENTER` and 
`MDTableAlign.RIGHT`. The index of the column may be specified when setting 
the alignment of a column. If it is not specified, the alignment value is just 
appended to the list of alignments. Once alignments set, they can be accessed 
via attribute `aligns` (which is a list). This class inherits from `MDMark`.

`MDFootnote` stores the starting and the ending points of a footnote tag. It 
associated a text with this footnote, for it to be displayed at end of page.
The text in-between contains the footnote number. This class inherits from 
`MDMarkText`.

`MDFootnoteRef`  stores the starting and the ending points of a footnote 
reference tag. It associated the reference text with this footnote. This 
reference text will be later used to link with the footnote text in the HTML 
text. This class inherits from `MDMarkText`.


### 2.2 `md_marks_list.py`

This module defines the class of the lists of MD marks and the few operations 
associated with them.

Class `MDMarksList` describes such lists. It inherits from _Python_ built-in 
type `list`. MD marks can then easily be appended to its instances along the 
parsing of some MD text. It is also easy to get access to its content either 
by indexing it, which is not the recommended way, or by iterating on it with a 
`for` loop, which the recommended way.

While this module contains very little code, we have decided to create it 
nevertheless, in case we woulf late rmodify this code and augment it to get 
more functionnalities.



## 3. _MD_ and _GFM_ Translators Modules

### 3.1 Markdown (_MD_) to HTML Translator

Class `MDtoHTML` defines all the needed stuff to translate 
["standard" Markdown ][standard MD syntax] as initially developed by John 
Gruber with Aaron Swartz.


#### 3.1.1 `__init__()`

The constructor, `__init__()`, directly translates the content of a `.md` file 
when a related file path is provided as input argument. The result of the 
translation is then available in attribute `self.html_text`. If no file path 
is provided as input argument to the constructor, then attribute `.html_text` 
is `None` and it is the responsibility of the user to call method 
`translate()` on the constructed instance of the class.


#### 3.1.2 `translate()`

Method `translate()` returns the translated text in its HTML5 form. Detected 
errors are neither logged nor displayed. Its up to the user to verify that 
the HTML text returned corresponds to what he expected.


#### 3.1.3 General design

An internal class, `_MDMark`, stores the line and column numbers where MD tags 
are detected. At construction time, the attribute `_marks` is set to an empty 
list. This list will store all MD marks detected in the MD source file. It is 
ordered on lines then on column numbers of those detected MD marks.

Another internal class, `_Refs`, stores all the references that are detected 
during the parsing of the MD source file. This is a dictionary with reference 
text as the key and link text as the item. It is instantiated at construction 
time with attribute `_refs`, set as empty at that time.

The list of MD marks indexes also the place vers references are... referenced 
(i.e. line and column numbers of starting and ending text in MD source file.

Method `translate()` runs in two phases:
- The first one parses the _MD_ text and marks the detected MD tags in 
attribute `_marks`. During this first phase, forward references are also 
detected and remembered in attribute `_refs`.
- During the second phase, the HTML text is generated using the marks and the 
references detected during first phase.



### 3.2 GitHub Flavored Markdown (_GFM_) to HTML Translator

Class `GFMtoHTML` inherits from class `MDtoHTML` and:
- augments it with the _GFM_ added marks;
- modifies it with _GFM_ specs that differ from their _MD_ equivalent specs.


#### 3.2.1 `__init__()`

The constructor, `__init__()`, acts exactly as does the base class 
constructor. It directly translates the content of a `.md` file when a related 
file path is provided as input argument. The result of the translation is then 
available in attribute `self.html_text`. If no file path is provided as input 
argument to the constructor, then attribute `.html_text` is `None` and it is 
the responsibility of the user to call method `translate()` on the constructed 
instance of the class.


#### 3.2.2 `translate()`

Method `translate()` returns the translated text in its HTML5 form. Detected 
errors are neither logged nor displayed. Its up to the user to verify that 
the HTML text returned corresponds to what he expected.


#### 3.2.3 General design

Method `translate()` of base class `MDtoHTML` is overwritten in the inheriting 
class `GFMtoHTML`. Specificities of GitHub Flavored Markdown, the ones that 
are augmenting the original Markdown specification, are implemented in method 
`translate()` aside the implementation of the other standard MD marks that are 
already available in the base class.



## 4. Related Scripts Usage

Two scripts, each related to one of the two classes discussed above, are 
provided to ease the translation of MD files into HTML.


### 4.1 Markdown to HTML Script

Module `scripts/md_to_html_script.py` runs the translation of "standard" MD 
text in HTML5 text. This is not the one we use for feeding our site 
www.typee.ovh but this script could be useful for any project using MD text 
files to be translated in HTML5.

(_options have to be described for command line_)


### 4.2 GitHub Flavored Markdown (_GFM_) to HTML Script

Module `scripts/gfm_to_html_script.py` runs the translation of GitHub Flavored 
Markdown text in HTML5 text. This is the one we use for feeding our site 
www.typee.ovh.

(_options have to be described for command line_)



[standard MD syntax]: https://daringfireball.net/projects/markdown/syntax
[GFM syntax]: https://github.github.com/gfm


## Annex - This document revisions history

| Date | Rev. | Author | Comments |
|---|---|---|---|
| 2018-08-21 | 0.0.1 | Schmouk | Creation. |
| 2018-08-22 | 0.0.2 | Kerm    | Added utility classes for MD tags, see module `scripts/utils/md_mark.py` |
| 2018-08-23 | 0.0.3 | Schmouk | Modified global design; Modified structure of this document; Added class for defining list of MD marks and their operations; Added classes for the description of MD marks and their location within MD texts. |
| 2018-08-24 | 0.0.4 | Schmouk | Added description of missing classes in section 2. |
| 2018-08-24 | 0.0.5 | Kerm    | Modified description of a few MD and GFM marks classes according to the current development of module `script/utils/md_to_html.py` |
|  |  |  |  |
