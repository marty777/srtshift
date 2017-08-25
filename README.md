# srtshift
Python 3 command line app to fix misaligned timecodes on SubRib .srt subtitle files

## srtshift
	
Shifts all timecodes in the file by a constant specified amount

	usage: srtshift.py [-h] [--outfile OUTFILE] [--timeshift TIMESHIFT] inputfile

	positional arguments:
		inputfile			Your source .srt file

	optional arguments:
		-h, --help			show this help message and exit
		
		--outfile OUTFILE		A destination .srt file. If not provided, output will
						be dumped to stdout
		--timeshift TIMESHIFT
						The number of milliseconds, positive or negative, to
						shift all timecodes in the input file.
						
#srtscale

Intended to be used in cases when subtitles and video drift out of alignment over time (for example, if the framerate of the video file is slightly different lower or higher than the source of the subtitles). Locate two timecodes, ideally near the start and end of the video, and specify their current and desired times. Somewhat inaccurate for large changes.

usage: srtscale.py [-h] [--outfile OUTFILE] [--timecode1curr TIMECODE1CURR]
                   [--timecode1new TIMECODE1NEW]
                   [--timecode2curr TIMECODE2CURR]
                   [--timecode2new TIMECODE2NEW]
                   inputfile

	positional arguments:
	  inputfile             Your source .srt file

	optional arguments:
	  -h, --help            show this help message and exit
	  --outfile OUTFILE     	A destination .srt file. If not provided, output will
						be dumped to stdout
	  --timecode1curr TIMECODE1CURR
						A timecode (in the format HH:MM:SS,MMM) near the start
						of the existing .srt file
	  --timecode1new TIMECODE1NEW
						The desired timecode (in the format HH:MM:SS,MMM) that
						TIMECODE1CURR should be updated to in the output file
	  --timecode2curr TIMECODE2CURR
						A timecode (in the format HH:MM:SS,MMM) near the end
						of the existing .srt file
	  --timecode2new TIMECODE2NEW
						The desired timecode (in the format HH:MM:SS,MMM) that
						TIMECODE2CURR should be updated to in the output file
