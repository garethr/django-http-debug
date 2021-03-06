from django.http import HttpResponse, Http404
from django.conf import settings

from lib.log import get_logger

# get the loggers we want to use here
ACCESS_LOG = get_logger('access')

def log_request(request, path):
    "We want to log all incoming requets, along with a few useful details"
    # first compose the log message. We want to know the path
    # as well as the request method
    msg = "%s request for %s" % (request.META['REQUEST_METHOD'], path)
    # if we have a query string we need to get that from the request
    # as it's not part of the path passed to the view
    if request.META['QUERY_STRING']:
        msg = "%s?%s" % (msg, request.META['QUERY_STRING'])
    # a Post or Put request will store data in the request
    # using the inbuilt urlencode method will give us 
    # a nice human readable version of this
    if request.POST:
        msg = "%s with data %s" % (msg, request.POST.urlencode())
    # we have a special list of things we don't care about in settings
    if path not in settings.REQUEST_EXCLUDES:
        # we have something we want, so lets log it
        ACCESS_LOG.info(msg)
        return HttpResponse("OK")
    else:
        # we hit something we don't care for, so ignore it
        raise Http404("NOT PRESENT")