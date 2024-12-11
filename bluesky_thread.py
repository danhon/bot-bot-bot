import os
import logging
import json
import pyjson5
from dotenv import load_dotenv
import argparse
import pprint

# Bot utilities
from utils.bluesky import get_bluesky_instance, bluesky_faceted_post
from utils.bluesky import bluesky_reply, Post_in_Thread
from atproto import models

from utils.tracery import get_rules, generate_posts, generate_normal_post


rules = get_rules('grammars/','startrek-granddesigns.json')
post = generate_normal_post(rules)

thread_text = post.splitlines()

thread_posts = []

for idx, item in enumerate(thread_text):
    this_thread_post = Post_in_Thread(text=item)
    thread_posts.append(this_thread_post)

# BLUESKY_USERNAME = "me-im-asking.bsky.social"
# BLUESKY_PASSWORD = "imeg-xpep-ikc4-nqno"
# BLUESKY_CLIENT =  "https://bsky.social"

BLUESKY_USERNAME = "st-grand-designs.bsky.social"
BLUESKY_PASSWORD = "pmvr-flgv-lqyv-qvgx"
BLUESKY_CLIENT =  "https://bsky.social"


client = get_bluesky_instance(BLUESKY_USERNAME, BLUESKY_PASSWORD, BLUESKY_CLIENT)


def post_thread(thread_of_posts):

    for idx, post in enumerate(thread_of_posts):
        print(idx, len(post.text), post.text)

        
        if idx == 0:
            this_post = client.send_post(post.text)
            root_post = this_post

            post.root_post = root_post
            post.post = this_post

        
        else: 
            previous_post = thread_of_posts[idx-1]

            root_post = previous_post.root_post
            print(root_post)
            parent_post = previous_post.post

            parent = models.create_strong_ref(parent_post)
            root = models.create_strong_ref(root_post)
                    
            this_post = client.send_post(
                text = post.text,
                reply_to = models.AppBskyFeedPost.ReplyRef(parent = parent, root = root)
            )

            post.root_post = root_post
            post.parent_post = parent_post
            post.post = this_post
            print (idx, post)


post_thread(thread_posts)
