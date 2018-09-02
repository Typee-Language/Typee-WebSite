This is a regular paragraph.

<table>
    <tr>
        <td>Foo</td>
    </tr>
</table>

This is another regular paragraph.

---------------------------
&copy;

AT&T

4 < 5

\< \&

------------------------------

This is a first paragraph - This is a first paragraph - This is a first paragraph -
This is a first paragraph - This is a first paragraph - This is a first paragraph -
This is a first paragraph - This is a first paragraph - This is a first paragraph -
with no brealines.

This is a second paragraph -  
This is a second paragraph -  
This is a second paragraph -  
with breaklines.

-----------------------
This is an H1
=============

This is an H2
-------------

# This is an H1

## This is an H2

### This is an H3 ######

###### This is an H6

--------------------------

> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
> 
> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
> id sem consectetuer libero luctus adipiscing.



> This is the first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.


> ## This is a header.
> 
> 1.   This is the first list item.
> 2.   This is the second list item.
> 
> Here's some example code:
> 
>     return shell_exec("echo $input | $markdown_script");

---

*   Red
*   Green
*   Blue

+   Red
+   Green
+   Blue

-   Red
-   Green
-   Blue

1.  Bird
2.  McHale
3.  Parish

1.  Bird
1.  McHale
1.  Parish

3. Bird
1. McHale
8. Parish


*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.


*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
Suspendisse id sem consectetuer libero luctus adipiscing.


*   Bird
*   Magic


*   Bird

*   Magic


1.  This is a list item with two paragraphs. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit. Aliquam hendrerit
    mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
    sit amet velit.

2.  Suspendisse id sem consectetuer libero luctus adipiscing.



It looks nice if you indent every line of the subsequent paragraphs, but here again, Markdown will allow you to be lazy:

*   This is a list item with two paragraphs.

    This is the second paragraph in the list item. You're
only required to indent the first line. Lorem ipsum dolor
sit amet, consectetuer adipiscing elit.

*   Another item in the same list.


To put a blockquote within a list item, the blockquote’s > delimiters need to be indented:

*   A list item with a blockquote:

    > This is a blockquote
    > inside a list item.

To put a code block within a list item, the code block needs to be indented twice — 8 spaces or two tabs:

*   A list item with a code block:

        <code goes here>

It’s worth noting that it’s possible to trigger an ordered list by accident, by writing something like this:

1986. What a great season.

In other words, a number-period-space sequence at the beginning of a line. To avoid this, you can backslash-escape the period:

1986\. What a great season.


----------------------------------------------------

This is a normal paragraph:

    This is a code block.


Here is an example of AppleScript:

    tell application "Foo"
        beep
    end tell


------------------

Within a code block, ampersands (&) and angle brackets (< and >) are automatically converted into HTML entities. This makes it very easy to include example HTML source code using Markdown — just paste it and indent it, and Markdown will handle the hassle of encoding the ampersands and angle brackets. For example, this:

    <div class="footer">
        &copy; 2004 Foo Corporation
    </div>

will turn into:

<pre><code>&lt;div class="footer"&gt;
    &amp;copy; 2004 Foo Corporation
&lt;/div&gt;
</code></pre>



* * *

***

*****

- - -

---------------------------------------



This is [an example](http://example.com/ "Title") inline link.

[This link](http://example.net/) has no title attribute.

See my [About](/about/) page for details.   

This is [an example][id] reference-style link.

This is [an example] [id] reference-style link.

[id]: http://example.com/  "Optional Title Here"


[foo]: http://example.com/  "Optional Title Here"  
[foo]: http://example.com/  'Optional Title Here'  
[foo]: http://example.com/  (Optional Title Here)

[id]: <http://example.com/>  "Optional Title Here"

[id]: http://example.com/longish/path/to/resource/here
    "Optional Title Here"


[link text][a]
[link text][A]


[Google][]

[Google]: http://google.com/


Visit [Daring Fireball][] for more information.

[Daring Fireball]: http://daringfireball.net/

I get 10 times more traffic from [Google] [1] than from
[Yahoo] [2] or [MSN] [3].

  [1]: http://google.com/        "Google"
  [2]: http://search.yahoo.com/  "Yahoo Search"
  [3]: http://search.msn.com/    "MSN Search"

Using the implicit link name shortcut, you could instead write:

I get 10 times more traffic from [Google][] than from
[Yahoo][] or [MSN][].

  [google]: http://google.com/        "Google"
  [yahoo]:  http://search.yahoo.com/  "Yahoo Search"
  [msn]:    http://search.msn.com/    "MSN Search"

For comparison, here is the same paragraph written using Markdown’s inline link style:

I get 10 times more traffic from [Google](http://google.com/ "Google")
than from [Yahoo](http://search.yahoo.com/ "Yahoo Search") or
[MSN](http://search.msn.com/ "MSN Search").


*single asterisks*

_single underscores_

**double asterisks**

__double underscores__

un*frigging*believable

**_strong/emph_**

*__emph/strong__*

 * 
 _ 

\*this text is surrounded by literal asterisks\*

Use the `printf()` function.

``There is a literal backtick (`) here.``

A single backtick in a code span: `` ` ``

A backtick-delimited string in a code span: `` `foo` ``

Please don't use any `<blink>` tags.

`&#8212;` is the decimal-encoded equivalent of `&mdash;`.

--------------------------

![Alt text](/path/to/img.jpg)

![Alt text](/path/to/img.jpg "Optional title")

![Alt text][id]

[id]: url/to/image  "Optional title attribute"


------------------

<http://example.com/>

<address@example.com>

--------------------------

\*literal asterisks\*

\\   backslash
\`   backtick
\*   asterisk
\_   underscore
\{\}  curly braces
\[\]  square brackets
\(\)  parentheses
\#   hash mark
\+   plus sign
\-   minus sign (hyphen)
\.   dot
\!   exclamation mark

-------------------------------
