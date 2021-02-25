import pygame
import requests
from time import sleep

test_url = 'https://archive.org/download/PinkFloyd07CarefullWithThatAxeEugene/02%20-%20Learning%20To%20Fly.mp3'
		
class myfile(object):
	def __init__(self,url):
		self.url = url
		self.file = ''
		self.pos = 0
		self.chunk_gen = self.stream()
		
	def stream(self):
		r = requests.get(self.url, stream=True)
		for chunk in r.iter_content(chunk_size=40972):		
			if chunk:
				self.file+=chunk
				yield

	def read(self,*args):
		size = args[0]	
		while self.pos+size>len(self.file):
			try:
				self.chunk_gen.next()
			except StopIteration:
				break			
			print 'have %d bytes, wants %d bytes(diff: %d)'%(len(self.file),self.pos+size,len(self.file)-self.pos+size)
		if len(args)>0:
			ret = self.file[self.pos:self.pos+size]
			self.pos+=size
			return ret
			

if __name__ == "__main__":
	pygame.mixer.init()
	fi = myfile(test_url)
	pygame.mixer.music.load(fi)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		sleep(1)