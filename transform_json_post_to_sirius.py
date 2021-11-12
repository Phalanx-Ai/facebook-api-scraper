""" Transform post data from Facebook to Sirius format """
import sys
import os
import json

AUTHOR = os.environ['AUTHOR']
RESOURCE = os.environ['RESOURCE']

def transform_post(post):
    """ Transform single post from original Facebook format """
    spost = {}

    ## Transform comment into socwatch format
    spost = {}
    spost['id'] = post['id']
    spost['resource'] = RESOURCE
    spost['source'] = 'facebook'
    spost['author'] = AUTHOR
    spost['published_at'] = post['created_time'][:-5] + 'Z'
    spost['language'] = 'cs'
    spost['url'] = post['permalink_url']
    spost['title'] = spost['author']
    # @note: E.g. update of page phone number - no message is included
    spost['content'] = post.get('message', '')
    ## @note: currently, we do not attempt to capture the structure
    # 		(althought it is in the downloaded data)
    ## @todo: entering a correct value might impact pairing of results in sirius BE
    spost['parent_id'] = None
    ## @note: copy output of socwatch
    spost['sentiment'] = 'missing'
    spost['image_url'] = post.get('full_picture', '')

    if 'post_reactions_by_type_total' in post:
        for reaction in ['like', 'love', 'wow', 'haha', 'sorry', 'anger']:
            spost['react_%s' % (reaction)] = \
                post['post_reactions_by_type_total']['data'][0]['values'][0]['value'].get(reaction, 0)

    spost['react_share'] = post.get('shares', {'count': 0})['count']

    return spost

POSTS_FILE = sys.argv[1]
with open(POSTS_FILE) as json_file:
    for single_post in json.load(json_file)['data']:
        print(json.dumps(transform_post(single_post)))
