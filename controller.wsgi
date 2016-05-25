#!/usr/bin/python
import sys
import logging
import uuid
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pydrive/")

from pythonapp import app as application
application.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"