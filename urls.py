import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from geek.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
	# Browsing
	(r'^$', home_page),
	(r'^blog/$', blog_page),
	(r'^home/$', home_page),
	(r'^feedback/$', feedback_page),
	(r'^guidelines/$', guidelines_page),
	(r'^storycapture/$', story_save_page),
	(r'^playlists/(\w+)/$', playlist_page),
	(r'^storytag/([^\s]+)/$', story_tag_page),
	(r'^storytag/$', story_cloud_page),
	(r'^beforeafter/$', before_after_page),
	(r'^playlist_open/$', playlist_open),
	(r'^tag/([^\s]+)/$', tag_page),
	(r'^tag/$', tag_cloud_page),
	(r'^search/$', search_page),
	(r'^bookmark/(\d+)/$', bookmark_page),
	
	# Session Management
	(r'^login/$', login_page),
	(r'^logout/$', logout_page),
	(r'^register/$', register_page),
	(r'^register/success/$', direct_to_template,
		{'template': 'registration/register_success.html'}),

	# Account Management
	(r'^saveplaylist/$', playlist_save_page),
	(r'^savestory/$', story_save_page),
	(r'^submit/$', story_save_page),			# stubbed out for now
	
	# Site Media
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': site_media}),
		
	# Comments
	(r'^comments/',
		include('django.contrib.comments.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
