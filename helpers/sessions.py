# -*- coding: utf-8 -*-
#
# A hander implementing session management
# Session configuration defined in config files
#
# https://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
#
# Extend the session handler with a route handler to use it
#
# class MyRoute(SessionHandler):
#     def get(self):
#         self.session['foo'] = 'bar'
#         foo = self.session.get('foo')
#         self.response.write("Foo: %s" % foo)


from webapp2 import RequestHandler, cached_property
from webapp2_extras.sessions import get_store


class SessionHandler(RequestHandler):

    # Override dispatch method to get and save session data with every request
    def dispatch(self):
        self.session_store = get_store(request=self.request)
        try:
            RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    # Make session data available within handlers
    @cached_property
    def session(self):
        return self.session_store.get_session()