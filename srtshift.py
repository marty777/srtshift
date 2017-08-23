
##	srtshift.py
##	Martin Thorne, August 2017
##	A quick program to adjust timestamps in .srt SubRip subtitle files. Timestamps can be
##	adjusted by a constant amount, or with a linear modification if the subtitle file and 
##	corresponding video file assume slightly different framerates and drift over time.

import argparse
import sys

def parse_timestamp(timestamp):
	hours = int(timestamp[0:2])
	minutes = int(timestamp[3:5])
	seconds = int(timestamp[6:8])
	millis = int(timestamp[9:12])
	return (hours * 3600000) + (minutes * 60000) + (seconds * 1000) + millis
	
def format_timestamp(milliseconds):
	hours = int(milliseconds / 3600000)
	milliseconds -= hours * 3600000
	minutes = int(milliseconds / 60000)
	milliseconds -= minutes * 60000
	seconds = int(milliseconds / 1000)
	milliseconds -= seconds * 1000	
	return "%02d:%02d:%02d,%03d" % (hours, minutes, seconds, milliseconds, )

def is_timestamp(string):
	if len(string) < 12 or string[2] != ':' or string[5] != ':' or string[8] != ',' or not (string[0:2].isdigit() and string[3:5].isdigit() and string[6:8].isdigit() and string[9:12].isdigit()): 
		return False
	return True

def outfunc(outhandle, outstring):
	if outhandle == False:
		print(outstring, end='')
	else:
		outhandle.write(outstring)
	
parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=argparse.FileType('r'),
					help='Your source .srt file')
parser.add_argument('--outfile', default=False, type=argparse.FileType('w'),
					help='A destination .srt file. If not provided, output will be dumped to stdout')
parser.add_argument('--timeshift', default=0, type=int,
					help='The number of milliseconds, positive or negative, to shift all timecodes in the input file.')

args = parser.parse_args()

millis = args.timeshift
linebuffer = list()
linecount = 0

for line in args.inputfile:
	linecount += 1
	if len(line.strip()) == 0:
		outfunc(args.outfile, linebuffer[0])
		timestamps = linebuffer[1].split(' --> ')
		if len(timestamps) != 2 or not is_timestamp(timestamps[0]) or not is_timestamp(timestamps[1]) :
			sys.exit('Error around line ' + str(linecount) +': Could not parse '+linebuffer[1]+' as timestamps')
		outfunc(args.outfile, format_timestamp(parse_timestamp(timestamps[0]) + millis) + ' --> ' + format_timestamp(parse_timestamp(timestamps[1]) + millis) + '\n')
		for i in range(2, len(linebuffer)):
			outfunc(args.outfile, linebuffer[i])
		outfunc(args.outfile, '\n')
		del linebuffer[:]
		
	else:
		linebuffer.append(line)

#clear any remaining lines in buffer
if len(linebuffer) > 1:
	outfunc(args.outfile, linebuffer[0])
	timestamps = linebuffer[1].split(' --> ')
	if len(timestamps) != 2 or not is_timestamp(timestamps[0]) or not is_timestamp(timestamps[1]) :
		sys.exit('Error around line ' + str(linecount) +': Could not parse '+linebuffer[1]+' as timestamps')
	outfunc(args.outfile, format_timestamp(parse_timestamp(timestamps[0]) + millis) + ' --> ' + format_timestamp(parse_timestamp(timestamps[1]) + millis) + '\n')
	for i in range(2, len(linebuffer)):
		outfunc(args.outfile, linebuffer[i])
	outfunc(args.outfile, '\n')
	
args.inputfile.close()
if(args.outfile):
	print ('Complete. ' + str(linecount) + ' lines processed with a timestamp shift of ' + str(millis) + ' milliseconds')
	args.outfile.close()
