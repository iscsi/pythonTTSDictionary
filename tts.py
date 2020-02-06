#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from gtts import gTTS
from pydub import AudioSegment

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

    lecCtr = 0
    ctr = 0
    start = 0

    #categorize the words to lectures

    category = {}

    for row in values:
        if row and len(row) > 1 and row[0] and row[1]:
            ctr = ctr + 1
        else :
            if ctr > start + 5 :
                lecCtr = lecCtr + 1
            for i in range(start,ctr) : 
                category[i] = lecCtr
            if ctr > start + 5 :
                start = ctr
    if ctr > start + 5 :
        lecCtr = lecCtr + 1
    for i in range(start,ctr) : 
        category[i] = lecCtr
    if ctr > start + 5 :
        start = ctr

    two_sec_pause = AudioSegment.silent(duration=2000)
    ctr = 0
    start = 0

    for row in values:
        if row and len(row) > 1 and row[0] and row[1]:
            print('%s, %s' % (row[0], row[1]))
            
            row[0] = row[0].replace('etw.', 'etwas ')
            row[0] = row[0].replace('jmdn.', 'jemanden ')
            row[0] = row[0].replace('jmdm.', 'jemandem ')
            
            
            row[1] = row[1].replace('so.', 'someone ')
            row[1] = row[1].replace('sth.', 'something ')
            
            ttsEng = gTTS(row[1], lang = 'en')
            ttsEng.save('eng_%d.mp3'%(ctr))
            
            ttsGer = gTTS(row[0], lang = 'de')
            ttsGer.save('ger_%d.mp3'%(ctr))
            
            if ctr + 1 == len(category) or category[ctr] < category[ctr+1] :
                finalSound = AudioSegment.silent(duration=500)
                
                for i in range(start,ctr) :    
                    actEngSound = AudioSegment.from_mp3('eng_%d.mp3'%(i))
                    actGerSound = AudioSegment.from_mp3('ger_%d.mp3'%(i))
                    finalSound = finalSound + actEngSound + two_sec_pause + actGerSound + two_sec_pause

                finalSound.export('final_%d.mp3'%(category[ctr]), format = "mp3")        
                start = ctr

            ctr = ctr + 1
        
    
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        main(key=argv[1])
    else:
        main()