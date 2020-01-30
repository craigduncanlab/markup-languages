import sml2docx
import review
import xmlutil
import sys # for processing command line args
import csv # library for simple csv reading

global h1code, h2code, notescode,lvlnames,schemename,lettermeta

# Program to translate a Plain Markup Language (PML) document to Styled Markup Language (SML).
# The names 'Plain Markup Language', 'Styled Markup Language' and this implementation (c) Craig Duncan
# Created 19 December 2019 by Craig Duncan
# (c) Craig Duncan 2019-2020

def openlmd(textfile):
	output=[]
	with open(textfile, 'r') as csvfile:
		EOLC="\r\n"
        spamreader = csv.reader(csvfile,delimiter="\n") # no delimiter.  Default is?
		for row in spamreader:
			if (len(row)>0 and row is not None):  # Null rows are ignored?  Why not 'default'?
				value=row[0]
				#exit()
				print(value)
				output.append(value)
	return output

# These are OOXML specific markdown schemes.  There is no intermediate 'CommonMarkdown' yet
# but this can be included if needed.
def chooseLetterScheme(myArray): 
	global h1code,h2code,notescode,lvlnames,schemename,lettermeta
	print("Letter Scheme. OK")
	schemename="letter"
	h1code="#LDB" # boldheading
	h2code="#LDBN" #numbered paragraph bold
	notescode="#LN"
	lvlnames=["LDP1","H3","H4","H5"]
	#
	# Do this if necessary to establish boundaries of letter
	precount=1
	letterstart=1
	letterend=1
	signindex=0
	for lines in myArray:
		if ("Dear" in lines or "Sir" in lines or "Madam" in lines or "To Whom" in lines):
			letterstart=precount
		if ("Yours " in lines or "Kind regards" in lines or "Regards" in lines or "Sincerely" in lines or "Faithfully" in lines):
			signindex=precount
			letterend=precount
		precount=precount+1
	lettermeta=[letterstart,letterend,signindex]
	# not found
	if (letterstart==1 and letterend==1):
		print("Cannot detect letter regions")
		chooseDefaultScheme()


def chooseMemoScheme():
	global h1code,h2code,notescode,lvlnames,schemename
	print("Memo Scheme. OK")
	schemename="memo"
	h1code="#SCHEDUL1" # boldheading
	h2code="#H2"
	notescode="#N"
	lvlnames=["Indent1","H3","H4","H5"]

def chooseLegalDocScheme():
	global h1code,h2code,notescode,lvlnames,schemename
	print("legal Doc Scheme. OK")
	schemename="legaldoc"
	h1code="#H1" # boldheading
	h2code="#H2"
	notescode="#N"
	lvlnames=["Indent1","H3","H4","H5"]

def chooseDefaultScheme():
	global h1code,h2code,notescode,lvlnames,schemename
	print("Default Scheme. OK")
	schemename="defaultdoc"
	h1code="#H1" # boldheading
	h2code="#H2"
	notescode="#N"
	lvlnames=["Indent1","H3","H4","H5"]

