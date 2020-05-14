Craig Duncan
23.1.2020

# Lessons from word processing - different encoding of spatial information

The attractiveness of word processors for people to use is that they emulate a traditional media, which was already popular because it used visual symbols and the represented relationships for those symbols were already spatial to some degree.  

The reason that information represented visually 'needs' to be converted to anything else is because we don't traditionally have computers interpret the meaning of spatial relations for text as the primary or even first method for identifying spatial regions (or containers) that have meaning.   

By omitting the end results of human effort to structure and space text, we never really enable computers to 'speak' in terms of this layout, or structure.  Instead, some meaning is reconstructed by searching, apparently naively, in other ways, using different communication channels.  If humans are, in fact, using multiple channels to represent information (or it is a single channel that can be reconstructed into different components), then by incorporating more of them we can have machines that use the more convenient channel or, alternatively, to confirm or corroborate meaning from one channel by another.

The difference between the storage of text as characters or as a merely a graphic 'image' has been traditionally thought of as completely different way of storing and using information.   In some ways they are.   They are the same information at a general level, and for some purposes, the differences mean very little.  

The representation of text through characters is linked to the sending of character sequences to the screen through a lean method: reading off a character code, looking it up in a fixed set set of stored characters, then producing a small image at the next place.  A single set of character definitions can be read off as needed; the output is a more consistent set of letters than handwriting would produce.  This method of encoding by keys and looking up a font set is less memory intensive than drawing an image, since the encoding can be done as numbers and a sequence. 

A Word Processor, which is closer to a character by character representation, handles the rendering in a different way to directly rendering key strokes to the screen, but it too ultimately produces something related to a character sequence that is being capable of being captured as an image on the screen.   

An image of the same sequence of letters, on the other hand, does not recognise the repeated letters as part of a data structure.   It repeats the entire image for display, pixel by pixel.  Humans can identify the similarity of the ultimate structure, even if the computer cannot.   To a human (looking at the letter on screen), this is the same information, with spatial similarity, even if it is rendered differently by the internal processes of the computer.  

Unlike traditional media, the grid-based rendering of characters on-screen by hitting keys already provided a degree of encoding and compression of information.  A keyboard does not require hands to shape letters: it replaces that with a tap; the simple pressing of a key (button) linked to a symbol.  Space is inserted by pressing the space bar, or by hitting enter or return (then the space is vertical; the next key is by convention, rendered below, and to the left, for most countries.)

If our source information can encode, concisely, the same information for rendering on screen, including spatial layout, as an image can, then it must contain similar encoding of not only the symbols, but the spacing too. Despite the fact that spaces or gaps (or the whitespace), or the punctuation or the words are rendered differently, it ultimately produces the same effect on screen.  Runs of spaces or words carry meaning because of their patterns, or density.  For example, five words on a page may mean nothing by itself, but when it appears above a paragraph of dense text, it may by its spatial location be more likely to represent a heading.  If it carries a number beside it, even more so.

Computer visualisation or machine learning of images might be taught, using the pixel image, to identify a 'letter' through a complicated process of identifying the layout of pixles (see ... Tors Seeman?).   Optical Character recognition is more focussed on identifying the individual letters, then converting those to character codes, so that they can be represented in text editors (with the simpler rendering process).

These observations suggest that when we have the possibility of dual systems of encoding, one of which is based on visual or spatial arrangement, we might be able to look at the process in reverse, That is, we might be able to use our knowledge of the spatial meaning for the human visual systems to map a relation, or classification, directly to the compressed form of encoding.   We avoid the need to do complex image analysis and look for smaller features and combine them into larger, more abstract concepts.  

Let's say that with the image-based machine learning, computers are able to classify or 'learn' what certain things look like, by finding similarities in the labels.  Advanced techniques might involve learning about edges, or clusters of areas that are text or whitespace.  A computer might be able to distinguish between a 'letter' or a 'cat' by these kinds of considerations.  It might inevitably have to link the whitespace around parts of the letter that contain text, to carry this out.  

If we had symbols for the parts of the cat, and our final image is encoded as partly 'cat parts'(H,F) and 'whitespace' (W), then producing an image from these symbols does not require the same level of enquiry to determine what is going on in the picture.  We can use our language of 'cat parts' to determine what a human will see.  If the cat's feet are feed into the sequence first, we might be able to conclude that the cat is upside down (WFHW).  If the cat's head is fed into the sequence first, we might be able to conclude it is right way up. (WHFW).  By looking at the encoding we can map a few symbols to what we are looking at (cat up or cat down).  It is a simple transform function.

