# Tracery Bluesky and Mastodon Bot

Hi, here's a way to post a simple tracery bot to bluesky and mastodon. It is terrible and stupid.

This repo is forked from [Bluesky Python Bot](https://github.com/skygaze-ai/bot-python) and uses the [Mastodon Python API wrapper](https://github.com/halcy/Mastodon.py?tab=readme-ov-file).

## Using this

Completely at your own risk. You'll need uv, and then all you need to do is:
uv run bot.py

if you want there's also a shell script, post.sh that you can use with your crontab if you want? 

### setup
Copy .env.example into .env and 

* stick in what's needed to access your bluesky and mastodon account.
* supply a directory if you want to put your tracery json grammars somewhere other than grammars/.

in bot.py you'll need to set your grammars file if you don't want to inadvertently end up with posting star trek job listings.

### weird stuff

so when we generate a tracery post, we'll actually do it twice because bluesky has a different character limit than mastodon.

when you call generate_posts() you'll get a dict back with a ["long"] post and a ["short"] post. The short one is less than 260 characters or whatever, and is done in a stupid way.

### hashtags in bluesky

this is done better now.

### mentions

these are TODO, I think I need to figure out resolving DIDs from handles. Mainily need to do this because Breaking Govtech mentions itself.

---

this is all super embarassing, sorry.

--- 

I've kept the examples from the original atproto Python Bot starter thing in /examples/bluesky-python-bot in case you want to look, but honestly I should just delete them?