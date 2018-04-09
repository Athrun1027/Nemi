from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

import models

from app_init import create_app
from app_config import Config


# Create thr app instance via Factory Method
app = create_app(Config)
# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create some new commands
manager.add_command("server", Server(host="*"))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(
        app=app,
        db=models.db,
        User=models.User,
        # Group=models.Group,
        Space=models.Space,
        Bucket=models.Bucket,
        File=models.File,
        Tag=models.Tag,
        Tag_File=models.tag_file,
        Server=Server
    )


if __name__ == '__main__':
    manager.run()
