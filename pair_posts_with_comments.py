""" Pair loaded FB posts with their (already imported) comments """
import sys
import os
from siriusrest import login, post_data, URL

token = login(os.environ['SIRIUS_USER'], os.environ['SIRIUS_PASS'])
post_data(token, URL + "socwatch/pairPosts", "")
