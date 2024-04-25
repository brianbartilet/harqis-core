from abc import ABC
from core.utilities.logging.custom_logger import create_logger

# Create a logger for "Behave Hooks"
log = create_logger(logger_name="Behave Hooks")


class IBehaveHooks(ABC, object):
    """
    This is an abstract base class that defines the interface for Behave hooks.
    Behave hooks are used to set up and tear down test environments, among other things.
    Each method in this class is a hook that gets called at different points in the test execution.
    """

    @staticmethod
    def setup(context):
        """
        This hook is called to set up the test environment.
        """
        ...

    @staticmethod
    def process_feature_tags(feature):
        """
        This hook is called to process the tags of a feature.
        """
        ...

    @staticmethod
    def process_scenario_tags(scenario):
        """
        This hook is called to process the tags of a scenario.
        """
        ...

    @staticmethod
    def before_all(context):
        """
        This hook is called before all tests are executed.
        """
        ...

    @staticmethod
    def before_feature(context, feature):
        """
        This hook is called before a feature is tested.
        """
        ...

    @staticmethod
    def before_scenario(context, scenario):
        """
        This hook is called before a scenario is tested.
        """
        ...

    @staticmethod
    def before_step(context, step):
        """
        This hook is called before a step is tested.
        """
        ...

    @staticmethod
    def after_step(context, step):
        """
        This hook is called after a step is tested.
        """
        ...

    @staticmethod
    def after_scenario(context, scenario):
        """
        This hook is called after a scenario is tested.
        """
        ...

    @staticmethod
    def after_feature(context, feature):
        """
        This hook is called after a feature is tested.
        """
        ...

    @staticmethod
    def after_all(context):
        """
        This hook is called after all tests are executed.
        """
        ...
