# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if not auth.user:
        if request.cookies.has_key('mycookie'):
            value = request.cookies['mycookie'].value
            value = int(value)
            user = db.auth_user(value)
            auth.login_user(user)
            #redirect(URL('user'))
        else:
            redirect(URL('user'))
    else:
        response.cookies['mycookie'] = auth.user.id
        response.cookies['mycookie']['expires'] = 24 * 3600
        response.cookies['mycookie']['path'] = '/'
    row_list = news()
    return dict(message=T('Hello World'), row_list = row_list)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    row_list = news()
    return dict(form=auth(), row_list = row_list)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

def news():
    """
    fetch news from rss
    """
    from datetime import datetime
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentDate = str(currentDay) + '_' + str(currentMonth) + '_' + str(currentYear)
    sel=[db.date_string['date_string']]
    row=db(db.date_string.id == 24).select(*sel).first() # note the *
    storedDate = row.date_string
    if storedDate != currentDate:
        db(db.date_string.id == 24).update(date_string=currentDate)
        db.commit()
        feedparser = local_import('feedparser')
        from BeautifulSoup import BeautifulSoup
        d = feedparser.parse('http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&output=rss')
        for field in d['entries']:
            soup = BeautifulSoup(field['description'])
            tags=soup.findAll('img')
            image_link = tags[0]['src']
            link = field['link'].strip().split(';')[-1]
            title = field['title']
            db.news.insert(title=title,link=link,image_link=image_link)
        db.commit()
    sel=[db.news['id'], db.news['title'], db.news['link'], db.news['image_link']]
    rows = db(db.news.id > 0).select(*sel, orderby=~db.news.id, limitby=(0,10))

    row_list = rows.as_list()
    return row_list

def feed():
    """
    shows posts on a news
    """
    from datetime import datetime
    news_id = request.vars.id
    rows = db(db.posts.news_id == news_id).select(db.posts.ALL, orderby=(db.posts.upvotes-db.posts.downvotes - (db.posts.time_stamp)))
    row_list = rows.as_list()
    return dict(news_vars = request.vars, row_list = row_list)

def blog():
    """
    Writes Blog Post
    """
    db.posts.insert(user_id=auth.user.id, body=request.vars.blog, news_id=request.vars.id)
    redirect(URL('default','feed',vars=dict(id=request.vars.id)))
