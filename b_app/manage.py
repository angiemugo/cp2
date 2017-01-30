from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager, Shell
from resources import app, db, models


migrate = Migrate(app, db)
manager = Manager(app)

# runserver command
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True
    )
)

 # points the shell command to db and models
def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("shell", Shell(make_context=_make_context))

# db management commands
manager.add_command('db',  MigrateCommand)


if __name__ == "__main__":
    manager.run()
