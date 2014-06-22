#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from platform import node

IS_LOCAL = bool(node() == 'Altynai-MacBook-Pro.local')

AUTHOR = u'Altynai'
SITENAME = u'Sideways'

if IS_LOCAL:
    SITEURL = 'http://localhost:8000'
else:
    SITEURL = 'http://Altynai.me'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social widget
SOCIAL = (
    ('github', 'https://github.com/Altynai'),
    ('weibo', 'http://weibo.com/u/2164187874'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISQUS_SITENAME = u"Sideways"

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
