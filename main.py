import re
import nltk
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from string import punctuation
from nltk.probability import FreqDist


def readAndRemoveLinks(myFile):
    f = open(myFile, "r",encoding='utf-8')
    text = re.sub(r'(?:(?:http|https):\/\/)?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', "",
                  f.read(), flags=re.MULTILINE)
    text = '\n'.join([a for a in text.split("\n") if a.strip()])

    writeTo = open("demofile2.txt", "a", encoding='utf-8')
    writeTo.write(text)
    writeTo.close()

#chose randomly 85 product with x romanian comments
def getRomanianComments(writeTo):
    with open(writeTo,encoding='utf-8') as myfile:
        firstNlines=myfile.readlines()[0:85]
    return firstNlines

#calling functions
readAndRemoveLinks("all_comments.txt")
list_to_be_analyzed = getRomanianComments("demofile2.txt")

#write comments to file
with open('list_to_be_analyzed.txt', 'w', encoding='utf-8') as f:
    for item in list_to_be_analyzed:
        f.write("%s\n" % item)

#split the whitespace and separate punctuation with a regex
def getTextNoPunctuation(file_input):
    pattern = r'[a-z]+[@][a-z]+\.[a-z]+\.*[a-z]*|' \
              r'http?:\/\/[a-z]+\.[a-z]+\.*[a-z]*/*[a-z]*/*[a-z]*\.*[html]*|' \
              r'\d+\.\d+\.\d+\.\d+|[Mm][RrSs][Ss]*\.[ ]*[a-zA-Z]+|' \
              r'\w+|' \
              r'[^\w\s]'
    tokeniser = RegexpTokenizer(pattern)
    list_tokens = list()
    with open(file_input, 'r', encoding='utf-8') as file_in:
        lines = file_in.readlines()
        for line in lines:
            list_tokens += tokeniser.tokenize(line)
    return list_tokens

#lemmatization
def getLemmatization(list_tokens):
    wnl = WordNetLemmatizer()
    list_lemmas = list()
    for token in list_tokens:
        list_lemmas.append(wnl.lemmatize(token))
    return list_lemmas

#save punctuation from input
def getPunctuation():
    return ''.join([p for p in punctuation if p not in ('@', '.', ':', '/')])

#read from file and save to another one without punctuation at all
def getSeparatePunctiation(file_input, file_output):
    file_out = open(file_output, 'w', encoding='utf-8')
    with open(file_input, 'r', encoding='utf-8') as file_in:
        lines = file_in.readlines()
        for line in lines:
            line_without_punctuation = ''.join([letter for letter in line if letter not in getPunctuation()])
            file_out.write(line_without_punctuation)

#function call
getSeparatePunctiation('list_to_be_analyzed.txt', 'corpus_without_punctuation.txt')

#part of speech tagger
def getPartOfSpeech(list_lemmas):
    return nltk.pos_tag(list_lemmas)

#get most frequent word
def getMostFrecvWords(list_pos_tags, top):
    words = [word for (word, tag) in list_pos_tags]
    freq_dist = FreqDist(words)
    return freq_dist.most_common(top)

#most frequest part of speech tags
def getMostFrecvPartOfSpeech(list_pos_tags, top):
    tags = [tag for (word, tag) in list_pos_tags]
    freq_dist = FreqDist(tags)
    return freq_dist.most_common(top)



noPunct = getTextNoPunctuation('corpus_without_punctuation.txt')
lemma = getLemmatization(noPunct)
part_of_speech = getPartOfSpeech(lemma)
frecv_word= getMostFrecvWords(part_of_speech, 15)
frecv_part_of_speech = getMostFrecvPartOfSpeech(part_of_speech, 15)





