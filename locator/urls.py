from django.conf.urls.defaults import *
from . import views
urlpatterns = patterns('',
    # Example:
    (r'^lookup.json', views.inmatelookup),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

