import os
import logging
import pyjson5
import sys

import tracery
from tracery.modifiers import base_english

from utils.bluesky import Post_in_Thread, bluesky_faceted_post

LIMIT_BLUESKY_CHARS = 260
LIMIT_MASTODON_CHARS = 500

# create logger
module_logger = logging.getLogger('bot-bot-bot.utils.tracery')

def generate_posts(rules):
    """Returns a dict containing two Tracery grammars with keys ["long"] and ["short"] when supplied a json Tracaery rules file."""
    post = {}
    
    module_logger.debug('Generating post...')
 
    post['long'] = generate_post(rules)
    post["short"] = generate_post_short(rules)

    module_logger.debug('Long post: %s', post["long"])
    module_logger.debug('Short post: %s', post["short"])

    module_logger.debug('Done generating post.')
    
    return post

def generate_post(rules):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    long_post = grammar.flatten("#origin#")

    while len(long_post) > LIMIT_MASTODON_CHARS:
        long_post = grammar.flatten("#origin#")
    return long_post

def generate_post_short(rules):
    short_post = generate_post(rules)

    while len(short_post) > LIMIT_BLUESKY_CHARS:
        short_post = generate_post(rules)
        if len(short_post) < LIMIT_BLUESKY_CHARS:
            break
    return short_post

def get_rules(GRAMMARS_DIRECTORY, GRAMMAR_JSON):
    """Returns a json rules object to be used with a Tracery grammar"""
    file_path = os.path.join(GRAMMARS_DIRECTORY, GRAMMAR_JSON)
 
    module_logger.debug('Opening rules file %s.', GRAMMAR_JSON)
 
    try: 
        with open(file_path) as rules_file:
            rules = pyjson5.decode_io(rules_file)

        module_logger.debug('Loaded rules for %s.', file_path)

    except IOError:
        module_logger.info("Couldn't open: ", file_path)
        sys.exit()

    return rules


def generate_bluesky_thread(rules):

    thread_posts = generate_bluesky_thread_posts(rules)

    while any(len(post.text) > LIMIT_BLUESKY_CHARS for (post) in thread_posts):
        for idx, post in enumerate(thread_posts):
            module_logger.debug('thread idx %s length %s',idx, len(post.text))

        module_logger.debug((any(len(post.text) > LIMIT_BLUESKY_CHARS for (post) in thread_posts)))
        generate_bluesky_thread(rules)
        if not any(len(post.text) > LIMIT_BLUESKY_CHARS for (post) in thread_posts):
            break
    return thread_posts


def generate_bluesky_thread_posts(rules):
        module_logger.info("Generating thread posts")
        post = generate_normal_post(rules)
        thread_text = post.splitlines()
        thread_posts = []

        for idx, item in enumerate(thread_text):
            facetedpost = bluesky_faceted_post(item)
            this_thread_post = Post_in_Thread(text=item, facetedpost=facetedpost)
            thread_posts.append(this_thread_post)

        # for idx, post in enumerate(thread_posts):
        #     print(idx, len(post.text))        
        module_logger.info("Finished generating thread posts")
        return thread_posts

def generate_normal_post(rules):
    module_logger.info("Generating a 'normal post' whatever that means... (full?)")
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    post = grammar.flatten('#origin#')
    module_logger.info("Post was %s long", len(post))
    module_logger.info("Done doing that")
    return post
