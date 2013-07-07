#! /usr/bin/env python
#
# Copyright (c) 2013 Theopolisme <theopolismewiki@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Returns the percentage of recent edits, out of TOTAL_EDITS, that have a specific tag,
TAG_TO_SEARCH. Only edits classified as meeting the requirements in TYPE_OF_EDITS
(see <http://www.mediawiki.org/wiki/API:Recentchanges#Parameters>) will be counted.
Edits whose summaries include strings in EXCLUDE_STRINGS will be skipped and not factored
into the total. 
"""

import mwclient
import password

TAG_TO_SEARCH = 'visualeditor'
TOTAL_EDITS = 10000
TYPE_OF_EDITS = "!bot|!anon"
EXCLUDE_STRINGS = ['AWB', 'TW', 'HG', 'STiki', 'AFCH', 'Undid']

def exclude(comment):
	for excl_string in EXCLUDE_STRINGS:
		if comment.find(excl_string) != -1:
			return True
	return False

def main():
	site = mwclient.Site('en.wikipedia.org')
	site.login(password.username, password.password)

	rc = site.recentchanges(namespace=0,prop='tags|timestamp|user|comment',show=TYPE_OF_EDITS)

	done = 0
	ve = 0

	for change in rc:
		if done < TOTAL_EDITS:
			if 'anon' not in change and exclude(change['comment']) == False:
				done += 1
				if TAG_TO_SEARCH in change['tags']:
					ve += 1
		else:
			break

	print "VisualEditor was tagged in {} out of {} edits, or {}%".format(ve,done,(float(ve)/done)*100)

if __name__ == '__main__':
	main()
