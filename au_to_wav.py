from pydub import AudioSegment
import os
import requests
import json
import glob

AudioSegment.ffmpeg = "C:\\Users\\Wyndham\\Desktop\\Fall2019\\ffmpeg\\bin\\ffmpeg.exe"

def main():
	folder = input("Folder name: ")
	bluesPath = 'C:\\Users\\Wyndham\\Desktop\\Fall2019\\CS6220\\project\\data\\' + folder + '\\'
	bluesFiles = os.listdir(bluesPath)
	print(bluesFiles)
	for song in bluesFiles:
		songpath = bluesPath + song	
		if song[-3:] == 'wav':
			print(song, "already a wav file")
			continue
		elif song[-2:] == 'au':
			print("converting",song)
			s = AudioSegment.from_file(songpath,'au')
			s.export(songpath[:-2]+"wav",format='wav')
		else:
			print(song, 'not a song / format i dont care about')
			

if __name__ == "__main__":
	main()