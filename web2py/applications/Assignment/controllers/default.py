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
            auth.user = db(db.auth_user.id==value).select()[0]
            #redirect(URL('user'))
        else:
            redirect(URL('user'))
    else:
        response.cookies['mycookie'] = auth.user.id
        response.cookies['mycookie']['expires'] = 24 * 3600
        response.cookies['mycookie']['path'] = '/'
    out = news_index()
    return dict(message=T('Hello World'), trending = out)


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
    out = news()
    return dict(form=auth(), trending = out)


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
    feedparser = local_import('feedparser')
    from BeautifulSoup import BeautifulSoup
    d = feedparser.parse('http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&output=rss')
    out = '<ul style="list-style: none;">\n'
    for field in d['entries']:
        out += '<li><a href="#" onClick="jQuery(\'.flash\').html(\'Sign in to view or participate in discussion!\').slideDown().delay(1000).fadeOut()" style="color:green; font-family:verdana; font-size:100%">'
        soup = BeautifulSoup(field['description'])
        tags=soup.findAll('img')
        out += (str(tags[0]).strip()[:-1] + ' align = middle>')
        out += ('     ' + field['title'])
        #out += '<li>'
        #out += field['description']
        #out += '</li>'
        out += '</a></li>'
    out += '</ul>'
    return out

def news_index():
    """
    fetch news from rss
    """
    feedparser = local_import('feedparser')
    from BeautifulSoup import BeautifulSoup
    d = feedparser.parse('http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&output=rss')
    out = '<ul style="list-style: none;">\n'
    for field in d['entries']:
        out += '<li><a href="#" style="color:green; font-family:verdana; font-size:130%">'
        soup = BeautifulSoup(field['description'])
        tags=soup.findAll('img')
        out += (str(tags[0]).strip()[:-1] + ' align = middle>')
        out += ('     ' + field['title'])
        out += '</a></li><br>'
    out += '</ul>'
    return out
