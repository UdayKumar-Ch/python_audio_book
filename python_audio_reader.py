from os import system
from typing import List
from pyttsx3 import speak
import slate3k as slate
import argparse
import pyttsx3
import sys
import datetime
from functools import reduce

class AudioFileReader(object):
    def __init__(self, filename, start_page = 1, password = None, end_page= None, speed=1.0, output=None, male_or_female = "f" ) -> None:
        self.fileName = filename
        self.start_page = start_page
        self.password = password
        self.totalPages = None
        self.output = output
        self.end_page = end_page
        self.speed = speed
        self.male_or_female_voice = male_or_female
        self.document = self.extractText()
        self.validateParameters()
        self.speaker = pyttsx3.init()
        self.initializeSpeakerConfiguration()
        
    def initializeSpeakerConfiguration(self) -> None:

        # Type of voice need to be used
        voices = self.speaker.getProperty('voices')
        if self.male_or_female_voice[0].lower() == 'm' and self.male_or_female_voice.lower() == 'male':
            self.speaker.setProperty('voice', voices[0].id)
        else:
            self.speaker.setProperty('voice', voices[1].id)

        # Rate of words in speech per minute
        rate  = self.speaker.getProperty('rate')
        self.speaker.setProperty('rate', 200 * self.speed)

        # check/append speaker output file with .mp3
        if self.output != None:
            if self.output.lower().endswith('.mp3'):
                array = self.output.split(".") 
                self.output = array[0]+'.'+array[1].lower()
            else:
                self.output += ".mp3";

    def validateParameters(self) -> None:
        if not self.isPdfFile():
            sys.exit("This program will only works with pdf files")
        elif self.end_page != None and self.totalPages < self.end_page:
            sys.exit("Given End_page is invalid because, total no. of pages are less than the given end page")
        elif self.speed == 0.0:
            sys.exit("speed cannont be selected as 0.0")
        elif self.start_page > self.totalPages:
            sys.exit("you cannot select start page greater than total pages in a pdf file")
        
         
    def isPdfFile(self) -> bool:
        return self.fileName.lower().endswith('.pdf')

    def replaceNewLineWithEmptySpace(self, page_text) -> str:
        return page_text.replace("\n", " ")
    
    def replaceSlashWithOr(self, page_text) -> str:
        return page_text.replace("/", " or ")

    def isPasswordEnabled(self) -> bool:
        return self.password != None and len(self.password.trim()) != 0

    def extractText(self) -> List[str]:
        try:
            with open(self.fileName, 'rb') as f:
                document = None
                if self.isPasswordEnabled:
                    document = slate.PDF(f, self.password)
                else:
                    document = slate.PDF(f)
            self.totalPages = len(document)
            return list(map(self.replaceSlashWithOr, map(self.replaceNewLineWithEmptySpace, document)))
        except:
            sys.exc_info("Unexpected Error: {}, {}, line: {}".format(sys.exc_info()[0],
                                         sys.exc_info()[1],
                                         sys.exc_info()[2].tb_lineno))

    def __startPlaying(self, text) -> None:
        self.speaker.say(text)
        self.speaker.runAndWait()

    def __save_voice_to_file(self, text) -> None:
        self.speaker.save_to_file(text, self.output)
        self.speaker.runAndWait()

    def startPlaying(self):
        array = None
        if self.start_page != None and self.end_page != None:
            array  = self.document[self.start_page-1 : self.end_page-1]
        elif self.start_page != None and self.end_page == None:
            array = self.document[self.start_page-1:]
        elif self.start_page == None and self.end_page != None:
            array = self.document[:self.end_page-1]
        else:
            array = self.document
        
        string_to_read = reduce(lambda a,b : a+b, array)

        if self.output != None:
            self.__save_voice_to_file(string_to_read)
        else:
            self.__startPlaying(string_to_read)
    
if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type= str , required=True)
    parser.add_argument('--start_page', '-s', type= int, default = 1)
    parser.add_argument('--end_page','--ep', type=int, default = None)
    parser.add_argument('--password', '-p', required=False, type = str, default = None)
    parser.add_argument('--speed', '--s', type=float, required=False, default= 1.0)
    parser.add_argument('--output','--o', type=str, required=False, default = None)
    parser.add_argument('--male_or_female', '--m/f' , type=str, default='f')
    args = parser.parse_args()
    # vars_args = vars(args)
    print(f'Arguments passed:\n\t {args}')
    print("Started playing file: ", datetime.datetime.now())
    audioFileReader  = AudioFileReader(**args.__dict__)
    audioFileReader.startPlaying()
    print("Completed reading : ", datetime.datetime.now())

