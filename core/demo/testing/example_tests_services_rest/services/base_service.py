from core.web.services.fixtures.rest import BaseFixtureServiceRest


class BaseServiceApp(BaseFixtureServiceRest):
    """
       Extends the BaseFixtureServiceRest to provide additional services tailored for the application.

       This class initializes the service application with specific configuration settings
       and any additional keyword arguments that might be necessary for the initialization of the base service.

       """
    def __init__(self, config, **kwargs):
        """
        Initialize the BaseServiceApp with configuration settings and other optional keyword arguments.

        Args:
            config: Configuration settings for the service application.
            **kwargs: Arbitrary keyword arguments that are passed to the parent class initializer.
        """
        super(BaseServiceApp, self).__init__(config=config, **kwargs)
