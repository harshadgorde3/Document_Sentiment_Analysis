import nltk
import ast
import re
import string
import numpy as npy
import matplotlib.pyplot as pPlot
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
from wordcloud import WordCloud, STOPWORDS
from PIL import Image


def removeStopwords(inputFilePath, outputFilePath, printResult):
    inputFile = open(inputFilePath, "r", encoding='utf-8').read()
    outputFile = open (outputFilePath, "w+", encoding='utf-8')
    cachedStopWords = nltk.corpus.stopwords.words("english")
    cachedStopWords.append('OMG')
    cachedStopWords.append(':-)')
    result = (' '.join([word for word in inputFile.split() if word not in cachedStopWords]))

    if(printResult):
        print('\nBELOW IS THE LIST OF STOP WORDS:')
        print(cachedStopWords)
        print("\n\nFOLLOWING IS THE TEXT WITHOUT STOPWORDS:")
        print(str(result))
    outputFile.write(str(result))
    outputFile.close()
	
def tokenizeData(inputFilePath, outputFilePath, printResult):
    tokenizedData = {}
    inputFile = open(inputFilePath, "r", encoding='utf-8').read()
    outputFile = open(outputFilePath, "w")
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    count = 1;
    cachedStopWords = nltk.corpus.stopwords.words("english")

    for sentence in tokenizer.tokenize(inputFile):      
        tokenizedData[count] = sentence
        count+=1

    outputFile.write(str(tokenizedData))
    
    if(printResult):
        for key,value in tokenizedData.items():
            print(key,' ',value)
    outputFile.close()
	
def tagWord(inputFilePath, outputFilePath, printResult):
    inputFile = open(inputFilePath, "r").read()
    outputFile = open(outputFilePath, "w")
    inputTupples = ast.literal_eval(inputFile)
    outputPost = {}

    for key,value in inputTupples.items():
        outputPost[key] = nltk.pos_tag(nltk.word_tokenize(value))
        
    if(printResult):
        for key,value in outputPost.items():
            print(key, ' ', value)
    outputFile.write(str(outputPost))
    outputFile.close()
	
def extractAspects(inputFilePath, outputFilePath, printResult):
    inputFile = open(inputFilePath, "r").read()
    outputFile = open(outputFilePath, "w")
    inputTupples = ast.literal_eval(inputFile)
    prevWord = ''
    prevTag = ''
    currWord = ''
    aspectList = []
    outputDict = {}
    #Extracting Aspects
    for key,value in inputTupples.items():
        for word,tag in value:
            if(tag=='NN' or tag=='NNP'):
                if(prevTag=='NN' or prevTag=='NNP'):
                    currWord = prevWord + ' ' + word
                else:
                    aspectList.append(prevWord.upper())
                    currWord= word

            prevWord = currWord
            prevTag = tag
    #Eliminating aspect which has 1 or less count
    for aspect in aspectList:
            if(aspectList.count(aspect) > 1):
                    if(outputDict.keys() != aspect):
                            outputDict[aspect] = aspectList.count(aspect)
    outputAspect = sorted(outputDict.items(), key = lambda x: x[1], reverse = True)
    if(printResult):
        print(outputAspect)
    outputFile.write(str(outputAspect))
    outputFile.close()
	
def displayGraph(inputFilePath, printResult):
    inputFile = open(inputFilePath, "r").read()
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = inputFile.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.tokenize.word_tokenize(cleaned_text)
    fd = nltk.FreqDist(tokens)
	
    if(printResult):
        fd.plot(30,cumulative=False)
	
	
def identifyOpinionWords(inputReviewListStr, inputAspectListStr, outputAspectOpinionListStr, printResult):       
    inputReviewList = open(inputReviewListStr, "r").read()
    inputAspectList = open(inputAspectListStr, "r").read()
    outputAspectOpinionList = open(outputAspectOpinionListStr, "w")
    inputReviewsTuples = ast.literal_eval(inputReviewList)
    inputAspectTuples = ast.literal_eval(inputAspectList)
    outputAspectOpinionTuples = {}
    orientationCache = {}
    negativeWordSet = {"don't", "never", "nothing", "nowhere", "noone", "none", "not",
                  "hasn't", "hadn't", "can't", "couldn't", "shouldn't", "won't",
                  "wouldn't", "don't", "doesn't", "didn't", "isn't", "aren't", "ain't"}

    for aspect,no in inputAspectTuples:
        aspectTokens = word_tokenize(aspect)
        count = 0
        for key,value in inputReviewsTuples.items():
            condition = True
            isNegativeSen = False
            for subWord in aspectTokens:
                if(subWord in str(value).upper()):
                    condition = condition and True
                else:
                    condition = condition and False

            if(condition):
                for negWord in negativeWordSet:
                    if(not isNegativeSen):#once senetence is negative no need to check this condition again and again
                        if negWord.upper() in str(value).upper():
                            isNegativeSen = isNegativeSen or True

                outputAspectOpinionTuples.setdefault(aspect, [0,0,0])

                for word,tag in value:

                     if(tag=='JJ' or tag=='JJR' or tag=='JJS'or tag== 'RB' or tag== 'RBR'or tag== 'RBS'):
                         count+=1
                         if(word not in orientationCache):
                             orien = orientation(word)
                             orientationCache[word] = orien
                         else:
                             orien = orientationCache[word]
                         if(isNegativeSen and orien is not None):
                             orien= not orien
                         if(orien == True):
                             outputAspectOpinionTuples[aspect][0]+=1
                         elif(orien == False):
                             outputAspectOpinionTuples[aspect][1]+=1
                         elif(orien is None):
                             outputAspectOpinionTuples[aspect][2]+=1
        if(count > 0):
            #print(aspect,' ', outputAspectOpinionTuples[aspect][0], ' ',outputAspectOpinionTuples[aspect][1], ' ',outputAspectOpinionTuples[aspect][2])
            outputAspectOpinionTuples[aspect][0] = round((outputAspectOpinionTuples[aspect][0]/count)*100, 2)
            outputAspectOpinionTuples[aspect][1] = round((outputAspectOpinionTuples[aspect][1]/count)*100, 2)
            outputAspectOpinionTuples[aspect][2] = round((outputAspectOpinionTuples[aspect][2]/count)*100, 2)
            print(aspect, ':\t\tPositive => ', outputAspectOpinionTuples[aspect][0], '\tNegative => ',outputAspectOpinionTuples[aspect][1], '\tFinal =>', outputAspectOpinionTuples[aspect][2])
    if(printResult):
        print('')
    outputAspectOpinionList.write(str(outputAspectOpinionTuples))
    outputAspectOpinionList.close();
    
    
def createWordCloud(inputFilePath, printResult):
   inputFile = open(inputFilePath, "r").read()
   dataset = inputFile.lower()
   maskArray = npy.array(Image.open("cloud.png"))
   cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray, stopwords = set(STOPWORDS))
   cloud.generate(dataset)
   cloud.to_file("wordCloud.png")
   
   if(printResult):
       img = Image.open("wordCloud.png")
       img.show()

#-----------------------------------------------------------------------------------

def orientation(inputWord): 
    wordSynset = wordnet.synsets(inputWord)
    if(len(wordSynset) != 0):
        word = wordSynset[0].name()
        orientation = sentiwordnet.senti_synset(word)
        if(orientation.pos_score() > orientation.neg_score()):
            return True
        elif(orientation.pos_score() < orientation.neg_score()):
            return False
            
