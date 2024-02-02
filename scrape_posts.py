""" Print all Facebook posts and insights (e.g. like) for them"""

import os
import json
import facebook

PAGE_TOKEN = os.environ['PAGE_TOKEN']
PAGE_ID = os.environ['PAGE_ID']

print(json.dumps(facebook.GraphAPI(access_token=PAGE_TOKEN).get_object(
    '/%s/posts' % (PAGE_ID),
    fields="id,created_time,message,permalink_url,"
        "insights.metric(post_reactions_by_type_total).period(lifetime)"
        ".as(post_reactions_by_type_total),shares,full_picture"
)))
