# A multi-stage approach to 'just-in-time' creation of .docx content from simple text

(c) 29 January 2020 Craig Duncan
Updated 15 May 2020.

# Introduction

This document describes a way in which raw text file data can be stored in very small text files, with minimal annotation, and yet can be used as the input for a computational process that can render, automatically, one or more styled .docx documents.

This document also contains a specification for the two utility markup languages I have created (and which are still in development).  These can be used as markup formats by themselves, but I have used them as intermediate data-storage formats in an automated workflow, one that can translate raw text files into .docx file(s).  The languages are:

 - Plain Markup Language (PML)
 - Styled Markup Language (SML)
 
That is, PML and SML are useful when chained together in a sequence to translate PML text files into .docx files.

In brief, you can write simple documents in the 'PML' text format (example) and the output appears as .docx files.  A person wanting to translate raw text to .docx may not have to write anything in SML if they do not want to.

I have provided a simple example of my implementation of this workflow in python, used within the Visual Studio Code text editor in [this note](/Demo/HowTo_PMLparser.md)

# Language and design considerations : insufficiency of OOXML

The assumption in Word-processing programs that use OOXML is that the program will perform invisible edits on OOXML content and the user will only see, on the screen or printer, what looks like a paper document.  The relationship to OOXML, hidden from the user, is complex: OOXML wraps around the text, and is then embedded within a .docx package.  Some text is fragmented within the OOXML tags, so that there is no guarantee that our normal understanding of sentences or paragraphs, in a grammatical sense, is reflected in the consistent storage of those parts of text in OOXML.  

We are sometimes told that markup-language formats like OOXML are the primary data structure needed to make, store or write programs for Word (.docx) files.  This is basically bad advice, if you are interested in creating a new paradigm for interacting with textual data, outside the assumptions of the software applications themselves.  

OOXML has a high mutual dependency with the software applications that use it.  It evolved with them, not independently of them.  Within OOXML is the fundamental assumption that the main data containers in a document are the text blocks formed by every line-break intended to be visible in a graphical user interface.   At its foundation, OOXML uses the 'Enter' or 'Return' key as the manual delimiter for text documents, and OOXML is intended to capture this delimiter by creating a new object block (which it calls a 'paragraph') whenever it occurs.  The same approach is used to split OOXML text fragments, by creating a new fragment every time new text is inserted somewhere between existing text characters.

Within software applications using OOXML, OOXML is mainly intended to be hidden from users, buried within the complex, object-orientated software designed primarily to produce a visual rendering of text in response to user-input through a manual typewriter interface.  These programs perform a high-level of automated maintenance of the style information in the OOXML data file, on the assumption it is being updated whilst the user painstakingly updates the document manually. 

A consequence of the environment in which OOXML developed is that translating directly from plain writing (text files) to tagged, style-based information, like OOXML requires, is difficult.  We run into the problem that OOXML is not flexible in how it stores data: it is tightly, rigidly bound to its origins as a data structure for typewriter-inspired ('Enter-key' based) software.  To overcome this creates a high programming overhead, and exposes the lack of easy access to the raw text itself.

The same factors also suggest that we should not turn to using object-orientated languages that closely reflect OOXML in order to prepare customised programs for text documents.  We do not want to have to deal with OOXML format, and its data divisions, *every time* we want to work with a text document, of any kind (whether for storage on disk, or for in-memory calculations).  Rather, we should be inventing new, flexible data formats and programs that avoid the need for OOXML altogether, or can interface with OOXML later without too much difficulty.  If we want to  introduce new 'intelligent' text data formats that are independent of OOXML, we must define them, and also  create programs that can still translate automatically from those formats to OOXML, as and when required.   We must also explore the extent to which we need text formats based on completely different assumptions to OOXML, and the reasons why.

We don't want this:

```
Complex markup scheme (OOXML) ---> .docx
```

And we don't want this either:

```
Complex programming language+'pro forma' text---> Complex markup scheme (OOXML) ---> .docx
```

## Solutions (new data formats and functions upstream of OOXML)

So what is the solution? Ans: a much leaner representation of the text, and programs that enable translation of the text data or your document(s) to OOXML (and then to .docx) as and when needed.  We want something more like this:

```
Software to detect features of your natural writing (1) ---> 
Very Simple Markup (PML) (2) ---> 
Automated line-by-line markup (SML) (3) ---> 
OOXML (4) --> 
.docx (5)
```

The advantage of using several steps is that we can chain the abstractions together, and generate a multiplied saving of labour (and file storage required) at each step.  A chained set of text parser programs acts like a chained set of mathematical functions.

