import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
import os
import json

def main():
	#setting up data
	train_path = 'msd_genre_dataset.csv'
	train_df = pd.read_csv(train_path)
	print(train_df.head())

	#splitting metal and classical (very different, and about equal data values)
	metal_df = train_df[train_df['genre'] == 'metal']
	met_len = len(metal_df.index)
	met = [1]*met_len
	metal_df['label'] = met

	classical_df = train_df[train_df['genre'] == 'classical']
	classical_len =len(classical_df.index)
	classical = [0]*classical_len
	classical_df['label'] = classical


	frames = [metal_df, classical_df]
	df = pd.concat(frames)


	#Transform names to integers (bag of words)
	vectorizer = CountVectorizer().fit(df['artist_name'])

	#turn names into count vectors
	x = vectorizer.transform(df['artist_name'])

	y = df['label']

	xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.2)

	# instantiate the model as clf(classifier) and train it
	clf = MultinomialNB()
	clf.fit(xtrain, ytrain)
	acc = clf.score(xtest,ytest)
	print("Artist Accuracy: ", acc)

	#Our data set
	test_df = build_dataset()
	xtest = vectorizer.transform(test_df['artist_name'])
	ytest = test_df['label']
	acc = clf.score(xtest,ytest)
	print("Artist Accuracy on our dataset: ", acc)

	print('-------------------------------------')


	#Transform names to integers (bag of words)
	vectorizer = CountVectorizer().fit(df['title'])

	#turn names into count vectors
	x = vectorizer.transform(df['title'])

	xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.2)

	# instantiate the model as clf(classifier) and train it
	clf = MultinomialNB()
	clf.fit(xtrain, ytrain)
	acc = clf.score(xtest,ytest)
	print("Song Title:", acc)


	xtest = vectorizer.transform(test_df['title'])
	ytest = test_df['label']
	acc = clf.score(xtest,ytest)
	print("Song Title on our Dataset:", acc)
	print('-------------------------------------')



def build_dataset():
	fileNames = ['results_blues.txt','results_classical.txt','results_country.txt','results_disco.txt','results_hiphop.txt','results_jazz.txt','results_metal.txt','results_pop.txt','results_pop.txt','results_reggae.txt','results_rock.txt']
	fileNames = ['results_classical.txt','results_metal.txt']

	data = []
	for file in fileNames:
		f = open(file,'r')
		label = file.split('.')
		label = label[0][8:]
		Met = 0
		if label == 'metal':
			Met = 1
		elif label == 'rock':
			Met = 2
		elif label == 'pop':
			Met = 3
		elif label == 'reggae':
			Met = 4
		line = f.readline()
		while(line):
			x = line.split(":")
			songData = x[2]
			songData = songData.strip('][').split(', ') 
			song = songData[0]
			#song.replace("'","")			
			artist = songData[1]
			artist = artist[1:-1]
			#artist.replace("'","")
			if ('-' in songData[0] and file != 'results_classical.txt'):
				x = songData[0].split('-')
				artist  = x[0]
				artist = artist[1:]
				song = x[1]
				song = song[:-1]
			else:
				song = song[1:-1]

			data.append([label,artist,song,Met])
			line = f.readline()
	data = pd.DataFrame(data, columns = ['genre', 'artist_name','title','label'])
	return data


if __name__ == '__main__':
	main()
