#coding:utf-8

from django.db import models
from datetime import date

class Lobbyist(models.Model):
	firstname		= models.CharField(max_length=100)
	lastname		= models.CharField(max_length=100)
	longterm		= models.BooleanField(default=False)
	timestamp_firstseen	= models.DateTimeField(auto_now_add=True)
	timestamp_lastupdated	= models.DateTimeField(auto_now=True)

	#class Meta:
	#	order_by	= ("lastname", "firstname")

	def name(self):
		return "%s %s" % (self.firstname, self.lastname)

	def access(self):
		if self.longterm:
			return "Long term access"
		else:
			try:
				curpass = self.euaccesspass_set.all().order_by("-expiry")[0]
				if curpass.expiry < date.today():
					return "Lapsed"
				else:
					return "Valid until %d/%d/%d" % (curpass.expiry.day, curpass.expiry.month, curpass.expiry.year)
			except:
				return "No access"


class Lobby(models.Model):
	name			= models.CharField(max_length=200)
	lobbyists		= models.ManyToManyField(Lobbyist)
	timestamp_firstseen	= models.DateTimeField(auto_now_add=True)
	timestamp_lastupdated	= models.DateTimeField(auto_now=True)


class EUAccessPass(models.Model):
	lobbyist		= models.ForeignKey(Lobbyist)
	expiry			= models.DateField()

	def access(self):
		if self.expiry < date.today():
			return "Lapsed"
		else:
			return "Valid"
