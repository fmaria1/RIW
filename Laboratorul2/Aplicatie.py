import os
import collections
import json
files_path= 'D:/AN4/sem2/riw/RIW/Laboratorul1/fisiere_text'
stop_words_path = r'stopwords'
exceptions_words_path = r'exceptions'

class TextParser:
    def __init__(self, dirPath):
        self.dirPath=dirPath
        self.directories =[self.dirPath]
        self.exceptions = []
        self.stops = []
        self.words = collections.OrderedDict()
 
    def read_stopwords_and_exceptions(self,file_path, list_of_words):
        with open(file_path, 'r',encoding='UTF-8') as file:
            word = ''
            letter = file.read(1)
            while letter != '':
                if letter != '\n':
                    word += letter.lower()
                else:
                    list_of_words.append(word)
                    word = ''
                letter = file.read(1)
                
    def text_parse(self,file_path):
        f=open(file_path, 'r')
        self.words[file_path]={}
        letter=f.read(1).lower()
        word=letter
        while True :
            letter = f.read(1).lower()
            
            if  letter=='':
                break
            else:

                if letter >= 'a' and letter <= 'z' or letter >= '0' and letter <= '9':
                    word=word+letter
                else:
                    if word in self.exceptions:

                        if word in self.words[file_path]:
                            self.words[file_path][word]=self.words[file_path][word]+1

                        else:
                             self.words[file_path][word]=1
                    else:

                        if word!='' and word not in self.stops:

                            if word in self.words[file_path]:
                                self.words[file_path][word]=self.words[file_path][word]+1
                            else:
                                self.words[file_path][word]=1

                    word=''
        f.close()
        

      
    def read_files(self):

        self.read_stopwords_and_exceptions(exceptions_words_path, self.exceptions)
        self.read_stopwords_and_exceptions(stop_words_path, self.stops)
        for dir in self.directories:
            for f in os.listdir(os.path.join(self.dirPath,dir)): 
                
                if os.path.isdir(os.path.join(dir,f)):

                  self.directories.append(os.path.join(dir,f))
                elif os.path.isfile(os.path.join(dir,f)):

                    key=os.path.join(dir,f)
                    self.text_parse(key)
        with open('output_Lab2.json', 'w') as scrieJson1:
            json.dump(self.words, scrieJson1,indent=10)

  
if __name__=='__main__':
     var=TextParser(files_path)
     var.read_files()
