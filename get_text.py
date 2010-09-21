#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib, os
"""
get_text.py
Detta script hämtar en undertext's filen frånn undertexter.se
./get-text.py <sökterm>
ex:
./get-text.py johan
./get-text.py house md s05e17
"""
def filter_page():
    """
    Filtrerar fram mÃ¶jliga resultat frÃ¥n hemsidan,
    och returnerar dessa som tupler i form: (id, url)
    """
    ut = "http://undertexter.se/?p=arkiv&cat=" + '%20'.join(sys.argv[1:])
    webtext = urllib.urlopen(ut).read()
    first = webtext.find('<title>' + ' '.join(sys.argv[1:]) + '</title>')
    last = webtext.rfind('<a href="javascript:history.go(-1)"><b>')
    newtext = webtext[first:last]
    textlist = []
    rawtextlist = newtext.split('\n')
    [textlist.append(line.strip()) for line in rawtextlist]

    hits = []
    hits.append(('Ingen av dessa.',0))
    iter = len(textlist)
    i = 0
    while i < iter:
        if 'Nedladdningar' in textlist[i]:
            hits.append((textlist[i+1][44:-5], "http://www.undertexter.se/utext.php?" + textlist[i-5][48:textlist[i-5].rfind('alt="')-2]))
        i +=1

    return hits

def get_textfile_url(hits):
    """
    Frågar användaren vilken rls som den vill ladda ner.
    0 betyder att man vill avbryta.
    """
    i = 0
    for item in hits:
        print "[" + str(i) + "] " + item[0]
        i +=1
    return hits[int(raw_input("Vilken rls? "))][1]

def down_load_sub(url):
    """
    Tar en url och laddar ner filen.
    """

    if url:
        a = urllib.urlopen(url)
        url = a.geturl()
        a.close()
        urllib.urlretrieve(url, url.rsplit('/')[-1])
        print 'Laddade ner' ,url.rsplit('/')[-1]

if __name__ == "__main__":
    result = filter_page()
    choice = get_textfile_url(result)
    down_load_sub(choice)
