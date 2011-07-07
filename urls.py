from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^EULobby/', include('EULobby.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^lobby/list/$', 'lobby.views.lobby_list'),
	(r'^lobby/(?P<lobby>\d+)/$', 'lobby.views.lobby_profile'),
	(r'^lobbyist/list/$', 'lobby.views.lobbyist_list'),
	(r'^lobbyist/(?P<lobbyist>\d+)/$', 'lobby.views.lobbyist_profile'),
)


urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)


