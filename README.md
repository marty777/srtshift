# srtshift
Python 3 command line app to fix misaligned timecodes on SubRib .srt subtitle files

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