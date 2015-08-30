#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'userena.runtests.settings'

import django

if django.VERSION >= (1, 7, 0):
    # starting from 1.7.0 we need to run setup() in order to populate
    # app config
    django.setup()

from django.conf import settings
from django.db.models import get_app
from django.test.utils import get_runner


def usage():
    return """
    Usage: python runtests.py [UnitTestClass].[method]

    You can pass the Class name of the `UnitTestClass` you want to test.

    Append a method name if you only want to test a specific method of that
    class.
    """


def main():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, failfast=False)

    if len(sys.argv) > 1:
        test_modules = sys.argv[1:]
    elif len(sys.argv) == 1:
        test_modules = []
    else:
        print(usage())
        sys.exit(1)

    if django.VERSION >= (1, 6, 0):
        # this is a compat hack because in django>=1.6.0 you must provide
        # module like "userena.contrib.umessages" not "umessages"
        test_modules = [
            # be more strict by adding .tests to not run umessages tests twice
            # if both userena and umessages are tested
            get_app(module_name).__name__[:-7] + ".tests"
            for module_name
            in test_modules
        ]

    if django.VERSION < (1, 7, 0):
        # starting from 1.7.0 built in django migrations are run
        # for older releases this patch is required to enable testing with
        # migrations
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    failures = test_runner.run_tests(test_modules or ['userena'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
