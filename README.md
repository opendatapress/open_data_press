GAE Boilerplate
===============

A boilerplate for Google App Engine using WebApp2.

It contains minimal structure for building an MVC application on GAE.

- `app.yaml` - The GAE config file
- `main.py` - The main application file
- `runtests.py` - Script to run unit tests
- `/conf` - Environment specific configuration files
- `/controllers` - Request handler classes
- `/docs` - Miscellaneous documentation files
- `/helpers` - Tools and utilities used throughout the application
- `/lib` - Third-party libraries bundled with this application
- `/models` - Model classes
- `/static` - Statically served content (images, css, js)
- `/tests` - Unit tests
- `/views` - Jinja2 templates


Configuration
-------------

The files in `/conf` allow application configuration values to be managed independently.

- `development.yaml` - Configuration for the development environment
- `production.yaml` - Configuration for the production environment
- `global.yaml` - Configuration for all environments

All config files must be valid [YAML documents][1].

Loading the appropriate configuration is handled by `helpers.config.load_config`.


Static Files
------------

The boilerplate comes bundled with the following useful static resources.

- [jQuery][3]
- [Twitter Bootstrap][4]
- [FontAwesome][5]
- [Humans.txt][6]

Serving static resources is usually configured in `app.yaml`.

Though it is possible to return static file content through a request handler.

    from helpers.views import static
    def error_404(request, response, exception):
      response.write(static('404.html'))
      response.set_status(404)


View Templates
--------------

Views use [Jinja2 templates][2].

Views can be rendered using the `helpers.views.render` method.

    from helpers.views import render
    class HomeRoute(RequestHandler):
        def get(self):
            data = {'message': 'Hello World!'}
            body = render('index.html', data)
            self.response.write(body)


Sessions
--------

A helper library exists to make session management easier.

        from helpers.sessions import SessionHandler
        class MyRoute(SessionHandler):
            def get(self):
                self.session['foo'] = 'bar'
                foo = self.session.get('foo')
                self.response.write("Foo: %s" % foo)


Unit Tests
----------

Tests are python modules in the `/tests` directory.
Module directories mut be named like `test_*` and contain and `__init__.py` file.
Test module files must be named like `test_*.py`.

Test can be run with the `runtest.py` script. Provide the GAE IDE path and the test module path as parameters.

    python runtests.py ~/google_appengine/ tests/


[1]: http://www.yaml.org/
[2]: http://jinja.pocoo.org/docs/
[3]: http://jquery.com/
[4]: http://twitter.github.com/bootstrap/
[5]: http://fortawesome.github.io/Font-Awesome/
[6]: http://humanstxt.org/