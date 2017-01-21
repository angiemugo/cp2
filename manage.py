from flask_script import Server, Manager
from b_app import app

manager = Manager(app)

# runserver command
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'
    )
)

if __name__ == "__main__":
    manager.run()
