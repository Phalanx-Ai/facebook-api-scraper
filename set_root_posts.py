import sys
import os
from siriusrest import login, post_data, URL

with open(sys.argv[1], encoding="utf-8") as content_file:
	content = content_file.read()

token = login(os.environ['SIRIUS_USER'], os.environ['SIRIUS_PASS'])
post_data(token, URL + "socwatch/setRootPost", content)
