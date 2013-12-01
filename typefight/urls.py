from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'voter.views.match_up', name='matchup'),
    url(r'^vote/$', 'voter.views.cast_vote', name='cast-vote'),
    url(r'^letters/$', 'voter.views.get_letters', name='letters'),
    url(r'^matchup/create/$', 'voter.views.create_matchup', name='create-matchup'),
    url(r'^results/$', 'voter.views.results', name='results'),
    url(r'^console/$', 'voter.views.admin_console', name='admin_console'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