# This processes an lmd document (supplied as an Array)
# New documents : -n- (See Specification.md)
# If there is no markdown code, tries its best to add one (and expand plain english tabulation)
# Change style scheme: meta: letter or meta: legaldoc (so far)
# TO DO: process to markdown, then to OOXML
# 
def processLegalMarkdown(myArray,notesOn):
	lvl=0
	EOLC="\r\n"
	global h1code,h2code,notescode,lvlnames,lettermeta
	# default
	#TO DO: choose a default scheme
	chooseDefaultScheme()
	output=[]
	#exit()
	#arraysize=len(myArray)
	#signindex=0
		
	linecount=0
	for item in myArray:
		linecount=linecount+1
		first1=item[:1]
		first2=item[:2]
		first3=item[:3]
		first5=item[:5]
		last1=item[-1:]
		last3=item[-3:]
		semicolsplit=item.split(';')
		semicolnum=len(semicolsplit)
		words=item.split(' ')
		processed=False
		# Check if this line is just a note line before doing anything else.
		if (first2=="//" and processed==False): # escaped
			newitem=item[2:]+notescode
			if (notesOn==True):
				print("NotesOnDetected")
				output.append(newitem) # if notes were 'off' we'd skip this step
				processed=True
				
		# This assumes stream processing, not prior indexing.
		if (first5=="meta:"):
			if ("letter" in item):
				chooseLetterScheme(myArray)
				processed=True
			elif ("legaldoc" in item):
				chooseLegalDocScheme()
				processed=True
			elif ("memo" in item):
				chooseMemoScheme()
				processed=True

		# --- check for instructions and ignore
		if (first3=="---" or first3=="-n-"):
			processed=True
			output.append(item)

		# --- BREAK UP LISTS IN SENTENCES IF NEEDED (REGARDLESS OF SCHEME)
		if (semicolnum>1 and processed==False): # and schemename!="defaultdoc"
			print(item)
			newparas=convertSentenceToLists(item,lvl)
			print(newparas)
			#exit()
			for y in newparas:
				output.append(y)
				processed=True
	
		# --- DEFAULT MARKDOWN SCHEME
		if (semicolnum<=1 and schemename=="defaultdoc" and processed==False):
			newitem=processGeneralItem(item,lvl,linecount)
			if len(newitem)>0:
				output.append(newitem)
				newitem=""
			processed=True


		# --- IF LETTER SCHEME ----
		
		if (semicolnum<=1 and schemename=="letter" and processed==False):
			newitem=processLetterItem(item,lvl,linecount)
			if len(newitem)>0:
				output.append(newitem)
				newitem=""
			processed=True
		
		# --- IF LEGAL DOC
		
		if (semicolnum<=1 and schemename=="legaldoc" and processed==False):
			newitem=processLegalDocItem(item,lvl)
			if len(newitem)>0:
				output.append(newitem)
				newitem=""
			processed=True

		# --- IF MEMO
		
		if (semicolnum<=1 and schemename=="memo" and processed==False):
			newitem=processMemoItem(item,lvl,linecount)
			if len(newitem)>0:
				output.append(newitem)
				newitem=""
			processed=True	

	return output

#Process Memo items
# if(first1!="-" note needed - already checked.
# linecount needed?
def processMemoItem(item,lvl,linecount):
	#analysis
	first1=item[:1]
	first2=item[:2]
	first3=item[:3]
	first5=item[:5]
	last1=item[-1:]
	last3=item[-3:]
	words=item.split(' ')
	if (len(words)<10):
			if("." not in last3 and "#" not in last3 and ":" not in last3):
				style=h1code # default
				if (linecount>5): # use second heading type after intro
					style=h2code
			else:
				style="#"+lvlnames[lvl]
	elif (len(words)>=10):
		style="#"+lvlnames[lvl]
	newitem=item+style	
	return newitem

#Holding item for now
def processGeneralItem(item,lvl,linecount):
	style="#"+lvlnames[lvl]
	newitem=item+style
	print("%d:%s" % (linecount,item))
	return newitem


# Add OOXML codes to a specific Legal Doc Item
# Uses the current lvlnames as per scheme, and the lvl as set in loop for main array
# Simple rules for this implicit markdown are:
# Less than 10 words, not the document name (-n-), not ending in full stop and no existing # code at end
# = heading.  If all capitals, then H1 otherwise H2.
# Default paragraph is Indent1.  Default level for : ; lists (plain English) is H3.
# Everything else requires explicit use of # for markup.
#
def processLegalDocItem(item,lvl):
	global h1code,h2code,notescode,lvlnames
	#analysis
	first1=item[:1]
	first2=item[:2]
	first3=item[:3]
	first5=item[:5]
	last1=item[-1:]
	last3=item[-3:]
	words=item.split(' ')
	if(first1!="-" and len(words)<10 and last1!="." and "#" not in last3 and ":" not in last3):
		style=h1code
		for a in item:
			if(a!=" " and a!="?" and a!="!" and a.isupper()==False):
				style=h2code
	else:
		style="#"+lvlnames[lvl]

	newitem=item+style
	return newitem
		

