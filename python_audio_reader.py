from typing import List
import slate3k as slate
import argparse
import pyttsx3
import datetime

class AudioFileReader(object):
    def __init__(self, fileName, start_page = 1, password = None) -> None:
        self.fileName = fileName
        self.start_page = start_page
        self.password = password
        self.totalPages = 0
        self.isPdfFile()
        self.speaker = pyttsx3.init()
    
    def isPdfFile(self) -> bool:
        return self.fileName.lower().endswith('.pdf')

    def replaceNewLineWithEmptySpace(self, page_text):
        return page_text.replace("\n", " ")
    
    def replaceSlashWithOr(self, page_text):
        return page_text.replace("/", " or ")

    def isPasswordEnabled(self) -> bool:
        return self.password != None and len(self.password.trim()) != 0

    def extractText(self) -> List[str]:
        with open(self.fileName, 'rb') as f:
            document = None
            if self.isPasswordEnabled:
                document = slate.PDF(f, self.password)
            else:
                document = slate.PDF(f)
        self.totalPages = len(document)
        return list(map(self.replaceSlashWithOr, map(self.replaceNewLineWithEmptySpace, document)))[self.start_page-1:]

    def __startPlaying(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

    def startPlaying(self):
        extracted_text = self.extractText()
        current_page = self.start_page - 1
        for page in range(0, self.totalPages - self.start_page+1):
            self.__startPlaying("Reading page number "+str(self.start_page+page))
            # print("-+-"*5, extracted_text[page],"-+-"*5 )
            self.__startPlaying(extracted_text[page])

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type= str , required=True)
    parser.add_argument('--start_page', '-s', type= int, default = 0)
    parser.add_argument('--end_page','--ep', type=int)
    parser.add_argument('--password', '-p', required=False, type = str)
    args = parser.parse_args()
    print(f'Arguments passed:\n\t {args}')
    print("Started playing file: ", datetime.datetime.now())
    audioFileReader  = AudioFileReader(args.filename, args.start_page, args.password)
    audioFileReader.startPlaying()
    print("Completed reading : ", datetime.datetime.now())

