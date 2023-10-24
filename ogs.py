from pathlib import Path
from urllib.request import urlopen
from datetime import datetime
import re
import os
import wget
import csv
from itertools import islice
import argparse

now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
ap = argparse.ArgumentParser(description='date search')
ap.add_argument('--date', action="store", dest='algo_date', default=now)
args = ap.parse_args()

print("Arguments Passed:" + args.algo_date)

furl = datetime.now().strftime("%Y") + ".csv"
url = "https://wichita.ogs.ou.edu/eq/catalog/2023/"
restr = r"\.csv\<.*(20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\s[0-9][0-9]:[0-9][0-9])"
tlog = Path("./timelog")
csvregex = r"^.*(2023-10-17\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]),([0-9]\.[0-9]),[A-Z]{1,},[a-zA-Z]{1,},([-+]?[0-9]*\.[0-9]*),([-+]?[0-9]*\.[0-9]*),.*(Oklahoma),(\D*),\w*$"

# logic outline:
# scrape page for timestamp
# check if timelog file exists
# if not, create it, write current page timestamp to it.
# if timelog exists, compare page timestamp to timelog
# if not different, quit
# if different, run remaining code to grab CSV values (TBD)

#TODO:
# Add condition to allow selecting entries based on date passed to script (std. yyyy-MM-dd hh:mm)
# or Add condition to find x most recent entries if nothing new is found.

def timelog(time):
	if DoesFileExist(tlog):
		if IsFileEmpty(tlog):
			print("file empty...writing time...")
			WriteTime(tlog,time)
			return True
		elif time == open(tlog).read():
			print("contents unchanged.")
			return False
		else:
			#if file contents not match, update with latest timestamp
			print("file outdated...updating...")
			WriteTime(tlog,time)
			return True
	else:
		print("timelog file missing...creating timelog file...")
		WriteTime(tlog,time)
		return True

def pagefetch():
	page = urlopen(url)
	html_bytes = page.read()
	html = html_bytes.decode("utf-8")
	#print(html)
	match = re.search(restr, html)
	#print(match.group(1))
	return match.group(1)

def DoesFileExist(path):
	return os.path.isfile(path)

def IsFileEmpty(path):
	return os.stat(path).st_size == 0

def WriteTime(path, time):
	f = open(path, "w")
	f.write(time)
	f.close()

def WGETfile(urlpath, fpath):
	if DoesFileExist("./" + fpath):
		print("csv exists already.")
		print(fpath)
		os.remove(fpath)
	fullpath = urlpath + fpath
	wget.download(fullpath, out="./")


# TODO CSV Parsing logic
def parsecsv():
	print("\nstarting CSV Parse...")
	f = open(furl, newline='')
	#r = csv.reader(f, delimiter=',')
	#print(next(islice(r, 0, 10)))
	c = f.readlines()
	#pattern = f'({tlog})'
	for line in c:
		#print(line)
		if re.match(csvregex,line):
			print("New Entry:" + line)


# Main
time = pagefetch()
#timelog(time)


# if time has been changed since last check, WGET new CSV, and parse for new entries
# else, do nothing

"""
if (timelog(time)):
	print("true")
	WGETfile(url, furl)
	parsecsv()
else:
	print("false")
"""

WGETfile(url, furl)
parsecsv()
