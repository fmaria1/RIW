import os
import collections
import json
import sys
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
opreanzi = []
operatori = []
dict_operanzi = {}
files = []
result = set()
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

def interogare(): 
    inter = input("Introduceti interogarea: ")
    word = ''
    for char in inter:
        char = char.lower()
        if (char >='a' and char <='z') or (char >='A' and char <= 'Z') or (char>='0' and char <='9'):
            word += char
        else:
            if (char == "!" or char == "&" or char == "|") and word !='':
                operatori.append(char)
                if word not in stop_words:
                    if word in exception_words:
                        opreanzi.append(word.lower())
                    else:
                        opreanzi.append(word.lower())

                else:
                    del operatori[len(operatori) - 2]
                word = ''
            else:
                sys.exit('Sirul introdus este gresit')
    if word not in stop_words:
        if word in exception_words:
            opreanzi.append(word.lower())
            word = ''
        else:
            opreanzi.append(word)
            word = ''
    if len(opreanzi) == len(operatori) and len(operatori)!=0:
        del operatori[-1]


def cautare_booleana():      
    interogare()
    for operand in opreanzi:
        if operand in file_position:
            dict_operanzi[operand] = set()
            dict_operanzi[operand] = set(file_position[operand])
    global result
    parser = 1
    try:
        result = result.union(dict_operanzi[opreanzi[0]])
    except:
        print("Cuvantul nu se gaseste in fisierele de lucru")
    for operator in operatori:
        if operator == '|':
            try:
                result = result.union(dict_operanzi[opreanzi[parser]])
            except:
                print("Cuvantul nu se gaseste in fisierele de lucru")
        elif operator == '!':
            try:
                if len(result) == 0:
                    result = result.union(dict_operanzi[opreanzi[parser]])
                else:
                    result = result.difference(dict_operanzi[opreanzi[parser]])
            except:
                print("Cuvantul nu se gaseste in fisierele de lucru")
        else:
            try:
                if len(result) == 0:
                    result = result.union(dict_operanzi[opreanzi[parser]])
                else:
                    result = result.intersection(dict_operanzi[opreanzi[parser]])
            except:
                print("Cuvantul nu se gaseste in fisierele de lucru")
        parser+=1
        
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
    cautare_booleana()  
    print("Rezultatul cautarii:")
    print(result)