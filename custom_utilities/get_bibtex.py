import urllib, urllib2, cookielib, urllister, sys, time, pickle

def get_page(url):
  filename = "cookies.txt"
  UA='Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12'
  UA2 = 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
  headers = {
    'User-Agent': UA2
  }
  request = urllib2.Request(url, None, headers)
  cookies = cookielib.MozillaCookieJar(filename, None, None)
  cookies.load()
  cookie_handler= urllib2.HTTPCookieProcessor(cookies)
  redirect_handler= urllib2.HTTPRedirectHandler()
  opener = urllib2.build_opener(redirect_handler,cookie_handler)
  response = opener.open(request)
  return response.read()

def make_dictionary_from_bibtex_entry(dict_,lines):
  found_type = False
  # dict_ = {}
  # print lines
  lines = lines.split('\n')
  for i,line in enumerate(lines):
    # print i,'[',line,']'
    if ( line.find('@') != -1 ):
      # test = line 
      # print line
      type_of_entry = line[line.find('@')+1:line.find('{')]
      name_of_entry = line[line.find('{')+1:line.find(',')]
      found_type = True
      dict_[name_of_entry] = {}
      dict_[name_of_entry]['type'] = type_of_entry
      istart = i
      break

  for i,line in enumerate(lines[istart+1:]):
    if ( found_type == True ):
      line = line.strip(' ')
      END_OF_ENTRY = len(line)
      if ( END_OF_ENTRY > 1): 
        if ( line[-1] == ','): END_OF_ENTRY = END_OF_ENTRY - 1
        key = line[0:line.find('=')]
        value = line[line.find('=')+1:END_OF_ENTRY]
        value = value.strip('{'); 
        value = value.strip('}');
        dict_[name_of_entry][key] = value
  # print type_of_entry,name_of_entry
  return dict_

def get_bibtex(termstring, base_url, scholar_subdir, get_all_results):
  terms=termstring.rsplit(" ")
  author_flags = []
  author_flag = False
  literal_flag  = False
  authors = []
  for i,element in enumerate(terms):
    if( element.find('author:') != -1):
      authors.append( element.split('author:')[-1] )
      author_flags.append( i )
      author_flag = True
    if (element.find('-literal') != -1 ):
      literal_flag = True
  if (literal_flag == True): terms.remove('-literal')

  if ( author_flag == False ):
    searchstring="+".join(terms)
    if (literal_flag == True): searchstring= "\""+searchstring+"\""
  else:
    # print '%% Authors to search for: '+(len(authors)*'{} ').format(*authors)
    searchstring="+".join(terms[:min(author_flags)])
    if (literal_flag == True): searchstring= "\""+searchstring+"\""
    for i in author_flags:
      searchstring+='+'+terms[i]
  # searchstring= "+".join(terms)DSDfit_all_file_10232012_17-47.tar.gz

  # print searchstring
  params = urllib.urlencode({'q': searchstring})
  url = base_url+url_subdir+"?"+params
  print '%% url search = ',url
  page_data = get_page(url)

  parser = urllister.URLLister()
  parser.feed(page_data)
  parser.close()
  biburls=[]
  # print parser.urls, len(parser.urls)
  for url in parser.urls:
      if url.find('scholar.bib')>0:
          biburls.append(url)

  Nbiburls = len(biburls)
  
  if biburls:
   retpage=get_page(base_url+biburls[0])
  else:
   retpage=""
  all_results = [retpage]
  if ( get_all_results == True):
    if ( Nbiburls > 1):
     for url in biburls[1:]:
      print "biburl:", url
      time.sleep(2)
      all_results.append ( get_page(base_url+url) )
  return retpage,all_results

if __name__ == "__main__":
  if len(sys.argv) >= 2:
    base_url = "http://scholar.google.com"
    url_subdir = "/scholar"
    options_list = sys.argv[1:]
    # print  options_list
    if ( "-getall" in options_list ): get_all_results = True
    else: get_all_results = False
    # print get_all_results
    titles_file = [ x for x  in options_list if not ( x=="-getall" ) ]
    # titles_file=sys.argv[1:]
    # if titles_file.find('.txt') != -1)
    # file = open(titles_file)
    lines=[]
    fopen2 = open('result.bib','w')
    dict_ = {};
    for termstring in titles_file:
      # termstring=file.readline()
      if not termstring:
          break
      else:
          # print 'Term searched for: "'+ termstring.strip()+'"'
          result,all_results = get_bibtex(termstring, base_url, url_subdir,get_all_results)
          fopen2.write("%% Top result \n")
          fopen2.write(all_results[0])
          if (get_all_results == True):
            fopen2.write("%% Other results \n")
            print "%% \t","\t"," Other results \n"
            for element in all_results[1:]:
              print element
              dict_ = make_dictionary_from_bibtex_entry(dict_,element)
              fopen2.write(element)
          print "%% \t","\t"," Top result \n"
          print result
          dict_ = make_dictionary_from_bibtex_entry(dict_,result)
          print dict_
          fopen2.close()
          pickle.dump( dict_, open( 'result.p', "wb" ) )
  else:
    print "usage: python "+sys.argv[0]+" [search string 1] [search string 2] ... \n results stored in result.bib"


# base code obtained from 
# http://code.activestate.com/recipes/523047-search-google-scholar/

# if __name__ == "__main__":
#   if len(sys.argv)==2:
#     base_url = "http://scholar.google.com"
#     url_subdir = "/scholar"
#     titles_file=sys.argv[1]
#     # if titles_file.find('.txt') != -1)
#     file = open(titles_file)
#     lines=[]
#     fopen2 = open('result.bib','w')
#     while 1:
#       termstring=file.readline()
#       if not termstring:
#           break
#       else:
#           print 'Term searched for: "', termstring.strip(), '"'
#           result = get_bibtex(termstring, base_url, url_subdir)
#           print result
#           fopen2.write(result)
#     fopen2.close()

#   else:
#     print "usage: python "+sys.argv[0]+" titles.txt\n titles.txt must contain a list of publication titles."


# the usage of this script is simple. Provide a list of terms or titles in a text file and separate every search by a new line within the file. The text file should look something like this

# Resonance of an Optical Monopole Antenna Probed by Single Molecule Fluorescence
# Optical antennas direct single-molecule emission
# ...

# additionally a cookies.txt is needed in order to tell google that you want BibTeX entries to be added (normaly done by changing the "scholar preferences"). Here is a sample of the cookies.txt file

# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
# .scholar.google.com TRUE    /   FALSE   XXX GSP ID=XXX:IN=XXX+XXX:CF=4

# this data can easily be extracted from your browser. for firefox i can recommend the "edit cookies" addon.

# Warning: Google will flag you as a bot if you intensively use this script. so be responsible (and use a random wait interval between get_bibtex interations).
