#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Altynai'
SITENAME = u'Sideways'

SITEURL = 'http://Altynai.me'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social widget
SOCIAL = (
    ('github', 'https://github.com/Altynai'),
    ('weibo', 'http://weibo.com/u/2164187874'),
    ('rss', "%s/feeds/all.rss.xml" % SITEURL),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISQUS_SITENAME = 'altynai'

TAGLINE = "Reflections on life, code, movie, and the craft of writing.."

# Categorys & Pages on menu
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True

# Themes
THEME = "theme/"

# Article Url
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Plugins
PLUGIN_PATH = '/Users/chenjiapeng/project/pelican-plugins'
PLUGINS = ['render_math', ]
