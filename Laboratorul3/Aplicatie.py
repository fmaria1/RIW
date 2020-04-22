import os
import collections
import json

stop_words_path = r'stopwords'
exceptions_words_path = r'exceptions'
main_path = r'fisiere_lucru'
di_word_path = r'Direct_index.json'
exception_words = []
stop_words = []
words = {}
indirect_index = {}
file_position = {}
paths_direct_index = {}

def read_stopwords_or_exceptions(file_path,list_of_words):
    with open(file_path,'r') as file:
        word = ''
        letter = file.read(1)
        while letter != '':
            if letter != '\n':
                word += letter.lower()
            else:
                list_of_words.append(word)
                word = ''
            letter = file.read(1)

def subdirectoare():
    queue = [main_path]
    for dir in queue:
        for current in os.listdir(dir):
            if os.path.isdir(os.path.join(dir,current)):
                queue.append(os.path.join(dir,current))
            elif os.path.isfile(os.path.join(dir,current)):
                try:

                    file_path = os.path.join(dir,current)
                    print(file_path)
                    paths_direct_index[file_path] = di_word_path
                    words[file_path] = {}
                    index_direct(words[file_path],file_path)
                except Exception as e:
                    print(e)
                    pass

def index_direct(cuvinte, file_path):

    with open(file_path, 'r', encoding = "utf8",errors = 'ignore') as file:
        letter = file.read(1).lower()
        word = ''
        while letter != '':
            if letter >= 'a' and letter <= 'z' or letter >= '0' and letter <= '9':
                 word=word+letter
            else:
                if word in exception_words:
                    if word not in cuvinte:
                        cuvinte[word] = 1
                    else:
                        cuvinte[word] = cuvinte[word] + 1
                else:
                    if word != '' and word not in stop_words and len(word) > 1 :
                        if word not in cuvinte:
                            cuvinte[word] = 1
                        else:
                            cuvinte[word] = cuvinte[word] + 1
                word = ''
            letter = file.read(1).lower()


def index_indirect(cuvinte,val):
    for word in cuvinte:
        if word not in indirect_index:
            indirect_index[word] = {}
            indirect_index[word][val] = cuvinte[word]
            file_position[word] =[]
            file_position[word].append(val)
        else:
            indirect_index[word][val] = cuvinte[word]
            file_position[word].append(val)


if __name__ == "__main__":

    read_stopwords_or_exceptions(exceptions_words_path, exception_words)
    read_stopwords_or_exceptions(stop_words_path, stop_words)
    subdirectoare()
    with open('Direct_index.json', 'w') as scrieJson1:
        json.dump(words, scrieJson1, indent=10)
    with open('Direct_index_paths.json', 'w') as scrieJson2:
        json.dump(paths_direct_index, scrieJson2, indent=10) 
    with open('Direct_index_paths.json') as input1:
        direct_index = json.load(input1)
        
    for val in direct_index:
        with open(direct_index[val]) as input2:
            temp_dict= json.load(input2)[val]
        index_indirect(temp_dict,val)
    with open('Indirect_index.json', 'w') as scrieJson3:
        json.dump(indirect_index, scrieJson3, indent=10)         
        