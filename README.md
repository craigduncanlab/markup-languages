# Styled Markup Language (SML) and Plain Markup Language (PML) Specifications

(c) 29 January 2020 Craig Duncan
Updated 15 May 2020.

# Introduction

This document contains a definition for the two markup languages I have created (and which are still in development).  

The languages are:

 - Plain Markup Language (PML)
 - Styled Markup Language (SML)
 
Presently, PML and SML are useful when chained together in a sequence to translate PML text files into .docx files.

In brief, you can write simple documents in the 'PML' text format (example here) and the output appears as .docx files.  There is an intermediate markup format used called Styled Markup Language (SML) which is used internally, but the user doesn't have to write anything in SML if they do not want to.

I have provided a simple example of my implementation in python, used within the Visual Studio Code text editor in [this note](/Demo/HowTo_PMLparser.md)

# Language and design considerations

Markup-language formats like OOXML are needed to make or store Word (.docx) files.  However, translating directly from plain text to complicated style formats like OOXML, is difficult.   There are too many features within OOXML that assume it will be used with a particular software application that uses the same direct relationship between what is represented on screen or printer, and the data containers used to store the information for that output.  The main goal is to create output to screen or printer that looks like a paper document.   If we cannot introduce abstract intermediate transformation functions, then we cannot achieve the benefits of generalisation of functions.

We don't want this:

```
Complex markup scheme (OOXML) ---> .docx
```

And we don't want this either:

```
Complex programming language---> Complex markup scheme (OOXML) ---> .docx
```

Programming languages and development environments intended to work with OOXML (e.g. C#, .NET) often force the programmer/user to adopt a very low-level, bottom-up approach to embedding text within OOXML tags.  The programmer must accept the unnatural divisions of the text (i.e. the data objects occur where there are line breaks, regardless of the content or type of text).  However, the real problem with this is that it effectively bypasses the main goal of the Word-processor application (which was to leverage key-strokes, hide complexity, and make it seem like key-strokes were being turned into styled text immediately).   

The very concept of programming the data structures that are used for this key-to-screen process removes the fundamental labour-saving assumption on which the Word-processing program was built.   It is like requiring the farmer to spend time building the tractor in order to plough the field.   The end-user of a word processing program is supposed to start with the assumption that it is going to transform their manual typing, and manually-entered style commands, into rendered, styled text.   The complexity needed by the {bloated software application} to do this is supposed to be hidden.

On the other hand, if our goal is to create a smarter software program, that enables the user to avoid having to do as much manual typing and/or styling, then we want to have even less coding of the OOXML tags.  We want something more like this:

```
Detect features of natural writing (1) ---> Very Simple Markup (2) ---> Automated line-by-line markup (SML) (3) ---> OOXML --> docx (4)
```

The advantage of using several steps is that we can chain the abstractions together, and generate a multiplied saving of labour at each step.  A chained set of parsers acts like a chained set of mathematical functions.

The focus of Word Processors on OOXML also creates an unnecessary attachment, or dependency on a line-by-line analysis of documents (and the other, inconvenient convention that a 'paragraph' in OOXML is a container for data, whether it is a sentence, paragraph or some other type of language structure).

1.  Natural writing uses grammar.  There is structure there, but if computer programmers ignore it, they make up new and less appropriate data containers for the same information.

2.  The very simple markup is PML.   It is a top-down approach, to determine what kind of document we have, and what kind of markup is needed (independently of individual 'lines' of text).

3. The main purpose of SML is to provide brief, line-by-line style codes that a computer can translate into more complicated style formats, like OOXML, which is needed to make Word (.docx) files.  SML performs a similar function to the 'Markdown' that was used to help prepare HTML documents.  

4. Translating from OOXML to docx requires packaging a new OOXML inside a zipped container.  This can be done the hard way (with a complete build of .docx) or the easy way - just update your relevant .xml document and rezip the file.

All of these steps represent a 'top-down' approach to markup translation.   The markup languages are just a means of capturing information at various intermediate stages, so that we can achieve a satisfactory approximation as we go (we give up complete accuracy in favour of efficiency: we move from generality to specificity of the application of styles).

It is the transformation from these intermediate 'states' of a document to the next (from 1 to 2, or 2 to 3 above) that involves the need for clever algorithms, and produces the actual labour saving.  That is, the purpose of translating from PML to SML first requires rules or algorithms to make the task of inserting markup easier for writers, so that they don't even have to code in a line-by-line scheme like SML.  Used together, these markup languages can be used, for example, in a chained sequence to translate simple text documents into rendered and styled output (for example in a .docx file).  My implementation uses domain knowledge and some clever rules to analyse the PML text to produce as much useful SML as possible without requiring the user to do it manually.  

If this system works, then you only need to type (or translate from recorded voice to the document using speech recognition).  The structure and presentation can be introduced by applying rules to the various parts of the type of document you are writing.

# How it works

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

The aim of this markup language is minimalist, to avoid the need for markup except where it can assist with automated application of styles and rendering of new documents.

Consistent with this aim, the present definition of PML avoids the need for marking up plain text except for:
 - basic metadata related to the type of document  - to assist with automated SML generation.
 - notes; 
 - punctuation like semicolons to encode tabulation (e.g. vertical expansion of long legal sentences); and
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