It is a top-down approach, and we are even free to introduce an interpretation stage, in which raw plain text is interpreted to give it an initial structure based on its context or category of document.  We might choose a very different data structure for our text representation at the start to what is needed at the end.  However, since OOXML is very much based on a line-by-line approach to storing data in 'paragraphs', we may need a specific stage which takes whatever data we have, and converts it into a line-by-line representation, just before translating into OOXML.

Here is a short statement about numbers (1) to (4) above.

1.  Natural writing uses grammar, but it can also be stored as simple unadorned text, in a very small file.  There is structure there, but if computer programmers ignore it, they make up new and less appropriate data containers for the same information.

2.  The first very simple markup scheme that distinguishes a completely plain text document from one that we want to translate into a styled form is PML.   

3. The main purpose of SML is to provide brief, line-by-line style codes that a computer can translate into more complicated style formats, like OOXML, which is needed to make Word (.docx) files.  SML performs a similar function to the 'Markdown' that was used to help prepare HTML documents.  

4. Translating from OOXML to docx requires packaging a new OOXML inside a zipped container.  This can be done the hard way (with a complete build of .docx) or the easy way - just update your relevant .xml document and rezip the file.

All of these steps represent a 'top-down' approach to markup translation.   The markup languages are just a means of capturing information at various intermediate stages, so that we can achieve a satisfactory approximation as we go (we give up complete accuracy in favour of efficiency: we move from generality to specificity of the application of styles).

It is the transformation from these intermediate 'states' of a document to the next (from 1 to 2, or 2 to 3 above) that involves the need for clever algorithms, and produces the actual labour saving.  That is, the purpose of translating from PML to SML first requires rules or algorithms to make the task of inserting markup easier for writers, so that they don't even have to code in a line-by-line scheme like SML.  Used together, these markup languages can be used, for example, in a chained sequence to translate simple text documents into rendered and styled output (for example in a .docx file).  My implementation uses domain knowledge and some clever rules to analyse the PML text to produce as much useful SML as possible without requiring the user to do it manually.  

If this system works, then you only need to type (or translate from recorded voice to the document using speech recognition).  The structure and presentation can be introduced by applying rules to the various parts of the type of document you are writing.

# How the new data formats work

The starting point, or input, is a 'plain markdown' file, which is basically a text document with a few PML additions.  The output is a .docx document (or more than one).

At present, the proposed workflow and my python implementation consists of two main translation programs:

- Conversion of .pml text files to .sml text ; using pml2sml
- Conversion of .sml text to OOXML and ultimately to .docx : using sml2docx.py

The staging of markup language processing helps achieves the broad aims of reducing markup burden on the writer.  The technical goals of such staged text translation are:

-  to bridge the inconvenient gap between simple markup and more complex object-orientated, serialised markup languages like OOXML (it does this with another human-readable markup scheme in the middle of the workflow); and
- to introduce additional markup language features such as document splitting and easy toggle of comments/notes content.

The last features (such as tighter control over notes) are enabled by the markup definitions, but it also requires the translation program to accept override instructions about whether notes should appear in the output or not.

SML is a markup language that specifies the styles for output, in a precise line-by-line fashion (suitable for .OOXML and .docx).  

Both PML and SML are markup languages, and each inserts more information into the output file, based on internal rules.   The SML output is more detailed than the SML input.  The PML output is the input to the SML.  

Some information needs to pass through every stage unaltered, such as the insertion of page or document breaks.  Also, user-level instructions like whether notes mode is 'on' need to pass through all stages.  Both PML and SML can distinguish the notes parts of the text, so that the initial PML to SML translator can be set to turn the notes on or off for the purpose of the finished .docx document.

