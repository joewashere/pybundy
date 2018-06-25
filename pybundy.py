
#! /usr/bin/python
# File name: pybundy.py
# Author: Joe Burton
# Date created: 6/24/18
# Date last modified: 6/24/18
# Python Version: 3.6

import json
import os
import sys
from colorama import init
from css_html_js_minify import js_minify, css_minify

init()

#Creates function to output my error messages with color
def error_output(error, data):
	print('\x1b[2;31;40m' + error + '\x1b[0m' + data)

#Creates function to output my success messages with color
def success_msg(msg, data):
	print('\x1b[1;32;40m' + msg + '\x1b[0m' + data)


#Function that handles the bundling
def bundle():

	#Check to see if output files exist, if so remove them
	if os.path.exists(cssoutput):
		os.remove(cssoutput)

	if os.path.exists(jsoutput):
		os.remove(jsoutput)

	#This part is a WIP. Please don't judge too hard. Trying to look through node_modules to find javascript and css files in packages specified in the config.		
	for module in modules:
		fullpath = './node_modules/' + module

		#This one checks if the node module exists or can be found
		if os.path.exists(fullpath):

			#Created a couple different paths to look for
			myfile = fullpath + '/dist/js/'+module+'.min.js'
			myfile2 = fullpath + '/dist/' + module + '.min.js'

			#Check if file exists, if found it performs same bundling operation as the javascript one documented below.
			if os.path.exists(myfile):
				output = "//FILE OUTPUT FROM: " + myfile + "\n"
				#output += js_minify(str(f.read()))
				os.makedirs(os.path.dirname(jsoutput), exist_ok=True)
				with open (myfile, 'r') as mf:
					with open(jsoutput, 'a+') as out:
						for line in mf:
							out.write(line)
				success_msg('Processed: ', myfile)
			#Performing check of second directory	
			elif os.path.exists(myfile2):
				f = open(myfile2, "r")
				output = "//FILE OUTPUT FROM: " + myfile2 + "\n"
				output += js_minify(str(f.read()))
				os.makedirs(os.path.dirname(jsoutput), exist_ok=True)
				with open(jsoutput, 'a+') as out:
					out.write(output+'\n\n')
				f.close()
				success_msg('Processed: ', myfile2)
			else:
				#Lets user know both directories checked on fail.
				error_output('File not found: ', myfile)
				error_output('Also checked: ', myfile2)
		else:
			#Error when node module not found
			error_output('Node module could not be located: ', fullpath)

		checkcss = fullpath + '/dist/css/' + module + '.min.css'
		if os.path.exists(checkcss):
			f = open(checkcss, "r")
			output = "/*FILE OUTPUT FROM: " + checkcss + "*/\n"
			output += css_minify(str(f.read()))
			os.makedirs(os.path.dirname(cssoutput), exist_ok=True)
			with open(cssoutput, 'a+') as out:
				out.write(output+'\n\n')
			f.close()
			success_msg('Processed: ', checkcss)

	#loops through the javascript files specified in config
	for file in jsfiles:

		#create full path using js path in config
		fullpath = jspath + file

		if os.path.exists(fullpath):
			#Check to see if file exists, on success open file, minify, and append to output specified in config. Close files
			f = open(fullpath, "r")
			output = "//FILE OUTPUT FROM: " + fullpath + "\n"
			output += js_minify(str(f.read()))
			os.makedirs(os.path.dirname(jsoutput), exist_ok=True)
			with open(jsoutput, 'a+') as out:
				out.write(output+'\n\n')
			f.close()
			success_msg('Processed: ', fullpath)
		else:
			#File not found
			error_output('File not found: ', fullpath)

		#See if any paths were provided to be forced into bundle
	if forcejs:
		#Loop through paths
		for fullpath in forcejs:
			#Check if they exist
			if os.path.exists(fullpath):
				#Run file tasks
				f = open(fullpath, "r")
				output = "//FILE OUTPUT FROM: " + fullpath + "\n"
				output += js_minify(str(f.read()))
				os.makedirs(os.path.dirname(jsoutput), exist_ok=True)
				with open(jsoutput, 'a+') as out:
					out.write(output+'\n\n')
				f.close()
				success_msg('Processed: ', fullpath)
			else:
				error_output('File not found: ', file)


	#This works identically to the javascript loop. Just uses the css vars from the config.
	for file in cssfiles:
		fullpath = csspath + file
		if os.path.exists(fullpath):
			f = open(fullpath, "r")
			output = "/*FILE OUTPUT FROM: " + fullpath + "*/\n" 
			output += css_minify(str(f.read()))
			os.makedirs(os.path.dirname(cssoutput), exist_ok=True)
			with open(cssoutput, 'a+') as out:
				out.write(output+'\n\n')
			f.close()
			success_msg('Processed: ', fullpath)
		else:
			error_output('File not found: ', fullpath)

	#Same as JS one
	if forcecss:
		for fullpath in forcecss:
			if os.path.exists(fullpath):
				f = open(fullpath, "r")
				output = "//FILE OUTPUT FROM: " + fullpath + "\n"
				output += css_minify(str(f.read()))
				os.makedirs(os.path.dirname(cssoutput), exist_ok=True)
				with open(cssoutput, 'a+') as out:
					out.write(output+'\n\n')
				f.close()
				success_msg('Processed: ', fullpath)
			else:
				error_output('File not found: ', file)


	

#Check to see if config file is in same directory
if os.path.exists('./pybundy.config.json'):
	#There's got to be a better way to do this [1]
	forcecss = ""
	forcejs = ""

	#If so, open config
	with open('./pybundy.config.json') as json_data:
		#Load json data into var
		d = json.load(json_data)

		#Assign variables from json config
		jspath = d['pybundy']['js']['path']
		jsfiles = d['pybundy']['js']['files']
		jsoutput = d['pybundy']['js']['output']
		csspath = d['pybundy']['css']['path']
		cssfiles = d['pybundy']['css']['files']
		cssoutput = d['pybundy']['css']['output']
		modules = d['pybundy']['modules']

		#[1] Trying to find a better way to check if array isnt passed in config
		if d['pybundy']['css'].get('force'):
			forcecss = d['pybundy']['css'].get('force')
		if d['pybundy']['js'].get('force'):
			forcejs = d['pybundy']['js'].get('force')

		#calls main function
		bundle()
else:
	#no config found
	error_output('Error: No configuration file found', 'pybundy.config.json')

