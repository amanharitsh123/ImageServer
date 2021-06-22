from . import db
from main import main
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(main, db)

manager = Manager(main)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()