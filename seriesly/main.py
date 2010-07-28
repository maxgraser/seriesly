import logging, os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library

use_library('django', '1.1')
# Google App Engine imports.
from google.appengine.ext.webapp.util import run_wsgi_app

# Force sys.path to have our own directory first, in case we want to import
# from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Must set this env var *before* importing any part of Django

from django import db
from django.core import signals
import django.core.handlers.wsgi
 
 
def log_exception(sender, **kwargs):
    if 'request' in kwargs:
        try:
            repr_request = repr(kwargs['request'])
        except:
            repr_request = 'Request repr() not available.'
    else:
        repr_request = 'Request not available.'
    logging.exception("Request: %s" % repr_request)
 
signals.got_request_exception.connect(log_exception)
signals.got_request_exception.disconnect(db._rollback_on_exception)


def main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()
    # Run the WSGI CGI handler with that application.
    run_wsgi_app(application)
    
def profile_main():
    # This is the main function for profiling
    # We've renamed our original main() above to real_main()
    import cProfile, pstats, StringIO
    prof = cProfile.Profile()
    prof = prof.runctx("main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    logging.info("Profile data:\n%s", stream.getvalue())

if __name__ == '__main__':
    # profile_main()
    main()