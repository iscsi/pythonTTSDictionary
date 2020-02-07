#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from gtts import gTTS
from pydub import AudioSegment
from random import shuffle

def main(key=None):
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build(
        'sheets',
        'v4',
        http=httplib2.Http(),
        discoveryServiceUrl=discoveryUrl,
        developerKey='AIzaSyBfIlNAVYrT0ZHej4cM-f9ZnPfVSimJ6rQ')

    spreadsheetId = '1Hhz6EaRhWsv4BOWoM8NACR7Gyh57-l7dyubkBUVh-KY'
    sheetId = 'AntrimA1/A2' # '1988626014' 
    rangeName = 'A1:B500'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=sheetId + '!' + rangeName).execute()
    values = result.get('values', [])

    #permute the words

    numberOfWords = 20
    wordlist = []

    for row in values:
        if row and len(row) > 1 and row[0] and row[1]:
            wordlist.append(row)
            
    shuffle(wordlist)

    categoryCnt = int(len(wordlist) / numberOfWords)
    numberOfWords = int(len(wordlist) / categoryCnt)
    
    categoryRem = len(wordlist) % categoryCnt
        
    two_sec_pause = AudioSegment.silent(duration=2000)
    ctr = 0
    
    finalSound = AudioSegment.silent(duration=500)

    for ger, eng in wordlist:
        print('%s, %s' % (ger, eng))
        ger = ger.replace('etw.', 'etwas ')
        ger = ger.replace('jmdn.', 'jemanden ')
        ger = ger.replace('jmdm.', 'jemandem ')
        
        eng = eng.replace('so.', 'someone ')
        eng = eng.replace('sth.', 'something ')
        
        ttsEng = gTTS(eng, lang = 'en')
        ttsEng.save('eng.mp3')
        
        ttsGer = gTTS(ger, lang = 'de')
        ttsGer.save('ger.mp3')
        
        actEngSound = AudioSegment.from_mp3('eng.mp3')
        actGerSound = AudioSegment.from_mp3('ger.mp3')
        finalSound = finalSound + actEngSound + two_sec_pause + actGerSound + two_sec_pause

        ctr = ctr + 1
        #check need to export
        num = int (ctr / numberOfWords)
        
        num = num * numberOfWords + min (num, categoryRem)
        
        if ctr > 0 and (ctr  == num or ctr == len(wordlist)):
            print('%d', ctr)
            finalSound.export('final_%d.mp3'%(int (ctr / numberOfWords)), format = "mp3")
            #check need to start a new or not
            
            if not ctr == len(wordlist) :
                finalSound = AudioSegment.silent(duration=500)
        
        
        
        
    
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        main(key=argv[1])
    else:
        main()