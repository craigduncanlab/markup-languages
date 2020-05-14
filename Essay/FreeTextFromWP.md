# Free Text From WP
a.k.a More thoughts on legal document data structures - what is feasible
Craig Duncan
23.1.2020

Some of the aims of the work so far are:
To free text data from the word processor, in that simple text can be stored without complication of specific layout and styles.  i.e. so that data structures associated with styles, numbering and rendering are not the primary means of tagging the document.

This is really at odds with, and independent of the goals of OpenOfficeXML - the primary purpose of OOXML is the opposite to tagging data structures.  The reference to styles,numbering and layout of text fragments is the primary system of tagging.  All other possible ways of classifying or dealing with the content are excluded by the focus on presentation.  It assumes that data structures will become apparent by the way tha text is sequenced, styled and numbered.  It assumes that data structures are interpreted through human visual processing.

This raises the question of how we can tag or markup any document for both semantic and stylistic purposes, whilst retaining as much of the original content as possible.

The semantic web investigates this.  Alternatives to HTML (such as 'markdown') are still primarily focussed on presentation, rather than semantics.  The computer acts as a library for documents (and therefore, independent document management systems are needed).   Each document acts as a container, and the user is less concerned with using the computer to work on internals (i.e. metadata is manually associated with each document, but it's not actually metadata in the same data space as the contents.  e.g. a 'lease' might be characterised by metadata in the independent document management system, not the metadata of the document).  One advantage of having metadata inside a document is that it remains there independent of the programs and programming languages that might be used with it.

## Observations on HotDocs (or how to understand it by creating programs that do the same thing, but open source, in an efficient manner)

HotDocs recognises that for logical manipulation of text, and making text choices based on data inputs, you need data structures (and logic, so variables and conditions need to be available).  The text contents must have flags to display them depending on the input.

HotDocs tries to retain all of the internal data structure of Word (in which style, layour is priority), and then introduces an explicit system of logic that is the only tagging and programming language visible to the user.   The result is that instead of a program with variables, you have a program that processes a document as a stream, with some tags being visible or not depending on the value of state variables that are maintained for processing.    It doesn't look like ordinary code - it is much more similar to HTML with javascript function enabled.   However, HotDocs is operating inside a domain-specific application, a very large application designed to handle rendering of text. 

The HotDocs assumptions are the same as Word: that each document exists as a separate container, and there are no data structures that can operate across multiple documents.  To deal with optional text, we are not able to swap large sections in or out from different documents, but merely to introduce some conditional tags inside a single document.

HotDocs retains the large docx files etc because it accepts the OpenOfficeXML (or rtf equivalent) annotation of documents, and those large file sizes, as unavoidable.   It then introduces domain specific markup and logical language, written in the same Word processor application, to deal with the contents.   Every HotDocs template is a mixture of a Word document, and elements of what looks very much like HTML and javascript.  

This language and the environment in which the text data sits, are unavoidable dependencies for the information that is stored in the system - it simply isn't easy to port that logic or text independently to a different system.  It is a domain-specific solution.  

More generic solutions would use data formats accessible to different operating systems, applications and programming languages.   Versions of HotDocs to 2017 had no ability to use independent data structures for text data because the whole point of the program was to insert conditional tagging (disguised as conditional programming language), within an existing Word document: it defined regions of tagged stylistic data (wrapper around application-specific text). 

To accomplish this, the HotDocs program must read and interpret the OOXML format (or whatever internal spec or XML format exists), looking for superficial-level tagging, to define text boundaries.  This is necessary because Word itself does not allow such data-centric tagging to occur.  Word is against tagging - the purpose of the software is for the text to appear unannotated, in keeping with its WYSIWYG philosophy.  

A program that can render docx must also be able to display OOXML as equally as the original program.  HotDocs leverages Word to do this.  HotDocs is really a wrapper that will 'run' the superficial program.  It requires you to have HotDocs and Word installed for this purpose (i.e. not a simple program that will run outside, independently of the source: see prototype X)

## HotDocs part 2

Programs that have attempted to avoid the HTML plus javascript and give users the ability to write more natural content, and then let a master program assemble it, seem to move the area of complexity.  Programs like Jekyll (written in Ruby?), uses markdown processing and meta-data to render web pages.

## Data structures - the central conundrum - and a DNA of legal documents.

The initial goal of moving text out of the word processing environment, and automating either the use of annotation or the generation of OOXML to fit a word processor can be overcome.  This allows simpler storage of text, which can then have minimalist style, numbering and layouts applied.   The Word processor takes over the function of giving numbers, because they are seen as irrelevant to the data storage or content (unless authors make them a dependency, which is not advised).

This gives rise to the possibility of having simple text as the primary information being stored.   This does not overcome the fact that the Word Processors rely on text layout, punctuation and sequencing, and storage of content in a single file to act as a data container.  That is, they rely on the human visual system which works with traditional media.  Text editors allow some of this - the typing that occurs mimics the handwriting that used to occur, but which has now been replaced by repetitive use of a small symbol set (keys/keyboards). The use of repeated characters has made text searching much easier, because people have moved to encoding of writing to fit computers, from the outset.

The same shift to encode whole blocks of text is possible for word processing.  Instead of typing in paragraphs, we type in 'blocks' - a single key then renders the paragraph or idea we want.  This idea of 'block typing' takes symbolic representation to a new level, a more high-level, abstract one.

Such a system relies on allocating a particular, repeatable block of information to a key.  This assumes a static data structure, and the ability to set up the library in the first place.  It assumes we won't want to repeat everything.  However, consider this: if typing blocks of text can be reduced to key-strokes, then we can also 'process' key-strokes as a stored file or sequence.  In that way, we can encode a whole document as a sequence of our keys, and we can recall them as we need them.  We can then edit those key-strokes (letters or codes).

Settling on classes of documents and data structures might seem a complicated exercise, but the answer is really to avoid too much logical consideration, and assist the user to 'type' from a library of options, in a given context.   We simply load up the library we want, and start typing in blocks.  If you want options within a particular context, you allocate a key to them.  If you don't, you don't.  

In this way, we do not have to introduce so much logic, if we can just choose our blocks as an expression of purpose.  We call up a sequence like 'ABCDE', and if we want to replace clause E, with clause F, we type "ABCDF".   The fewer choices there are, the fewer block sequences we need to be concerned with.   In addition, the storage of two similar but different documents can be encoded in such a ridiculously short way that the 'compression' of what used to be completely separate Word documents will be in the order of 5 to 10000 less data.  Why?  Because you have isolated the information you need to instruct, by encoding, the sequence of events that leads to stylised output.

Now what happens if your library text, for a key-stroke, changes?  You can have split screen, or two-level access.  e.g. a bar like Excel can hold your block-strokes, and then the main editor can display the text blocks.  If you edit the blocks at the character level, it won't alter the key-strokes, but what you might have to do is resave the relevant library as a new library, to work with your key-strokes.  You could also update that specific key in the original library, for a more permanent change.

How is this different from 'Hot Keys'?  For a start, Word doesn't allow you to load up libraries of text blocks as 'libraries'.  Secondly, you'd always be working with the full text, and not the library encoding.   You wouldn't be seeing the structures.

What would this give us, in a pure text form?
1.  A library file for block-strokes.  Something that has "A" with text "B" with text etc.  It's up to you to ensure that your key-strokes are consistent between similar documents.  Maybe over time there will be a table of block-codes for topics (R=Rent, for example), and conventions.
2.  Files with the minimalist encoding.  The meta-data in the little files consists simply of: library file, date, author, then the keystrokes.  Possibly other things.
3.   The editor that allows you to view this in split screen.   before this is built, it will still be possible to set up your library file, your block file, and then run programs to convert block-codes to text, and then to process that into a Word document.

The last step (of converting text to styles) may be able to be achieved by automatic markdown application (e.g. assuming it is a legal document, numbered) or possibly by including some informatino in the library meta-data (e.g. letter, legal document etc).

Other options:
block keys represent high-level encoding of documents.  THey might choose to ignore whitespace.  e.g. a letter might be ABCDE, where A is the address, and E is the signing section.   We could have programs define what A is, drawing upon data (like for mail-merge), and then iterate through all of these.  The letter sequence is really just a high-level instruction for the block codes.

Block processing is really the high-level automation that might be sufficient for describing legal documents.   If people can define their library, and their letters, they can also define documents a little bit like a DNA code.  If nothing else, it provides a structured way to talk about the contents of documents like contracts.

## Number of codes needed

For some documents, will we need more than 26 'letters' to write the document?

Single letters are useful because we can 'type' on the keyboard and the contents of the library will appear.

For documents with greater numbers of clauses, then would a 2 or three letter code work?
e.g. RR for Rent Review, RE for rent.   If these become standardised so that the libraries work with codes drawn from a very large set, possibly larger than a single document, we might be able to 'read' the code and learn it without it being too subjective and individual.
e.g. GST might be the code for a GST clause.  Then all we have to do is specify the library we are using for that code.  But if our libraries are document specific, we get into trouble.

How do we specify both the code for the type of clause, and the library?
A single library for each family of documents would be helpful, but won't there be other situations where a few clauses from more general libraries are needed?  Do we need to associate some codes with the local library and some codes with the general?  could we indicate this with some codes being only general e.g. ZGS = GST from general library, ZBP = boilerplate from general library?

Then the 'Z' library acts as the general repository, and the rest of the document uses the local library?

Possible format:

abc ABC RRR RRR ZBG ZBG

where first three letters are code for the library.   Z codes are codes for general library clauses

Ability to encode a document this way relies on:
agreed codes within each library
library that has codes and text
ability to automate the 'markdown' process.  i.e. use conventions to markdown the contents to save users. users should not do plain english sentence breakdowns at this point {could abort at this point}
use conventions for converting markdown to docx styles (single template)
as part of this the process of expanding 'tabulated sentences' as part of plain english conventions involves both fragmenting a sentence into docx 'paragraphs', then applying sub-style to those.

# Encoding and encoded transmissions; sharing; server storage.

The use of shared libraries enables communication of a document simply by way of codes (as above):

abc ABC RRR RRR ZBG ZBG

This enables purely text files to be rendered into docx.  The information has been summarised in such a way it is difficult for intermediary to know; yet it allows flexibility and precision in the information being referred to.   A person discovering the general table of contents for codes would still not know the contents of the specific library (although Z codes could be determined by past knowledge)

System works with a combination of :
- encoded documents, libraries
- expansion of codes to text, text to markdown, markdown to docx

The 'expansion' process is a useful summary of what is currently, often, a manual process of writing within a word processor, and also storing information with markup primarily designed for layout, when in fact, it does not allow compression of ideas or content.

The compression factor of a message like the one above (to store the 'contents'), compared to its equivalent word document, is probably in the 100's of thousands.

Individual users might only have to deal in codes, allowing central storage to be smaller.

Also note the possibility of sending a code to a server, having a docx sent back.  Very small outward transmission needed.

# Library file metadata

If the library files contain all the codes and text blocks, they might also contain for some of the common blocks, the 'key' that can be used for block-typing.  i.e. this is like a convenient config for people who just want to type and get the clause, but it will also cross-reference the general 3-letter code.  The program could read the library and report this table to console or screen for reference (like 'help').

# Implementation

How much could be written in C?  Allows compilation and execution on different platforms.  Keep it very generic and simple.


# Simplification of logic

Is it easier to just say:

	If we get data so that x=true, y=true etc use LegalDNA string 1 else LegalDNA string 2.

cf HotDocs.   All the logic is trying to make variations on one LegalDNA string, depending on the data.   Why?  because it cannot refer to the whole of the document, or an alternative document, in a simple and summarised way.   If you do not have the capacity to simplify, your grammar is inappropriate for the task, and you end up using a complex grammar to achieve the same think.  You start referring to which parts of a document are on or off, without having a map of the finished alternatives.   People start to analyse documents with reference only to the bits that vary (this is like DNA scientists who study only genetic variation).  

HotDocs cannot alter or rearrange text sequences (clauses and sequences of clauses) easily, or switch out all of the content of each block.  For HotDocs, there is only ever the possibility of discussing/reasoning about the contents of long-hand text blocks, and those are the blocks which might seem to change depending on the input.   HotDocs never offers the opportunity to create libraries of block sequences that simply exist as a saved sequence (there would be no need for HotDoc code, and you'd just have a plain Word document).  i.e. HotDoc specialises in 'variation making', and logic insertion, rather than efficient information representation for re-use.  

Word never really enables us to define a 'document', for some relevant purposes, as a string of encoded blocks of text.  Such encoding, in the LegalDNA strings, allows us to work with information at both the document level, as well as variations to the order or sequence of blocks, or the text within blocks.  We can also choose to adopt different libraries, or schemes, which allow for stylistic differences and the ability to write the same LegalDNA sequence using different contents for each of the codons[blocks].

HotDocs accepts Word as the platform for the information representation, then offers the ability to introduce logic into that environment.  It is working in an environment for which the primary encoding of data is the layout of text in a stream of characters, divided into paragraphs.  Word has no concern with higher-level encoding.  As such, it encourages its use for precedent templates where some variation to text is needed, by defining logic for 'in-place' variations to that text.   It is the equivalent of hacking the contents of an existing document (without addressing the fundamental omission of an information encoding scheme).  The more hacking and logic that is required, the more the absence of an ability to encode an unvaried document becomes obvious, and difficult.

For simple insertion of client-specific data, the idea of mail-merge and HotDocs go together easily enough (i.e the new data is the variation to the 'layout' data), but as a way of storing precedents it offers no advantages, and in general, no higher level of abstraction about information than offered by Word.

What Word (and therefore HotDocs) lacks is an opportunity for symbolic representation of the entire contents of the document.
