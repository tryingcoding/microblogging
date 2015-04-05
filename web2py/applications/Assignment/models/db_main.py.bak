# -*- coding: utf-8 -*-

db.define_table('news',Field('time_stamp',  'datetime', default=request.now, update=request.now),
                        Field('title','string', required=True, notnull=True),
                        Field('link', 'string', required=True, notnull=True),
                        Field('image_link', 'string', default='http://timesofindia.indiatimes.com/photo/34824568.cms'))

db.define_table('posts',Field('time_stamp',  'datetime', default=request.now, update=request.now),
                        Field('user_id', 'reference auth_user'),
                        Field('body','text', length = 140, required=True, notnull=True),
                        Field('votes', 'integer', default=0),
                        Field('news_id', 'reference news'))

db.define_table('comments',Field('time_stamp',  'datetime', default=request.now, update=request.now),
                        Field('user_id', 'reference auth_user'),
                        Field('body','text', length = 140, required=True, notnull=True),
                        Field('upvotes', 'integer', default=0),
                        Field('downvotes', 'integer', default=0),
                        Field('post_id', 'reference posts'))

db.define_table('date_string',Field('date_string', 'string'))

db.define_table('vote',
                Field('post_id','reference posts'),
                Field('up_down','integer'),
                Field('posted_on','datetime',readable=False,writable=False),
                Field('posted_by','reference auth_user',readable=False,writable=False))
auth.messages.logged_in = None
auth.messages.logged_out = None