In the case of letters, we also have the same information, encoded differently in text files to its rendered output.  If we decided to look only at the literal content of the text to determine if it was a 'letter', it might require concepts like addresses, addressees etc.  But that would possibly miss the common structure of letters, and their distinctive visual appearance.  Short lines (a few words), or a short sentence followed by dense text are part of the graphical language of letters. 

In the text form of the letter, Whitespace is encoded by sequences of spaces or line returns.  This cruder (but more compressed) form of information encoding involves less units of initial information.  It involves, paradoxically, more precise information about where the whitespace is than a high resolution image because there are fewer units of information and they are space or not space in a simple binary classification scheme. 

The text-based representation of a letter should be able to be mapped more easily to the human perception of a 'letter' because it is more compactly expressed than the pixels in an image (it has not been converted into higher resolution, or fragmented into smaller pixels that no longer reference the original objects).   {* In the same way, a Word processing document achieves fragmentation of a sentence by inserting paragraphs... it loses meaning by fragmentation that does not maintain the connection with the container... in some ways it is reversable but this requires computational effort.}

## Using text encoding to spatial mapping to classify documents, and/or parts of documents

Unlike the simple encoded cat picture example, we made need some intermediate concepts to help identify the broad graphical 'language' that humans use to interpret documents.  Sentence length (word sequences) might be one of them.  Blocks of text (identifiable by word density counts) may be another.   Horizontal white space (encoded as briefly as a single carriage return) might require little more than a run of carriage returns to define it.

A plain-english tabulation is really a sentence, and one that is possibly an indication of a legal draftsperson.   This 'concept' might help define how a document looks, and distinguish a document from other documents.

With a grammar for what to look for visually, and how that relates to the text encoding, we have ways to do low-level classification without requiring a pixel-based image analysis, or fully interrogating the text.

What we are trying to do is ascertain some visual by using the spacing, the word density and other matters.  These are capable of being understood as visual patterns with sequence and directional qualities.  We seek to turn these into scalar/abstract measures  (non-spatial, but proportional to a spatial quantity, like word density along a row, or in a paragraph).  

We can distinguish a letter from, say, a legal document by the differences in our chosen measures for inferring the presence of some characteristics in the visual image that is encoded.  We look for classification-relevant differences in our quantitatively-measured visual qualities derived directly from the encoding.

If we choose the data [electronic] that has the most economical storage of data (lower visual resolution, combined with libraries to use with that encoding), we may have a simple and effective method for classification than when that data is represented in a different way (higher visual resolution, with expansion of the encoding scheme now complete).

## Simple measures of visual qualities in text encoding for classification of legal documents

Our central concern is with encoding i.e. representation of something more complex (a character, a letter of the alphabet) by a single symbol, or number.   Applied to something like a legal document, at the highest level we might encode a whole paragraph/clause as a symbol, or number.  Seen in this way, a document represents an 'expansion' of that encoding, or a scalar value like high word density can be equated with some visual quality like "a large block of text", or "verbose sentences".  

The goal of converting vague perceptual (spatial) information into more definite identities or quantities is that it allows reasoning based on those objects.   We can convert complex arrangements into a single entity (a number, a scalar value).  The conversion of something like a block of text to scalar word-density or sentence length values loses some information, but also enable us to more easily construct true/false statements.   If we also recognise that Word paragraphs can be sentence fragments, then we can more accurately identify long, tabulated sentences as of high word count plus an indication of structured drafting.  It also does not mean we have lost the information we had about the original object.  It is supplmentary not substitute.

The Word processing environment might encourage authors to indent parts of text, or apply bold to headings and so on.  These are visual cues to readers of the document. The XML has to be converted to a more text-orientated representation, or one with simple encoding of style annotations, to allow it to be more easily analysed for its spatial and word density qualities.  If we an convert the document into one in which the text representation is closer to a simple text-editor representation, with an abstract encoding of heading level, we can then interrogate the use of carriage returns and white space as if a plain text document.}

## Logic

If we can encode a spatial quality in a region as a single index, we have a good method for simple reasoning about it logically.  Logic - implies certain abstractions (logic is really any kind of system of abstraction; a way of encoding the preceptions and statements about the world; i.e. a formal language for recording perception and transferring knowledge).  What kind of logic?  Might be as simple as propositional logic, in this case (might not even need predicate logic). 

Further reading:

cf Russell with 'there exists' and 'for all': 
https://plato.stanford.edu/entries/quantification/. https://www.cs.odu.edu/~cs381/cs381content/logic/prop_logic/tautology/tautology.html.  

If...then is propositional logic (related to existence propositions, implication of B from A e.g. A->B).  https://www.cs.odu.edu/~cs381/cs381content/logic/prop_logic/E2L/E2L.html
