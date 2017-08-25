
##	srtsclae.py
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
	if milliseconds < 0:
		milliseconds = 0
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
	
def timestamp(string):
	if not is_timestamp(string):
		msg = "%r is not a timestamp in the format HH:MM:SS,MMM (eg: 01:10:25,220)" % string
		raise argparse.ArgumentTypeError(msg)
	return parse_timestamp(string)

def outfunc(outhandle, outstring):
	if outhandle == False:
		print(outstring, end='')
	else:
		outhandle.write(outstring)


def adjust_timestamp(timestamp, a, b):
	return timestamp + int(a + timestamp*b)
	
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', type=argparse.FileType('r'),
						help='Your source .srt file')
	parser.add_argument('--outfile', default=False, type=argparse.FileType('w'),
						help='A destination .srt file. If not provided, output will be dumped to stdout')
	parser.add_argument('--timecode1curr', default=0, type=timestamp,
						help='A timecode (in the format HH:MM:SS,MMM) near the start of the existing .srt file')
	parser.add_argument('--timecode1new', default=0, type=timestamp,
						help='The desired timecode (in the format HH:MM:SS,MMM) that TIMECODE1CURR should be updated to in the output file')
	parser.add_argument('--timecode2curr', default=0, type=timestamp,
						help='A timecode (in the format HH:MM:SS,MMM) near the end of the existing .srt file')
	parser.add_argument('--timecode2new', default=0, type=timestamp,
						help='The desired timecode (in the format HH:MM:SS,MMM) that TIMECODE2CURR should be updated to in the output file')

	args = parser.parse_args()

	if (args.timecode1curr and not args.timecode1new) or (not args.timecode1curr and args.timecode1curr):
		parser.error("both TIMECODE1CURR and TIMECODE1NEW are required")
		return 0
	if (args.timecode2curr and not args.timecode2new) or (not args.timecode2curr and args.timecode2curr):
		parser.error("both TIMECODE2CURR and TIMECODE2NEW are required")
		return 0
	
	millis_const = 0
	millis_coefficient = 0.0
	
	
	if args.timecode1curr and not args.timecode2curr:
		millis_const = args.timecode1new - args.timecode1curr
	elif args.timecode2curr and not args.timecode1curr:
		millis_const = args.timecode2new - args.timecode2curr
	elif args.timecode1curr and args.timecode2curr:
		
		millis_const = args.timecode1new - args.timecode1curr
		if args.timecode1curr != args.timecode2curr:
			millis_coefficient = float(args.timecode2new - args.timecode2curr - millis_const) / float(args.timecode2curr - args.timecode1curr)
	
	linebuffer = list()
	linecount = 0
	
	for line in args.inputfile:
		linecount += 1
		if len(line.strip()) == 0:
			outfunc(args.outfile, linebuffer[0])
			timestamps = linebuffer[1].split(' --> ')
			if len(timestamps) != 2 or not is_timestamp(timestamps[0]) or not is_timestamp(timestamps[1]) :
				sys.exit('Error around line ' + str(linecount) +': Could not parse '+linebuffer[1]+' as timestamps')
			outfunc(args.outfile, format_timestamp(adjust_timestamp(parse_timestamp(timestamps[0]), millis_const, millis_coefficient)) + ' --> ' + format_timestamp(adjust_timestamp(parse_timestamp(timestamps[1]), millis_const, millis_coefficient)) + '\n')
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
		outfunc(args.outfile, format_timestamp(adjust_timestamp(parse_timestamp(timestamps[0]), millis_const, millis_coefficient)) + ' --> ' + format_timestamp(adjust_timestamp(parse_timestamp(timestamps[1]), millis_const, millis_coefficient)) + '\n')
		for i in range(2, len(linebuffer)):
			outfunc(args.outfile, linebuffer[i])
		outfunc(args.outfile, '\n')
		
	args.inputfile.close()
	if(args.outfile):
		print ('Complete. ' + str(linecount) + ' lines processed')
		args.outfile.close()


sys.exit(main())