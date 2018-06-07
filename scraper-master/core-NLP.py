from pynlp import StanfordCoreNLP as ner_NLP
from stanfordcorenlp import StanfordCoreNLP
from nltk import sent_tokenize
import json,sys
from pymongo import MongoClient
import datetime

def parseSentence(sentence):
    annotators = 'tokenize, ssplit, pos, lemma, ner'
    sentences = sent_tokenize(sentence)

    options = {'openie.resolve_coref': True}

    nlp1 = ner_NLP(annotators=annotators, options=options)
    ret = []
    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
    for i,sentence in enumerate(sentences):
        store = {}
        store["sentence_id"] = i
        store["sentence"] = sentence

        document = nlp1(sentence.encode('utf-8'))

        first_sentence = document[0]
        ner = {}
        for entity in first_sentence.entities:
            #print(entity, '({})'.format(entity.type))
            ner[entity.type] = ner.get(entity.type, []) + [str(entity)]

        #print ('Tokenize:', nlp.word_tokenize(sentence))
        #print ('Constituency Parsing:', nlp.parse(sentence))
        store["parse_sentence"] = nlp.parse(sentence)
        store["token"] = ",".join(nlp.word_tokenize(sentence))
        store["ner"] = ner
        ret.append(store)
    return ret
client = MongoClient('localhost:27017')
db = client.event_scrape
print("Started")
actCol = db.stories.find()
print("IN")
file = open("parsedData.txt","w")
i=0
for st in actCol:
    if(i>20):
        break
    i+=1
    data = {}
    data["type"]="story"
    data["doc_id"]= st['source']+str(datetime.datetime.utcnow())
    data["head_line"]= st['title']
    data["date_line"]= st['date']
    data["sentences"]= parseSentence(st['content'])
    final = json.dumps(data)
    print("*****************************************************")
    print (final)
    file.write(str(final)+"\n")
    print("*****************************************************")
