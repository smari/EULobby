#coding:utf-8
import os
import sys
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from scrapemark import scrape
from urllib2 import urlopen
from lobby.models import *
from datetime import date

letters = [chr(x) for x in range(65, 90)] + ['0']

baseurl = "http://www.europarl.europa.eu/parliament/expert/lobbyAlphaOrderByOrg.do?letter=%s&language=EN"

def getletters():
	for letter in letters:
		url = baseurl % letter
		parsefile(urlopen(url))

def parsefile(thefile):
	if type(thefile) == file:
		fh = thefile
	else:
		fh = open(thefile)

	text = fh.read()

	wait = """
	"""

	results = scrape("""
{*
	<td class="listcontent{{[color]}}_left" width="290">
		{{ [names].companyname }}
	</td>        
	<td class="listcontent{{[color]}}_left">
		{*
		<span class="listcontent_iconleft" title="Temporary - Expiry date: {{ [names].expires }}">
		<b> {{ [names].lastname }} </b>
		{{ [names].firstname }}
		</span>
		*}
		{*
		<span class="listcontent_marginleft">
		<b> {{ [names].lastname }} </b>
		{{ [names].firstname }}
		</span>
		*}
	</td>
*}
""", text)
	companies = 0
	lobbyists = 0

	print results

	for r in results["names"]:
		r["lastname"] = r["lastname"].capitalize()
		if not r.has_key("companyname"):
			r["companyname"] = lastcompanyname
		else:
			companies += 1
			print "%-70s" % (r["companyname"])

		lobbyists += 1
		
		lobby, status = Lobby.objects.get_or_create(name=r["companyname"])
		if status:
			print "  |        [Found new lobby group!]"

		lobbyist, status = Lobbyist.objects.get_or_create(firstname=r["firstname"], lastname=r["lastname"])
		if status:
			print "  |        [Found new lobbyist!]"

		lobby.lobbyists.add(lobbyist)

		if r.has_key("expires") and r["expires"] != None:
			print "  |----- T %s %s     (EXPIRES '%s')" % (r["firstname"], r["lastname"], r["expires"])
			exp = [int(x) for x in r["expires"].split("/")]
			exp.reverse()
			exp = date(*exp)
			euapass, status = EUAccessPass.objects.get_or_create(lobbyist=lobbyist, expiry=exp)
			print "  |        [New access pass found]"
		else:
			print "  |----- F %s %s" % (r["firstname"], r["lastname"])
			lobbyist.longterm = True
			lobbyist.save()

		lastcompanyname = r["companyname"]

	print "Companies: %d" % companies
	print "Lobbyists: %d" % lobbyists

# http://ec.europa.eu/transparencyregister/public/consultation/listlobbyists.do?letter=A&alphabetName=LatinAlphabet


if __name__ == "__main__":
	parsefile("testdata/ac_a.html")
