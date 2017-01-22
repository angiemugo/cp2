from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager

from b_app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# runserver command
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'
    )
)

# db management commands
manager.add_command('db',  MigrateCommand)

if __name__ == "__main__":
    manager.run()
