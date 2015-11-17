# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".."))  # only for example_project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alibaba.settings")

from django.core.mail import EmailMultiAlternatives

message = {
    'body': u'Dear admin12,\n\nThank you for signing up at \u6708\u5149\u5427.\n\nTo activate your account you should click on the link below:  \nhttp://yueguangba.com/accounts/activate/e7907b1b45f237082c194c400b3efd160dc4f9\n8d/\n\nThanks for using our site!  \nSincerely,  \n\u6708\u5149\u5427\n\n',
    'from_email': u'月光吧 <1026414376@qq.com>',
    'subject': u'Your signup at \u6708\u5149\u5427.',
    'to': [u'290191473@qq.com']}

msg = EmailMultiAlternatives(**message)
msg.send()
