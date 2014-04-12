#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

def parse_markdown_to_beamer(filein,fileout,default_header,author,institute):
	"""
	Sample file :
	--------------------------------------------------------------------
		#_ Introduction
		## Frame 1
		carlos
		
		## Frame 2
		is
		
		#_ Motivation
		
		## Frame 3
		$$D_n = D0\sin\phi$$
		
		## Frame 4
		*i
		** a
		** b
		*i
		
		## Frame 5
		*e 
		** a
		** $\alpha$
		*e
	"""
	filename = open(filein,'r')
	converted_doc_lines = []
	
	start_list     = True
	start_document = True
	start_section  = True
	start_frame    = True
	
	for line in filename:
		line_code = line[0:2]
		
		if ( line_code  == '!_'):
			title_str = line[2:].strip()
		elif ( line_code  == '#_'):
			if ( start_section == True ):
				converted_doc_lines.append('\section{{{}}}'.format(line[2:].strip()) )
				start_section = False
			else:
				converted_doc_lines.append('	\end{frame}')
				start_frame = True
				converted_doc_lines.append('\section{{{}}}'.format(line[2:].strip()) )
		elif ( line_code  == '##' ):
			if start_frame == True:
				converted_doc_lines.append('	\\begin{{frame}}{{ {} }} '.format(line[2:].strip()))
				start_frame = False
			else:
				converted_doc_lines.append('	\end{frame}')
				converted_doc_lines.append('	\\begin{{frame}}{{ {} }} '.format(line[2:].strip()))
		elif ( line_code == '*i'):
			if ( start_list == True):
				converted_doc_lines.append('		\\begin{{itemize}}{} '.format(line[2:].strip()))
				start_list = False
			else:
				converted_doc_lines.append('		\end{itemize}')
				start_list = True
		elif ( line_code == '*e'):
			if ( start_list == True):
				converted_doc_lines.append('	\\begin{{enumerate}}{} '.format(line[2:].strip()))
				start_list = False
			else:
				converted_doc_lines.append('	\end{enumerate}')
				start_list = True
		elif ( line_code  == '**' ):
			converted_doc_lines.append('			\item {}'.format(line[2:].strip()))
		else:
			converted_doc_lines.append('		{}'.format(line.strip()))
	converted_doc_lines.append('	\end{frame}')
	
	fileo = open(fileout,'w')
	for line in converted_doc_lines:
		fileo.write('{}\n'.format( line ))
	fileo.close()
	
	if default_header == True:
		fileheader = open('beamer_header_'+fileout,'w')
		fileheader.write("""
\documentclass[10pt]{{beamer}}
\usepackage[utf8x]{{inputenc}}
\usepackage{{default}}

\\title{{ {} }}
\\author{{ {} }}
\institute{{ {} }}
\date{{}}
\\begin{{document}}
\maketitle

\input{{ {} }}

\end{{document}}
""".format(*[title_str,author,institute,fileout]) )

if __name__ == "__main__":
	print "Converting custom MARKUP to beamer slide code "
	print " Fri Jul 6 18:51:28, version. 0.3.0"
	N = len(sys.argv)
	author = 'Carlos Chiquete'
	institute = 'WX-9, Shock \& Detonation Physics Group \\\ Los Alamos National Laboratory'
	#print sys.argv
	
	if ( N == 2):
		fileout = sys.argv[1].replace('.md','.tex')
		parse_markdown_to_beamer(sys.argv[1],fileout,False,author,institute)
	elif ( N > 2):
		fileout = sys.argv[1].replace('.md','.tex')
		for i,flag in enumerate(sys.argv[2:]):
			#print i,flag,sys.argv[2+i+1]
			if ( flag == '-a'):
				author = sys.argv[2+i+1]
			elif ( flag == '-i'):
				institute = sys.argv[2+i+1]
			elif ( flag == '-o'):
				fileout = sys.argv[2+i+1]
			parse_markdown_to_beamer(sys.argv[1],fileout,True,author,institute)
	else:
		print "Usage: (-i : instutute, -a : author, -o : output file )"
		print "\t Example : \n \t \t./mdbeamer.py talk.md -i 'UofA' -a 'Carlos Ch.' -o 'talk.tex'"

