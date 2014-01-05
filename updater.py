import urllib2
import re
import argparse
import sys
import os
from urllib2 import urlopen, URLError, HTTPError

def createDir(directory):
	if not os.path.exists(directory):
		os.mkdir(directory)


def dlfile(url, destdir):
    
    # Open the url
    try:
    	createDir(destdir)
    	opener = urllib2.build_opener()
    	opener.addheaders.append(('Cookie', 'eula_3.0_agreed=tools.hana.ondemand.com/developer-license-3.0.0.txt'))
        f = opener.open(url)
        
        print "downloading " + url + " in directory: " + destdir

        # Open our local file for writing
        with open(destdir + url.rsplit('/',1)[1], "wb") as local_file:
            local_file.write(f.read())
            
        print os.path.abspath(local_file)

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def unzip(file,output_dir):
	import zipfile
	#rx_path = r'{0}'.format(output_dir)
	zip = zipfile.ZipFile(r'{0}'.format(file))
	zip.extractall(r'{0}'.format(output_dir))


#usage
# Run this command in a shell:
# python updater.sh [OPTIONS]
# AVAILABLE OPTIONS:
# --list-availabes: list all the available versions
# --use-version-1: indicates to use 1.x version of sdk. Default is to use beta version 2.x
# --check: shows informations of the current installation
# --update-to-version <version>: donwload the version specified. You can specify also 'latest' version

#This is the main url of SAP tools site.
SDK_URL = 'https://tools.hana.ondemand.com'

#These flags are the links name in the html for latest version
LAST_FLAG = 'latestSdk'
LAST_BETA_FLAG = 'latestBetaSdk'

#These are the prefix in the file name of the two version of sdk
SDK_WEB_FLAG = 'neo-java-web-sdk-'
SDK_J2EE_WP_FLAG = 'neo-javaee6-wp-sdk-'
#define the directory name for sdk installation
hcp_sdk_dir = 'sap-hcp-sdk'

#get the current user home directory
user_home = os.getenv("HOME")
sdk_home = user_home + os.sep + hcp_sdk_dir + os.sep

#parsing arguments
parser = argparse.ArgumentParser(description='SAP HCP SDK Updater')
parser.add_argument('-l','--list-available-versions', dest="list", action="store_true", default=False,
                   help='list all the available versions.')
parser.add_argument('-s','--set-sdk-type', dest="sdktype", type=int, default=2, choices=[1, 2],
                   help='Set the sdk version type to use.')
parser.add_argument('-u','--update-to-version', dest="sdkversion", default='latest',
                   help='Update sdk to version. Default update to latest version 2')
parser.add_argument('-d','--sdk-home', dest="sdkhome", default=sdk_home,
				   help='Directory in which the sdk will be installed. NEOSDK_HOME Environment variable')


args = parser.parse_args()

#start the real work

#download html source
response = urllib2.urlopen(SDK_URL)
html = response.read()


if args.list:
	print 'Available SDK Versions'
	urls = re.findall(r'href=[\'"]sdk/?([^\'" >]+)', html)
	
	urls = sorted(set(urls))
	urls.sort(key=str.lower)
	for url in urls:
		print '   ' + url
	sys.exit(0)


if args.sdkversion:
	if args.sdktype == 2:
		url_id = LAST_BETA_FLAG
	else:
		url_id = LAST_FLAG

	if args.sdkversion == 'latest':
		print 'Download the latest version: ' 
		#identify the latest version
		rx = r'id=\"{0}\" href=[\'"]sdk/?([^\'" >]+)'.format(url_id)
		latest_version = re.findall(rx, html)
		#print latest_version
		#download
		dlfile(SDK_URL+"/sdk/"+latest_version[0], sdk_home)
		#unzip()




