from pathlib import Path
from urllib.request import urlopen
from datetime import datetime
import re
import os
import wget

furl = datetime.now().strftime("%Y") + ".csv"
url = "https://wichita.ogs.ou.edu/eq/catalog/2023/"
restr = r"\.csv\<.*(20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\s[0-9][0-9]:[0-9][0-9])"
tlog = Path("./timelog")

# logic outline:
# scrape page for timestamp
# check if timelog file exists
# if not, create it, write current page timestamp to it.
# if timelog exists, compare page timestamp to timelog
# if not different, quit
# if different, run remaining code to grab CSV values (TBD)

def timelog(time):
	if DoesFileExist(tlog):
		if IsFileEmpty(tlog):
			print("file empty...writing time...")
			WriteTime(tlog,time)
		elif time == open(tlog).read():
			print("contents unchanged.")
		else:
			#if file contents not match, update with latest timestamp
			print("file outdated...updating...")
			WriteTime(tlog,time)
	else:
		print("timelog file missing...creating timelog file...")
		WriteTime(tlog,time)

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
		os.remove(fpath)
	fullpath = urlpath + fpath
	wget.download(fullpath, out="./")

# Main
#time = pagefetch()
#timelog(time)

WGETfile(url, furl)
