from django.conf.urls.defaults import *

from views import log_request

# given that this application is designed to simple log all incoming 
# requests we just grab everything and pass it to our view
urlpatterns = patterns('',
    (r'^(.*)', log_request),
)
