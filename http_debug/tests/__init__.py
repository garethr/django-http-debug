import os

from django.core import mail
from django.test import TestCase
from django.conf import settings

# we want to keep our test logs seperate from our normal logs
settings.LOG_FILE = "%s_test" % settings.LOG_FILE

class NoDatabaseTestCase(TestCase):
    """
    TestCase replacement to ignore all the database
    stuff, mainly fixtures and flush
    """
    def _pre_setup(self):
        "Override the offending method which talks to the DB"
        # we do want some of the featues from the default method
        if hasattr(self, 'urls'):
            self._old_root_urlconf = settings.ROOT_URLCONF
            settings.ROOT_URLCONF = self.urls
            clear_url_caches()
        mail.outbox = []

class ViewTests(NoDatabaseTestCase):
    
    def tearDown(self):
        """
        We define a log for tests above, but after each test
        we should remove it, other wise it's going to clash
        """
        for log in settings.LOGS:
            try:
                # Open the log file and write a blank string to it, 
                # then close the file. Otherwise the file builds 
                # up across multiple tests.
                # the test runner itself gets rid of all the files
                # after each full run
                handle = open("%s_%s" % (settings.LOG_FILE, log), 'w')
                handle.write('')
                handle.close()
            except OSError:
                # not all tests are going to tigger the get_log
                # method which creates the log file
                # in which case we don't care
                pass
   
    def test_logging_for_get(self):
        response = self.client.get('/test')
        handle = open("%s_access" % settings.LOG_FILE, 'r')
        content = handle.read()
        if content[-22:-2] == "GET request for test":
            assert True
        else:
            assert False

    def test_logging_for_post(self):
        response = self.client.post('/test', {'data': 'test'})
        handle = open("%s_access" % settings.LOG_FILE, 'r')
        content = handle.read()
        assert "POST" in content
        if content[-11:-2] == "data=test":
            assert True
        else:
            assert False
        
    def test_normal_views(self):
        response = self.client.get('/test')
        self.assertContains(response, "OK")
        response = self.client.get('/test?test=test')
        self.assertContains(response, "OK")
        response = self.client.get('/test/test2')
        self.assertContains(response, "OK")

    def test_excluded_views(self):
        # we clobber whatever might be in settings so
        # we can be sure of it working
        settings.REQUEST_EXCLUDES = (
            'favicon.ico',
            'something/random',
        )
        response = self.client.get('/favicon.ico')
        self.assertContains(response=response, 
            text="NOT PRESENT", status_code=404)
        response = self.client.get('/something/random')
        self.assertContains(response=response, 
            text="NOT PRESENT", status_code=404)
