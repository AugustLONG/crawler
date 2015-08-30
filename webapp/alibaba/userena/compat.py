# -*- coding: utf-8 -*-
from collections import defaultdict
import django


# this default dict will store all compat quirks for parameters of
# django.contrib.auth views
auth_views_compat_quirks = defaultdict(lambda: dict())

# below are quirks we must use because we can't change some userena API's
# like (url names)
if django.VERSION >= (1, 6, 0):  # pragma: no cover
    # in django >= 1.6.0 django.contrib.auth.views.reset no longer looks
    # for django.contrib.auth.views.password_reset_done but for
    # password_reset_done named url. To avoid duplicating urls we
    # provide custom post_reset_redirect
    auth_views_compat_quirks['userena_password_reset'] = {
        'post_reset_redirect': 'userena_password_reset_done',
    }

    # same case as above
    auth_views_compat_quirks['userena_password_reset_confirm'] = {
        'post_reset_redirect': 'userena_password_reset_complete',
    }


# below are backward compatibility fixes
password_reset_uid_kwarg = 'uidb64'
if django.VERSION < (1, 6, 0):  # pragma: no cover
    # Django<1.6.0 uses uidb36, we construct urlpattern depending on this
    password_reset_uid_kwarg = 'uidb36'

if django.VERSION < (1, 5, 0):
    from django.utils.encoding import smart_unicode as smart_text
else:
    from django.utils.encoding import smart_text


# SiteProfileNotAvailable compatibility
if django.VERSION < (1, 7, 0):  # pragma: no cover
    from django.contrib.auth.models import SiteProfileNotAvailable
else:  # pragma: no cover
    class SiteProfileNotAvailable(Exception):
        pass

# old fallback to django hashcompat
try:
    from hashlib import sha1 as sha_constructor, md5 as md5_constructor
except ImportError:  # pragma: no cover
    from django.utils.hashcompat import sha_constructor, md5_constructor
