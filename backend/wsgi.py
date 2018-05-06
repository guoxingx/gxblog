#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()


if __name__ == '__main__':

    import os
    from app import create_app
    app = create_app(os.getenv('APP_CONFIG') or 'test')

    from gevent.pywsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    @run_with_reloader
    def run():
        app.debug = True
        application = DebuggedApplication(app, evalex=True)
        server = WSGIServer(('0.0.0.0', 8000), application)
        server.serve_forever()
    run()
