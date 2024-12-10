import os
import logging
import json
import pyjson5
from dotenv import load_dotenv
import argparse

# Bot utilities
from utils.bluesky import get_bluesky_instance, bluesky_faceted_post
from utils.bluesky import bluesky_reply
from atproto import models


BLUESKY_USERNAME = "me-im-asking.bsky.social"
BLUESKY_PASSWORD = "imeg-xpep-ikc4-nqno"
BLUESKY_CLIENT =  "https://bsky.social"

client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)

# here's our list of posts
# text of original post
# the model of the returned post
# the model of a parent post, if any
# the model of a root post, if any

post1 = { 
        'text': 'this is post 1',
        'post_root': None,
        'post': None,
        'post_parent':  None
}

post2 = { 
        'text': 'this is post 2',
        'post_root': None,
        'post': None,
        'post_parent':  None
}


post3 = { 
        'text': 'this is post 3',
        'post_root': None,
        'post': None,
        'post_parent':  None
}


thread_of_posts = (
    post1, post2, post3
)

for idx, post in enumerate(thread_of_posts):
    
    if idx == 0:
        this_post = client.send_post(post['text'])
        root_post = this_post

        post['post_root'] = root_post
        post['post'] = this_post

        print(idx, post)
    
    else: 
        previous_post = thread_of_posts[idx-1]

        root_post = previous_post['post_root']
        print(root_post)
        parent_post = previous_post['post']

        parent = models.create_strong_ref(parent_post)
        root = models.create_strong_ref(root_post)
                
        this_post = client.send_post(
            text = post['text'],
            reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
        )

        post['post_root'] = root_post
        post['post_parent'] = parent_post
        post['post'] = this_post
        print (idx, post)



        