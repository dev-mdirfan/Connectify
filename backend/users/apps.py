from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig class for the 'users' app.

    This class represents the configuration for the 'users' app in the Django project.
    It sets the default auto field and defines a 'ready' method to import the signals module.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    
    def ready(self):
        import users.signals
