import sys
import os
import facebook
import json

PAGE_TOKEN = os.environ['PAGE_TOKEN']
POSTS_FILE = sys.argv[1]

def transform_comments(graph, post_id):
    PAGE_ID = post_id.split("_")[0]

    # @todo: add 'since' so we download only data from last week (?)
    for comment in graph.get_all_connections(post_id, 'comments', filter='stream', fields='id,created_time,permalink_url,from,parent{id},message,like_count', order='reverse_chronological'):
        ## Transform comment into socwatch format
        scomment = {}
        scomment['id'] = "%s_%s" % (PAGE_ID, comment['id'])
        scomment['resource'] = os.environ['RESOURCE']
        scomment['source'] = 'facebook'
        scomment['author'] = comment['from']['name'] if 'from' in comment else 'N/A'
        scomment['published_at'] = comment['created_time'][:-5] + 'Z'
        scomment['language'] = 'cs'
        scomment['url'] = comment['permalink_url']
        scomment['title'] = '%s - %s' % (scomment['author'], scomment['resource'])
        scomment['content'] = comment['message']
        ## @note: currently, we do not attempt to capture the structure (althought it is in the downloaded data)
        ## @todo: entering a correct value might impact pairing of results in sirius BE
        scomment['parent_id'] = post_id
        if ('parent' in comment):
            scomment['in_reply_to'] = "%s_%s" % (PAGE_ID, comment['parent']['id'])
        else:
            scomment['in_reply_to'] = post_id

        scomment['react_like'] = comment['like_count']
        ## @note: copy output of socwatch
        scomment['sentiment'] = 'missing'
        return scomment

graph = facebook.GraphAPI(access_token=PAGE_TOKEN)

with open(POSTS_FILE) as json_file:
    data = json.load(json_file)
    for post in data['data']:
        print (json.dumps(transform_comments(graph, post['id'])))
