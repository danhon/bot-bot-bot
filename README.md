# Tracery Bluesky and Mastodon Bot

Hi, here's a way to post a simple tracery bot to bluesky and mastodon.

This repo is forked from [Bluesky Python Bot](https://github.com/skygaze-ai/bot-python) and uses the [Mastodon Python API wrapper](https://github.com/halcy/Mastodon.py?tab=readme-ov-file).

## Using this

Completely at your own risk. You'll need uv, and then all you need to do is:
uv run bot.py

### setup
Copy .env.example into .env and 

* stick in what's needed to access your bluesky and mastodon account.
* supply a directory if you want to put your tracery json grammars somewhere.

in bot.py you'll need to set your grammars file if you don't want to inadvertently end up with posting star trek job listings.

### weird stuff

so when we generate a tracery post, we'll actually do it twice because bluesky has a different character limit than mastodon.

when you call generate_posts() you'll get a dict back with a ["long"] post and a ["short"] post. The short one is less than 260 characters or whatever, and is done in a stupid way.

### hashtags in bluesky

omg these were annoying and they're done in a super hacky way.

so on bluesky, hashtags are super smart and consist of marked-up text called a facet. facets are delimited by their start and ending bytes, and those bytes are annotated with a facet, in this case, a "tag". The facet itself has two attributes that we really care about: the presentation text of the facet (i.e. what you'd see, like #winning) and the underlying hashtag (i.e. winning), which sets up bluesky searches, etc.

the important thing to note here is that the presentation text of the facet can be different from the actual underlying hashtag. 

for this thing, *hashtags are presumed to be at the end of a generated post* because a) that's the structure of the tracery posts (i.e. text, followed by a number of hashtags) and b) I couldn't be bothered figuring out generalizing inline hashtags because the bluesky documentation for the textbuilder helper class kind of implies that you build the post text in sequence?

anyway, so we split the generated tracery post at the first hashtag (#) and assume everything after that is a hashtag. I told you this was stupid.

then we hackily set up an array of those hashtags and then use textbuilder to, um, add the tag facets to them. ta-da.

---

this is all super embarassing, sorry.