import sentimentFunctions

def printResult():
    choice = str(input('\nPrint the result on console? (Y/N):'))
    if(choice=='Y' or choice=='y'):
        return True
    else:
        return False

_Path = 'C:/Users/hgorde/OneDrive - Omniscient Software Pvt. Ltd/yHarshad/Project/Document Sentiment Analysis/datafiles//'
_FolderName='C:\Data\iPhone12\\'
#_Dataset = _Path + 'iPhone12ReviewDataset.txt'
#_Dataset = _Path + 'ZeroMovieReviewDataset.txt'
_Dataset = _Path + 'SquidGameReviewDataset.txt'
_PreprocessedData = _Path + '1.PreprocessedData.txt'
_TokenizedData = _Path + '2.TokenizedData.txt'
_PosTaggedWords = _Path + '3.PosTaggedWords.txt'
_NounAspects = _Path + '4.NounAspects.txt'
_FinalOpinions = _Path + '5.FinalOpinions.txt'


print("\n\n\n\n\n\nPRE-PROCESSING DATA TO REMOVE STOPWORDS...")
sentimentFunctions.removeStopwords(_Dataset, _PreprocessedData, printResult())


print("\n\n\n\nDOCUMENT IS CONVERTED INTO NUMBERED SENTENCES...")
sentimentFunctions.tokenizeData(_Dataset, _TokenizedData, printResult())


print("\n\n\nALL WORDS FROM ABOVE SENTENCES ARE ASSIGNED A PART OF SPEECH TAG...")
sentimentFunctions.tagWord(_TokenizedData, _PosTaggedWords, printResult())

print("\n\n\nALL THE NOUNS WILL BE LISTED AS ASPECTS...")
sentimentFunctions.extractAspects(_PosTaggedWords, _NounAspects, printResult())

print("\n\n\nMOST OCCURRED WORDS FROM THIS DOCUMENT AND THEIR RESPECTIVE COUNTS WILL BE SHOWN GRAPHICALLY...")
sentimentFunctions.displayGraph(_PreprocessedData, printResult())

print("\n\n\n\n\n\nIDENTIFYING THE OPINION WORDS...")
sentimentFunctions.identifyOpinionWords(_PosTaggedWords, _NounAspects, _FinalOpinions, printResult())

print("\n\n\n\n\n\nSHOWING WORD CLOUD GENERATED FROM ABOVE DATA...")
sentimentFunctions.createWordCloud(_TokenizedData, printResult())
