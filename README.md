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

Markup-language formats like OOXML are needed to make Word (.docx) files.  However, translating directly from plain text to complicated style formats like OOXML, is difficult.   There are too many features within OOXML that are related to the application that uses the OOXML, and there is significant bias toward using the OOXML as a very precise specification to ensure that it can output something to screen or printer that looks like a paper document.  

Programming languages and development environments intended to work with OOXML (e.g. C#, .NET) often force the programmer/user to adopt a very low-level, bottom-up approach to tagging text so that it resembles the desired output.  The computer languages, and the tagging, represents very little benefit to users if it is concerned with low-level encoding of how the text should *look*.   The need to tag the text with a complex annotation scheme, like OOXML, to describe how it should look, even with the benefit of computer code, is contrary to the original design goals of the Word Processing application anyway.  It is simply not a smart solution to replace the labour-saving goals of the Word Processor with a new form of laborious coding and complex annotation.

This problem of having to insert complex annotation to get the look of the document right in a WP application can be solved by using an intermediate style format, like SML.  The main purpose of SML is to provide brief style codes that a computer can translate into more complicated style formats, like OOXML, which is needed to make Word (.docx) files.  SML performs a similar function to the 'Markdown' that was used to help prepare HTML documents.  This kind of markdown has a bias toward translating simple line-by-line style codes or tags into a more complex markup language.  The labiour saving is not so much in how many lines have to be processed, but in how much initial annotation has to be done for a serialised flow of text. 

However, SML is still mainly focussed on labour-saving in relation to style and presentation.  I do not think it permits labour-saving that is based on what the information is.   My goal is to avoid line-by-line annotation and, if possible, to adopt a semantic or content-based data structure that allows some of the line-by-line style codes (even the brief ones) to be themselves inserted by computer automation.  

We can reduce the need for repetitive style codes (or repeated cycles of style codes) by recognising that much of what we write, and how we want to present it, is influenced by context-specific conventions.   By using simple markers to indicate *what* we are doing, we can reduce the burden of inserting style-based markup at all, or we may be able to achieve a higher level of automation of simpler markup schemes.

The reduction of complexity is achieved by introducing a new preliminary step that allows codification of the purpose or context of a document into style schemes, which in turn allow line-by-line style codes to be applied to regions of text, not just individual lines in isolation.   By chaining together more abstract coding schemes with the line-by-line markup schemes, and finally, the markup to OOXML translation, we can achieve a higher degree of abstraction.   The greater the abstraction, the more the computer can relieve the burden of doing the work.  

This is a 'top-down' approach to markup translation.  That is, the purpose of translating from PML to SML first is to allow some automated algorithms to make the task of inserting markup easier for writers, so that they don't even have to code in a line-by-line scheme like SML.  Used together, these markup languages can be used, for example, in a chained sequence to translate simple text documents into rendered and styled output (for example in a .docx file).  My implementation uses domain knowledge and some clever rules to analyse the PML text to produce as much useful SML as possible without requiring the user to do it manually.  

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
 - notes; 
 - punctuation like semicolons to encode tabulation (e.g. vertical expansion of long legal sentences);
 - defining where new documents begin; and
 - basic metadata related to the type of document  - to assist with automated SML generation.

## Notes

One of the aims of PML is to give easy control over the inclusion of comments(notes) that will pass through to SML.  

## Document divisions

The document division '-n-' is currently the same in PML as SML, but it could be changed if the PML to SML translator makes an appropriate substitution.

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

If our goal is human information processing, and not just text presentation, then we want to ensure that the data structures we used to store and analyse data have more in common with our intended purpose than conventional formats like OOXML do.  PML retains the grammatical convention for sentences, because we can use normal grammatical rules to identify the original sentence, and use the full stop and line breaks as grammatically-inspired markers for text divisions.  The subdivision of a sentence into presentation-specific data types, or transformation into vertical items, is handled further downstream.  

The reason we have to be explicit about this is that the way in which Word Processors, and formats like OOXML store data, has been uncritically accepted as being correct, for the limited purpose of the visual presentation of information.

Efforts at 'clearer' legal drafting are not always focussed on the distinction between making something easier for the human visual system, and whether there is attention to the data structures actually used to store the data in a word processing application.  When people write in long sentences (as lawyers often do), they might choose to adopt work-arounds to make it easier to read the sentence, and this includes how the sentence is visually presented.  In particular, one legal drafting process (known as 'tabulation') rewrites some long sentences into vertical lists, with a new line for different items, even if they are in the same sentence. Some legal writers routinely adopt this approach, skipping the transformation step altogether.  Readers can see the sentence, and are not concerned with how it might be stored in a computer.

These visual work-arounds to long sentences have their draw-backs for analysing the text of sentences stored in Word Processor files.  The reason is that that Word Processor applications do not adopt common grammatical conventions for the way they store text data.  A WP file resembles more a database of blocks of text separated by line breaks. It is not actually a database of sentences, or even sentences on particular topics. Most legal drafters probably do not realise that their efforts to create a more pleasing visual representation of their sentences, by inserting more line breaks, create the potential for even more inconsistency between the grammatical conventions of language, and how that data is stored by a Word Processing application.

The primary concern of Word Processor designers has been how text looks, and so they have been less concerned with functions that require grammatical conventions to be retained, and used.  The Word Processor application may store each new line in something that the data format (e.g. OOXML) happens to calls a 'paragraph', but which has little to do with the normal grammatical meaning of a 'paragraph'.  In OOXML, a list-style sentence that occupies 8 lines may be stored in, say, 8 component parts or 'paragraphs'.  If you scan the file for 'paragraphs', what you get then are bits of a sentence, all looking like they are separate ideas when they are really part of one single sentence.  

The definitions of 'sentences' and 'paragraphs' in our language seems like a basic, fundamental condition for working with text and the meaning of text.   We know that sentences are the basic units of expression for information, and sentences form part of paragraphs.  The normal conventions of language, which of course are intended to perform a function: *to help us gather and interpret meaning*.  For this reason, it makes sense to give greater priority to these grammatical conventions for our upstream data processing than has been the case with presentation-focussed developments like markup schemes and OOXML files.

## Metadata (categories of document)

The instruction 'meta:' can be used to specify the style outline schemes to be used for PML to SML translation schemes.

For example, 

	meta:legaldoc
	meta:letter
	meta:defaultdoc
	meta:memo

Each of these will specify the specific hashcodes to be used in place of the 'default' styles detected by the program.

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
