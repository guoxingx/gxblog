#!/usr/bin/env python

import os
from app import create_app
from app import db
from flask_script import Manager
from flask_script import Shell, Server
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('APP_CONFIG') or 'test')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
