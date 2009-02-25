import os
import unittest

from django.test.utils import setup_test_environment, teardown_test_environment
from django.conf import settings

import tests

def run_tests(test_labels, verbosity=0, interactive=False, extra_tests=[]):

    setup_test_environment()

    suite = unittest.TestSuite()
    
    tl = unittest.TestLoader().loadTestsFromModule(tests)
    suite._tests = tl._tests

    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    
    teardown_test_environment()
    
    # we want to keep our test logs seperate from our normal logs
    settings.LOG_FILE = "%s_test" % settings.LOG_FILE
    
    # we want to get rid of our test log file afterwards
    for log in settings.LOGS:
        try:
            # remove our log file
            os.remove("%s_%s" % (settings.LOG_FILE, log))
        except OSError:
            # not all tests are going to tigger the get_log
            # method which creates the log file
            # in which case we don't care
            pass
    
    return len(result.failures) + len(result.errors)