PML/SML can insert document breaks - allowing you to produce more than one .docx file from a single PML script file.   In SML, normal page breaks can also be inserted with a different code (#PB).

Automated SML generation requires the translator to use algorithms and analysis of the PML text to produce more detailed markup encoding than exists in the starting PML input.  

# Plain Markup Language (PML) - design

The aim of this markup language is to avoid the need for markup except where it can assist with automated application of styles and rendering of new documents.  It is a minimalist approach.

Consistent with this aim, the present definition of PML avoids the need for marking up plain text except for:
 - basic metadata related to the type of document  - to assist with automated SML generation.
 - identification of notes; 
 - use of punctuation like semicolons for tabulation (e.g. vertical expansion of long legal sentences); and
 - defining where new documents begin.

## Metadata (categories of document)

The instruction 'meta:' can be used to specify the style outline schemes to be used for PML to SML translation schemes.

For example, 

	meta:legaldoc
	meta:letter
	meta:defaultdoc
	meta:memo

Each of these will specify the specific hashcodes to be used in place of the 'default' styles detected by the program.

## Notes

One of the aims of PML is to give easy control over the inclusion of comments(notes) that will pass through to SML.  

## Transformation of sentences into vertical lists

PML treats sentences as a single unbroken list of words, and doesn't expect you to set out lists as if they are a table.  That is, PML retains single sentences without line breaks, even if they include lists or sub-paragraphs that are intended to be represented differently in docx.   

The translation from this PML form to a presentation-based form with separate, styled lines  (more often used in the WP environment) is handled by the PML to SML translator. For example, the translator can convert a sentence that is written in PML as :

	This is a sentence that has lists, including: first item; second item; and third item.

into sml like this:

	This is a sentence that has lists, including:#IN

	first item;#H3

	second item; and#H3

	third item.#H3

which can ultimately appear in .docx as something like this:

	This is a sentence that has lists, including:

	(a) first item;

	(b) second item; and

	(c) third item;

The exact hashcode applied in SML will depend on the currently chosen 'theme' of the document.  The parser will turn these into separate paragraphs and attempt to locate the 'and' on the correct line.

## Why PML avoids the need to specify vertical lists in sentences

Word Processors, and formats like OOXML, store data in blocks that are called, misleadingly "paragraphs".  This is the label given to the data units within which software developers store the data, in OOXML, for an application that is primarily interested in visual appearance.  However, these paragraphs are based on detection of line-breaks, and do not represent the usual sentences and paragraphs in natural language (grammar).  In some professions, like law, inserting line breaks within sentences to create 'lists' within sentences ('tabulation') is supposed to be an example of plain English, or clearer writing, but it just exagerrates the problems of storing sentences in Word Processors.   Long sentences that are tabulated will then occupy several lines.  In the OOXML format, these are not longer kept in the same data container - they now appear in different blocks of data (the 'paragraphs' of OOXML).

If our goal is human information processing, and not just text presentation, then we want to ensure that the data structures we used to store and analyse data have more in common with our intended purpose than conventional formats like OOXML do.  PML retains the grammatical convention for sentences, because we can use normal grammatical rules to identify the original sentence, and ensure data containers more accurately reflect actual grammatically-based text divisions.  The subdivision of a sentence into presentation-specific data types, or transformation into vertical items, is handled further downstream.  

## Document divisions

The document division '-n-' is currently the same in PML as SML, but it could be changed if the PML to SML translator makes an appropriate substitution.

# Styled Markup Language (SML) - design

SML can be used as the basis for a simple translater to OOXML.  I have implemented one such translator in python in conjunction with a predefined .docx template, with the names of styles captured in the text for which the relevant style is applied.

For example, in the demonstration template document (StylesTemplate.docx), the only text in the document is text naming styles for use with SML, like:

	H1
	Indent1

and each of these lines has the relevant style applied to allow OOXML conventions to be sampled and used.

The penultimate markup language for conversion to OOXML (in this case, SML) must be organised as if each line is a paragraph, and each paragraph needs a style, to conform to OOXML assumptions.

## Defining new document breakpoints for distinct .docx files 

A feature of SML not found in most markup/markdown languages is the ability to divide the output of the single input file (whether chained .pml or .sml).

The insertion of document divisions by the ```-n-``` code is retained by PML to SML translation but then processed by SML to OOXML translators as a document division code.

The following codes should be at the beginning of a line.

- New documents use ```-n-```
- Document sections use ```---``` (legacy)

Every ```-n-``` line in an sml file will create a new docx file when processed.

The ```-n-``` code must be followed by the proposed filename (e.g. for .docx file output)

e.g. ```-n-NewFilename```

If no ```-n-``` line appears in the file the file will be output as 'Demo'

## SML hashcodes syntax

All hash tags appear at the *end* of a line or relevant paragraph, before the carriage return (line feed).

e.g.

	This is a heading level 1#H1

	This is a sentence. This is another sentence.#LN

	This is a note#N

	This will be indented #IN

	This will be indent level 2#Indent2

## Simple line-based hashcodes to use

The prepareParagraph function in sml2docx.py matches sml #codes to the template style names.  The default template .docx file is in LegalDocsTemplate.docx.

The following hashcodes used for .sml map to the Styles in LegalDocsTemplate.docx 
(see sml2docx.py prepareParagraph)

 | sml hashcode |	Equivalent StyleName | Description
 | :-------- | :-------------- | ------------|
 | LH | H1 | 
 | LHF			| Indent1 |
 | LC 			|   H2 | 
 | LCF			|  Indent1
 | LCFF		|  H3
 | H1 			|    H1 | A numbered, bold heading (level 1 heading)
 | H2 			|    H2 | A numbered, bold heading (level 2 heading)
 | H3 			|    H3 | A numbered, alphabetic heading (level 3 heading)
 | H4 			|    H4
 | H5 			|    H5
 | IN 			|  Indent1
 | Indent1	|	Indent1
 | Indent2	|	Indent2
 | Indent0	|	IndentNoSpace
 | GD			|  Indent1
 | LD 			|  Indent1
 | ST 			|  SUBTITLE
 | DT 			|  DocTitle
 | BC 			|  BoldCentred
 | CH 		  |	CentredHeading
 | Note 	  |	Note
 | None	  |	Note
 | NP 		  |	NumParas
 | NP2 	  |	NumParas2
 | NB 		  |	NumParasBold
 | B 		  |	BoldHeading
 | LDP0 	  |	LDP0
 | LDP1 	  |	LDP1
 | LDdate 	|	LDdate
 | LDB 	  |	LDB
 | LDBN 		| LDBN
 | LN 			|    LN
 | Sched1 	| SCHEDL1

```nb: The `Note` style in the LegalDocsTemplate.docx is highlighted and italicised.```

| SML hashcode | Breaks: |
| :------- | :--- |
| SB 		|	SectionBreak
| PB 		|	PageBreak
   
## SML's patterned hashcodes

The purpose of SML is to identify line by line styles, however it is often convenient to process a schema or pattern of different styles in a hierarchical way, to a given block of text, or a sequence of sentences.  This saves having to encode SML lines comprehensively.  In addition, this can, if convenient, be a feature taken into account by PML to SML translaters.

If there are multiple sentences in a paragraph, you can direct the parser to use a hashcode pattern within the paragraph by just placing one hashcode at the end  (see sml2docx.py function readRowsSpam)

If there are more than 3 sentences in the paragraph, the last hashcode pattern will repeat as often as necessary to complete the paragraph.  These are the patterned hashcodes currently implemented in sml2docx.py.


| Hashcode 		| SML hashcode pattern	|		Description
| ---------- | --------------- | ---------------------------------------
| BC 	|			["BC","BC","BC"]		|			All bold centred
| LH 	|			["LH","Indent1","H3"]	|			Heading 1, Indent para with (a)
| IP 	|			["Indent1","Indent1","Indent1"]	|	Indented paragraphs
| H3 	|			["H3","H3","H3"]		|			All H3 level
| LC 	|			["LC","LCF","LCFF"]	|				H2, Indent, H3 repeat
| BHP |			["B","NP","NP"]			|			Bold Heading with numbered paras (Witness st)
| PP 	|			["NP","NP","NP"]		|			All numbered paras
| PL 	|			["NP","NP2","NP2"]		|			Numbered paras with change of numbering
| LHC |			["LH","LC","LCF"]			|		H1,H2, Indent
| L2 	|			["H2","Indent1","H3","H3"]		|	H2 with an indent then (a) pattern

# Implementation of the PML to SML translation

PML to SML translator design is based on the premise that by knowing a specific document type, the conventions and writing patterns can be used to detect structure and automated the application of detailed, line-by-line style codes.  This helps to convert relatively plain text into SML.  It can also be described as an Automatic SML Assistant.

The translator is based on domain-specific knowledge and the quality of inferences that can be made by the algorithms that it uses.

The currently implemented plain english markup pre-processor is : pml2sml.py. 

## 'Plain English' long sentence expansion

The use of in-line colons and semicolons without line breaks in a PML file can be converted into separate separate SML lines (plain english style) by the PML to SML translation program.  This conversion to separate lines in SML enables each of the sentence fragments to be styled, ultimately, in a .docx output format. 

## Auto-detection of features for automated markup of styles

The PML to SML program attempts to convert sentences or paragraphs into SML hashcodes based on text features (e.g. automatic detection of headings levels 1 and 2)

The hashcodes it is looking to add can be generalised as :
	h1code,	h2code, notescode and level names (e.g. ["LDP1","H3","H4","H5"])

The classification system is based on the assumption that different types of documents (e.g. legal documents) are written with structural and grammatical patterns that can be automatically detected.

The way in which the document is processed depends on the currently selected 'theme' (triggered by encountering the 'meta:' code in the file being processed).  e.g. if the code 'meta:legaldoc' is encountered it will process the file using the set of abstract hashcodes defined for legal documents.

## Translation of comments to SML

The initial PML parser to SML, pml2sml.py, recognises simple notes or comments encoded by a '//' at the start of the line (like some programming languages).   These will be converted to an SML hashcode #N for the next stage of text processing.

e.g.

```// can be used to indicate a comments (notes) line (i.e. #N) will be inserted by pml2sml.py```
