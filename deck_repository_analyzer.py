#!/usr/bin/env python
#coding=utf-8

import os
import sys
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt


""" 
Comparator Tool, author: photon79

"""

def shellquote(s):	# treat white space in strings, applied to path names
    return "'" + s.replace("'", "'\\''") + "'"

def create_nl(directory):
	for item in (os.path.join(directory,item) for item in os.listdir(directory)
		if not item.startswith('.')):
	        if os.path.isdir(item): create_nl(item)
        	elif os.path.isfile(item):
			if "Runner" in item: nl_r.append(item)
			else: nl_c.append(item)

def create_dl():	# creates lists dl_c and dl_r of decks
	for i in range(len(nl_c)):	
		with open(nl_c[i]) as fpointer:
			dl_c.append(convert_to_percentage(extract_card_list(fpointer.read())))
	for i in range(len(nl_r)):	
		with open(nl_r[i]) as fpointer:
			dl_r.append(convert_to_percentage(extract_card_list(fpointer.read())))

def convert_to_percentage(card_list):	# converts the card numbers into relative frequencies
	newlist = {}
	count = 0.0
	for key in card_list.keys(): count += card_list[key]		
	for key in card_list.keys(): newlist[key] = round((card_list[key]/count), 3)
	return newlist		

def extract_card_list(deck):		# reads each file and makes a dict out of the card list
	card_list = {}
	for line in deck.split("\n"): 
		line = line.strip() 	# Clean any leading or trailing spaces.
		if len(line) == 0 or line[0] == "#": 
			continue	# Skip comments and blanklines
		else: 
			try:
				count, cardname = line.split(" ", 1)
				count = int(count.strip())
				cardname = cardname.strip()
				if cardname in card_list: card_list[cardname] += count
				else: card_list.update({cardname:count})
			except:	continue	# TODO print into file "Error skipped at X"
	return card_list

def distance(lista, listb):	# Bhattacharyya distance of two discrete distributions
	runningtotal = 0
	for elem in lista.keys():
		if elem in listb:
			runningtotal += round((sqrt(lista[elem])*sqrt(listb[elem])),3)
	return runningtotal

def compare_dl(deck_list):	# calculates pairwise the distance measure for a deck list
	result = []
	for i in range(len(deck_list)):
		for j in range(i+1, len(deck_list)):
			d = distance(deck_list[i], deck_list[j])
			try:
				result.append(round(float(d)*100,2))
			except:
				result.append(0.0)
	return result

def group(list):		# cuts the final distributions into intervals of percentage points
	step = 1
	max = 100/delta
	result = []
	list = sorted(list)
	for n in range(0, max):	result.append(0) # initialize nl with zeros
	i = long(0)
	while i < len(list):
		#print list[i]
		if list[i] < step*delta+0.5:	# Check!
			result[step-1] += 1 	# Check!
			i += 1
		else:	step += 1
	weight = listsum(result)
	for j in range(len(result)): result[j] = round(float(result[j]*100)/weight,2)
	return result

def listsum(list):	# sum of list entries
	result = 0
	for i in range(len(list)): result += list[i]
	return result

def average(list):
	result = 0
	for i in range(len(list)):
		result += list[i]
	return result/float(len(list))
	
if __name__ == "__main__":
	nl_c = []		# corp name list
	nl_r = []		# runner name list
	dl_c = []		# corp deck list in percentages
	dl_r = []		# runner deck list in percentages
	
	deck_dir = sys.argv[1] 	# deck directory to process
	delta = int(sys.argv[2])# percentage point intervals
	
	create_nl(deck_dir)	# initialize name lists nl_c and nl_r
	create_dl()		# create deck lists dl_c and dl_r
	
	c_c = compare_dl(dl_c)
	c_r = compare_dl(dl_r)
	g_c = group(c_c) # corp data to display
	g_r = group(c_r) # runner data to display
	
	print average(c_c)
	print average(c_r)
	print average(g_c)
	print average(g_r)

	plt.plot(g_r, 'green', g_c, 'purple') # plot data for runner and corp decks
	plt.ylabel('similarity')
	plt.show()

