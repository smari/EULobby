from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from lobby.models import *


def index(request):
	return render_to_response("index.html")	


def lobby_list(request):
	l = Lobby.objects.all().order_by("name")

	if request.REQUEST.has_key("q"):
		l = l.filter(name__icontains=request.REQUEST.get("q"))

	return render_to_response("lobby_list.html", {"results": l})


def lobby_profile(request, lobby):
	try:	l = Lobby.objects.get(id=lobby)
	except:	raise ObjectDoesNotExist("Must provide a valid lobby id")
	return render_to_response("lobby_profile.html", {"profile": l})

def lobbyist_list(request):
	l = Lobbyist.objects.all().order_by("lastname", "firstname")

	if request.REQUEST.has_key("q"):
		l = l.filter(name__icontains=request.REQUEST.get("q"))

	return render_to_response("lobbyist_list.html", {"results": l})


def lobbyist_profile(request, lobbyist):
	try:	l = Lobbyist.objects.get(id=lobbyist)
	except:	raise ObjectDoesNotExist("Must provide a valid lobbyist id")
	return render_to_response("lobbyist_profile.html", {"profile": l})
