#!/usr/bin/python
# coding=utf-8

import os.path
import random
import numpy

def strip_non_ascii(string):
	''' Returns the string without non ASCII characters'''
	stripped = (c for c in string if 0 < ord(c) < 127)
	return ''.join(stripped)

def scrambled(orig):
	dest = orig[:]
	random.shuffle(dest)
	return dest

class Analysis:
	def __init__(self, filename):
		self.filename = filename
		tmp_f = open(self.filename, 'r')
		self.s = tmp_f.read()
		tmp_f.close()
		self.cleaned = [ n.lower() for n in strip_non_ascii(self.s).replace("\n","").split(" ") ]
		self.unique_words = list(set(self.cleaned))
		# Now generate an array of len(self.unique_words) X len(self.unique_words)
		# to contain the probability of each word being followed by another word.
		self.t = len(self.unique_words)
	def load(self):
		""" Loads data from the filename """
		npfile = self.filename.replace('.txt','')
		if os.path.isfile(npfile+'_appearances.npy'):
			self.probabilities = numpy.load(npfile+'_probabilities.npy')
		else:
			self.appearances = numpy.zeros( (self.t, self.t) )
			self.probabilities = numpy.zeros( ( self.t, 100 ) )
			print 'Counting...'
			self.count()
			print 'Normalizing...'
			self.normalize()
			self.generate_probabilities()
			numpy.save(npfile+'_probabilities', self.probabilities)
	def count(self):
		cleaned_t = len(self.cleaned)
		h = 0
		for i, word in enumerate(self.unique_words):
			h += 1
			if h%1000 == 0:
				print h
			for j, word_tmp in enumerate(self.cleaned):
				# If it is the last one then just skip it
				if j == (cleaned_t - 1):
					continue
				if self.unique_words[i] == self.cleaned[j]:
					# Find the index of the next word and increase its counter by 1.
					self.appearances[i][ self.unique_words.index( self.cleaned[j + 1] ) ] += 1
	def normalize(self):
		for i in range(self.t):
			total = sum(self.appearances[i])
			total = total if total > 0.0 else 1.0
			# print total
			for j in range(self.t):
				try:
					self.appearances[i][j] /= total
				except:
					print self.appearances[i][j]
					print total
	def generate_probabilities(self):
		for i in range(self.t):
			k = 0
			for j in range(self.t):
				if self.appearances[i][j] != 0.0:
					tmp = int(self.appearances[i][j]*100)
					tmp = tmp if tmp != 100 else 99
					for l in range(tmp):
						self.probabilities[i][k] = j
						k += 1
						k = k if k != 100 else 99
	def obtain_word(self, i):
		k = int( random.random() * 100 )
		k = k if k != 100 else 99
		return self.unique_words[ int(self.probabilities[int(i)][int(k)]) ], self.probabilities[int(i)][int(k)]
	def speak(self, n, start = None):
		if not start:
			k = int( self.t * random.random() )
			k = k if k != self.t else self.t-1
			start = self.unique_words[k]
		if start not in self.unique_words:
			print 'The word must exists in the list of words'
		final = []
		current_word = start
		current_index = self.unique_words.index(start)
		for i in range(n):
			final.append(current_word)
			current_word = ''
			i = 0
			while current_word == '':
				i += 1
				new_word, new_index = self.obtain_word(current_index)
				current_word = new_word
				if current_word in final:
					current_word = ''
				if current_word == 'system':
					current_word = ''
				if current_word != '':
					current_index = new_index
				if i % 20 == 0:
					i = 1
					current_index = new_index
		return ' '.join(final)
	def speakZarathustra(self, n, start = None):
		return self.speak(n, start)


Niet = Analysis('data/antichrist.txt')