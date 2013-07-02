"""
Read in a file
Extract either:
	- emails
	- urls
	- domains
	- mobile (simplified for singapore mobile only)
	- all
Write to a file 
"""

import re
import traceback
import urlparse

# Email regex for extraction
# A simple version
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)

# URL regex
# url_regex = re.compile('(https?://\S*)', re.IGNORECASE)
url_regex = re.compile('(?:(?:https?|ftp|file)://|www\.|ftp\.)[-A-Z0-9+&@#/%=~_|$?!:,.]*[A-Z0-9+&@#/%=~_|$]', re.IGNORECASE)

# Singapore phone number regex
# Starts with 8 or 9, and 8 digit long
sg_mobile_phone_regex = re.compile('[8-9][0-9]{7}')


# A convenient enum for the type of data that can be extracted
class EXTRACT_TYPE:
	EMAIL, URL, DOMAIN, MOBILE = 'email', 'url', 'domain', 'mobile'


def extract(type, in_filename):
	# Read the file
	file = open(in_filename,"r")
	data = file.read()

	if (type == EXTRACT_TYPE.EMAIL):
		extracted_data_list = extract_emails(data)
		print '%d emails extracted to .csv' % len(extracted_data_list)

	if (type == EXTRACT_TYPE.URL):
		extracted_data_list = extract_urls(data)
		print '%d URLs extracted to .csv' % len(extracted_data_list)

	if (type == EXTRACT_TYPE.DOMAIN):
		extracted_data_list = extract_domains(data)
		print '%d domains extracted to .csv' % len(extracted_data_list)

	if (type == EXTRACT_TYPE.MOBILE):
		extracted_data_list = extract_sg_mobile(data)
		print '%d mobile numbers extracted to .csv' % len(extracted_data_list)

	# Write to the file
	# eg. filename - email.csv
	out_filename = in_filename.split('.')[0] + ' - ' + type + '.csv'
	file = open(out_filename, "w+")
	file.writelines("\n".join(list(extracted_data_list)))
	file.close()





def cleanup_for_emails(data):
	"""
	Clean up data
	We replace these with @
	  [at]  (at)  <at>  /at/  [@]  	
	We replace these with .
	  [dot]  etc..  [.]
	Also replace remove the surrounding whitespace
	"""
	data = re.sub('\s*[[(</-]?\s*(?:at|@)\s*[])>/-]?\s*', '@', data)
	data = re.sub('\s*[[(</-]?\s*(?:dot|\.)\s*[])>/-]?\s*', '.', data)
	return data


def extract_emails(data):
	"""
	Extract all emails from data. This includes email obfuscation techniques. 
	It is impossible to cover all cases, but this method will try as many of the common cases.

	>>> extract_emails('samwize@gmail.com')
	set(['samwize@gmail.com'])

	>>> extract_emails('bluebirdof [dot] happiness [at] yahoo [dot] com')
	set(['bluebirdof.happiness@yahoo.com'])
	
	>>> extract_emails('rajr at uol dot com dot br')
	set(['rajr@uol.com.br'])

	>>> extract_emails('hinfai/at/gmail/dot/com')
	set(['hinfai@gmail.com'])

	>>> extract_emails('eehassell   -   at  -  hushmail.com')
	set(['eehassell@hushmail.com'])

	>>> extract_emails('kellydc[.]wanderer[@]gmail<.>com')
	set(['kellydc.wanderer@gmail.com'])

	"""
	email_set = set()

	# Clean up the data for email first
	data = cleanup_for_emails(data)

	# Extract each email
	for email in email_regex.findall(data):
		email_set.add(email)

	return email_set


def extract_urls(data):
	"""
	Extract URLs from data.

	>>> extract_urls('yoyoyo http://www.regexguru.com/2008/11/detecting-urls-in-a-block-of-text/ yoyoyo')
	set(['http://www.regexguru.com/2008/11/detecting-urls-in-a-block-of-text/'])

	>>> extract_urls('ohoho\nhttp://www.google.com.sg/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CHQQFjAB&url=http%3A%2F%2Fwww.junda.com%2F&ei=faoXUMKNEsWGrAfhm4DwCg&usg=AFQjCNFXDbUHvVhdvVkPuSgDVU-Pb01EiA&sig2=EkLM-_6En7Jg4_XVAzQYAQ me too\nme too')
	set(['http://www.google.com.sg/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CHQQFjAB&url=http%3A%2F%2Fwww.junda.com%2F&ei=faoXUMKNEsWGrAfhm4DwCg&usg=AFQjCNFXDbUHvVhdvVkPuSgDVU-Pb01EiA&sig2=EkLM-_6En7Jg4_XVAzQYAQ'])
	
	>>> extract_urls('https://a.b.com http://a.b.org')
	set(['https://a.b.com', 'http://a.b.org'])

	"""
	_set = set()
	for x in url_regex.findall(data):
		_set.add(x)
	return _set


def extract_domains(data):
	"""
	Extract the domains. 

	This method use extract_urls to get all the URLs first, then use urlparse module to get the hostname.
	"""
	_set = set()
	urls = extract_urls(data)
	for url in urls:
		hostname = urlparse.urlparse(url).hostname.split(".")
		hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
		_set.add(hostname)
	return _set


def extract_sg_mobile(data):
	"""
	Extract Singapore mobile phone numbers 

	The regex is a simplified one. A match starts with 8 or 9, and is 8 digit long.
	"""
	_set = set()
	for phone in sg_mobile_phone_regex.findall(data):
		_set.add(phone)
	return _set


if __name__ == "__main__":
	import sys
	import argparse
	
	# Describe the data
	parser = argparse.ArgumentParser(description='Extract useful data from a file!')

	# filename is positional argument
	parser.add_argument("filename", help="The filename to extract data from")
	
	parser.add_argument("-e", "--emails", action='store_true', help="Extract emails")
	parser.add_argument("-u", "--urls", action='store_true', help="Extract URLs")
	parser.add_argument("-d", "--domains", action='store_true', help="Extract domain names")
	parser.add_argument("-m", "--mobile", action='store_true', help="Extract mobile phone numbers (for Singapore only)")
	parser.add_argument("-a", "--all", action='store_true', help="Extract all data types above")
	
	# -v 2
	parser.add_argument("-v", "--verbosity", help="Increase output verbosity")
	parser.add_argument('--version', action='version', version='%(prog)s 0.1')

	args = parser.parse_args()
	# print vars(args)

	if args.emails or args.all:
		print 'Extracting emails..'
		extract(EXTRACT_TYPE.EMAIL, args.filename)

	if args.urls or args.all:
		print 'Extracting URLs..'
		extract(EXTRACT_TYPE.URL, args.filename)

	if args.domains or args.all:
		print 'Extracting domains..'
		extract(EXTRACT_TYPE.DOMAIN, args.filename)

	if args.mobile or args.all:
		print 'Extracting mobile numbers..'
		extract(EXTRACT_TYPE.MOBILE, args.filename)

	if args.verbosity:
		print 'Verbosity level: %s' % args.verbosity








