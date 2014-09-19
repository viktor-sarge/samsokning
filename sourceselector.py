# -*- coding: utf-8 -*-
import cgi
import Cookie
import os
import datetime
import json

'''
Manages the user's preference of sources to be searched.
'''
class SourceSelector:
    _selected_sources = []
    COOKIE_NAME = "sources"

    def __init__(self):
        form = cgi.FieldStorage()
        if "clearsources" in form:
            pass
        elif "source" in form:
            sources = form.getvalue("source")
            if isinstance(sources, list):
                self._selected_sources.extend([x.decode('utf-8') for x in sources])
            else:
                self._selected_sources.append(sources.decode('utf-8'))
        else:
            try:
                cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
                if cookie.has_key(self.COOKIE_NAME):
                    cookie_list = json.loads(cookie[self.COOKIE_NAME].value)
                    if isinstance(cookie_list, list):
                        self._selected_sources.extend(cookie_list)
            except (Cookie.CookieError, KeyError):
                pass

    def getCookie(self):
        if os.environ.has_key("HTTP_COOKIE"):
            cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        else:
            cookie = Cookie.SimpleCookie()
        cookie[self.COOKIE_NAME] = json.dumps(self._selected_sources)
        expiration = datetime.datetime.now() + datetime.timedelta(weeks=10)
        cookie[self.COOKIE_NAME]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        return cookie

    def getSelectedSources(self):
        return self._selected_sources

    def isSourceSelected(self, source):
        if len(self._selected_sources) == 0:
            return True
        return source.decode('utf-8') in self._selected_sources

sourceselector = SourceSelector()
