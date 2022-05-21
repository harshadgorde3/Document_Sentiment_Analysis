
Document Sentiment Analysis using Opinion Mining

1) Install nltk.
	Run command => pip3 install nltk  - using administrator privileges
2) now download below nltk corpora i.e. datasets
	>>> import nltk
	>>> nltk.download('stopwords')
	>>> nltk.download('punkt')
	>>> nltk.download('averaged_perceptron_tagger')
	>>> nltk.download('wordnet')
	>>> nltk.download('sentiwordnet')
	
3)  corpora - sentiwordnet, stopwords, wordnet
	taggers - averaged_perceptron_tagger
	tokenizers - punkt
	
4) for word cloud, these libraries need to be downloaded:
	>pip3 install matplotlib
	>pip3 install wordcloud