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


## 1. Two translating classes and the associated scripts

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


## 3. _MD_ and _GFM_ Translators Modules

#### 3.1 Markdown (_MD_) to HTML Translator

Class `MDtoHTML` defines all the needed stuff to translate 
["standard" Markdown ][standard MD syntax] as initially developed by John 
Gruber with Aaron Swartz.


##### `__init__()`

The constructor, `__init__()`, directly translates the content of a `.md` file 
when a related file path is provided as input argument. The result of the 
translation is then available in attribute `self.html_text`. If no file path 
is provided as input argument to the constructor, then attribute `.html_text` 
is `None` and it is the responsibility of the user to call method 
`translate()` on the constructed instance of the class.


##### `translate()`

Method `translate()` returns the translated text in its HTML5 form. Detected 
errors are neither logged nor displayed. Its up to the user to verify that 
the HTML text returned corresponds to what he expected.


##### General design

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



#### 3.2 GitHub Flavored Markdown (_GFM_) to HTML Translator

Class `GFMtoHTML` inherits from class `MDtoHTML` and:
- augments it with the _GFM_ added marks;
- modifies it with _GFM_ specs that differ from their _MD_ equivalent specs.


##### `__init__()`

The constructor, `__init__()`, acts exactly as does the base class 
constructor. It directly translates the content of a `.md` file when a related 
file path is provided as input argument. The result of the translation is then 
available in attribute `self.html_text`. If no file path is provided as input 
argument to the constructor, then attribute `.html_text` is `None` and it is 
the responsibility of the user to call method `translate()` on the constructed 
instance of the class.


##### `translate()`

Method `translate()` returns the translated text in its HTML5 form. Detected 
errors are neither logged nor displayed. Its up to the user to verify that 
the HTML text returned corresponds to what he expected.


##### General design

Method `translate()` of base class `MDtoHTML` is overwritten in the inheriting 
class `GFMtoHTML`. Specificities of GitHub Flavored Markdown, thes that are 
augmenting the original Markdown specification, are implemented in method 
`translate()` aside the implementation of the other standard MD marks that are 
already available in the base class.



## 4. Related Scripts Usage

Two scripts, each related to one of the two classes discussed above, are 
provided to ease the translation of MD files into HTML.


#### 4.1 Markdown to HTML Script

Module `scripts/md_to_html_script.py` runs the translation of "standard" MD 
text in HTML5 text. This is not the one we use for feeding our site 
www.typee.ovh but this script could be useful for any project using MD text 
files to be translated in HTML5.

(_options have to be described for command line_)


#### 4.2 GitHub Flavored Markdown (_GFM_) to HTML Script

Module `scripts/gfm_to_html_script.py` runs the translation of GitHub Flavored 
Markdown text in HTML5 text. This is the one we use for feeding our site 
www.typee.ovh.

(_options have to be described for command line_)



[standard MD syntax]: https://daringfireball.net/projects/markdown/syntax
[GFM syntax]: https://github.github.com/gfm


## Annex - This document revisions history

| Date  | Rev.  | Author(s)  | Comments  |
|---|---|---|---|
| 2018-08-21 | 0.0.1 | Schmouk | Creation. |
| 2018-08-22 | 0.0.2 | Kerm | Added utility classes for MD tags, see module `scripts/utils/md_mark.py` |
| 2018-08-23 | 0.0.3 | Schmouk | Modified global design; Modified structure of this document; Added class for defining list of MD marks and their operations; Added classes for the description of MD marks and their location within MD texts. |
|  |  |  |  |