# Add a particular OOXML style to text depending on contents, position
# return a letter paragraph formatted with an OOXML markup style (i.e. this is not CommonMarkup)
# TO DO: modularise this even further.
def processLetterItem(item,lvl,linecount):
	#init
	global h1code,h2code,notescode,lvlnames,lettermeta

	newitem=""
	style=""
	#analysis
	first1=item[:1]
	first2=item[:2]
	first3=item[:3]
	first5=item[:5]
	last1=item[-1:]
	last3=item[-3:]
	#semicolsplit=item.split(';')
	#semicolnum=len(semicolsplit)
	words=item.split(' ')
	# Date flags
	datelist=["January","February","March","April","May","June","July","August","September","October","November","December"]
	datezone=False
	for x in datelist:
		if (datezone==False and x in item or x[:3] in item):
			datezone=True
	# Lettermeta/Signing flags
	letterstart=lettermeta[0]
	letterend=lettermeta[1]
	signindex=lettermeta[2] # or init to 0
	signzone=False
	if (signindex!=0 and (linecount-signindex)<8):
		signzone=True
	else:
		signzone=False
		
	# sections (mutually exclusive)
	if (linecount<=letterstart):
		print(linecount)
		print(item)
		print(lettermeta)
		print(lettermeta[0])
	
	# process anything not a regular sentence or start of a para
		if (len(words)<10 and last1!="." and "#" not in last3 and ":" not in last3):

			# lines before body, at start
			if (datezone==False):
				style="#LDP0" #Indent no space after	
			if (datezone==True): # TO DO: space before as well
				style="#LDdate" 
			# lines outside body,at end
	
	if (linecount>=letterend):
		style="#"+lvlnames[lvl]
	
	# body paragraph for the "Dear" line
	if (linecount==letterstart):
		style="#"+lvlnames[lvl]

	# less than 10 lines in body of letter
	if (linecount>letterstart and linecount<letterend):
		#letter regular style for a sentence, wherever it is
		if (len(words)>10):  # (last1=="?" or "." in last3) and
			if ("#" not in last3 and ":" not in last3):
				style="#"+lvlnames[lvl]
		# first heading after the letter begins
		if (len(words)<10):
			if("." not in last3 and "#" not in last3 and ":" not in last3):
				style=h1code # default
				if (linecount>letterstart+1):
					style=h2code
			else:
				style="#"+lvlnames[lvl]
	newitem=item+style	
	return newitem

