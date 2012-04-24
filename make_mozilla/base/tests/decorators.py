from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
import os

__all__ = ['wip']

def fail(message):
    raise AssertionError(message)

def wip(f):
    @wraps(f)
    def run_test(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            raise SkipTest("WIP test failed: " + str(e))
        fail("test passed but marked as work in progress")
    return attr('wip')(run_test)

def integration(f):
    @wraps(f)
    def run_test(*args, **kwargs):
        integration_run = (os.getenv('INTEGRATION', None) is not None)
        if integration_run:
            f(*args, **kwargs)
        else:
            raise SkipTest("Skipping integration test")
    return attr('integration')(run_test)