# a plain english tool to convert non-broken sentences into paras with OOXML codes
# Example of auto-markdown using grammatical rules
# for OOXML codes, uses whatever lvlnames scheme has been activated by current scheme
# TO DO: convert to an intermediate CommonMarkdown?
def convertSentenceToLists(item,count):
	result=[]
	newchars=[]
	count=0
	lvl=0 # ok?while(count<len(item)):
	newchars=[]
	last1=item[-1:]
	last3=item[-3:]
	while(count<len(item)):
		count=count+1
		a=item[count-1]
		p=a
		s=''
		# conditions needed before plain english level break included
		if (a==":" and (len(item)-count)>4 and last1=="."):
			p=a+"#"+lvlnames[lvl]
			newchars.append(p)
			newstring=s.join(newchars)
			newchars=[]
			result.append(newstring)
			newstring=""# in this situation it is never a string of # with code at end
			if (lvl<(len(lvlnames)-1)):
				lvl=lvl+1
		# if we find 'and' after the semi-colon
		elif(a==";" and (len(item)-count-1>4) and item[count-1:count+4]=="; and"):
			# ignore this semi-colon
			p=a+" and#"+lvlnames[lvl]
			#item = item[0:count-1]+item[count+5] # remove the and and carry on
			count=count+4
			#print(item)
			#exit()
			newchars.append(p)
			newstring=s.join(newchars)
			newchars=[]
			result.append(newstring)
			newstring=="" # in this situation it is never a string of # with code at end
			#lvl = no change

		# if we do not find 'and' after the semi-colon
		# 4 is the len of the ' and' string
		elif(a==";" and (len(item)-count-1>4) and item[count:count+4]!="; and"):
			#print(item[count-1:count+4])
			p=a+"#"+lvlnames[lvl]
			newchars.append(p)
			newstring=s.join(newchars)
			newchars=[]
			result.append(newstring)
			newstring=="" # in this situation it is never a string of # with code at end
			#lvl = no change
		# a full stop encountered before the end
		elif (a=="." and (len(item)-count)<4 and "#" not in last3):
			p=a+"#"+lvlnames[lvl]
			newchars.append(p)
			newstring=s.join(newchars)
			result.append(newstring)
			newstring=""
			newchars=[]
			if lvl>0:
				lvl=lvl-1
		else:
			newchars.append(p)
				#newstring=s.join(newchars)
			# TO DO: if reaches end, just add another entry
	return result

# START HERE
# we are able to see how this code was invoked, and if called by another program, take no immediate action
# some prefer this technique for checking if this is the top-level or stand-alone source code run from command line:
# if __name__ == '__main__':

args=len(sys.argv)
#alternative way of checking how this is invoked
#progname=sys.argv[0]
#if (progname!="docmaker.py"):
#    print(progname)
#    exit()
notesOn=False
outFolder=False
outFoldIndex=0
outFoldName="/output"
lmdFoldName="/lmd"
count=0
flagindex=0

if (args<2):
	print("Please supply a filename with your program.")
	print("i.e. python3 plaineng.py filename.lmd")

elif (args==2 and __name__ == '__main__'):
	filename=sys.argv[1]
	if len(filename)!=0:
		# remainder is optional for now hey:
		#
		nameonly,suffix=filename.split('.')
		if (suffix=="txt" or suffix=="md" or suffix=="lmd" or suffix=="pml"):    # or suffix=="odt":
			print("Name is "+filename)
			print("Hello, this executed after importing docmaker")
			contentArray=openlmd(filename)
			adjustedArray=processLegalMarkdown(contentArray, False)	 #notes on by default
			docmaker.docFromArray(adjustedArray)# create docx from results (in output folder)
		else:
			print("This program requires .txt .md or .lmd extensions for the input markdown file")
	else:
		doError()
		# TO DO: just use the new filename if an error, create new blank file to work with.

elif (args>2 and __name__ == '__main__'):
	for x in sys.argv:
		if "-n" in x:
			notesOn=True
			flagindex=count
		# This output folder is WIP
		if "-o" in x:
			outfolder=True
			outFoldIndex=x
			if (len(sys.argv)>count):
				outFoldName=sys.argv[count+1]
		count=count+1
	
	# filename is not the -no argument
	if flagindex==0:
		filename=sys.argv[1]
	if flagindex==1:
		filename=sys.argv[2]
	elif flagindex==2:
		filename=sys.argv[1] # flag at end

	if len(filename)!=0:
		# remainder is optional for now:
		#
		nameonly,suffix=filename.split('.')
		if (suffix=="txt" or suffix=="md" or suffix=="lmd"):    # or suffix=="odt":
			print("Name is "+filename)
			contentArray=openlmd(filename)
			adjustedArray=processLegalMarkdown(contentArray,notesOn)	
			docmaker.docFromArray(adjustedArray)	
		else:
			print("This program requires .txt .md or .lmd extensions for the input markdown file")
	else:
		doError()
else:
	print("WOW")
