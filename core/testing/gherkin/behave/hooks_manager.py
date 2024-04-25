from core.utilities.logging.custom_logger import create_logger
import sys
import os

log = create_logger(logger_name="Hooks Manager")


class BehaveHooksManager:
    """
    Manages hooks for Behave tests, providing a centralized registry of hooks to be executed during test runs.

    Attributes:
        hooks (list): A static list that stores hook functions to be executed at various stages of the test lifecycle.
    """
    hooks = []


def create_hook_function(hook_type):
    """
    Factory function that creates hook functions for different stages of the test lifecycle.

    Args:
        hook_type (str): A string that specifies the type of hook (e.g., 'before_all', 'after_feature').

    Returns:
        function: A function that executes the appropriate hooks for the given lifecycle stage.
    """
    def hook_function(context, feature_or_scenario=None):
        """
        Executes registered hooks for a specific test lifecycle stage, passing the necessary arguments.

        Args:
            context: The Behave context for the current test or scenario.
            feature_or_scenario (optional): The feature or scenario related to the current context, if applicable.
        """
        args = [context]
        if feature_or_scenario is not None:
            args.append(feature_or_scenario)
        _execute_hooks(hook_type, BehaveHooksManager.hooks, args)
    return hook_function


before_all = create_hook_function('before_all')
before_feature = create_hook_function('before_feature')
before_scenario = create_hook_function('before_scenario')
before_step = create_hook_function('before_step')
after_all = create_hook_function('after_all')
after_feature = create_hook_function('after_feature')
after_scenario = create_hook_function('after_scenario')
after_step = create_hook_function('after_step')


def _execute_hooks(method_name, hooks_sequence, context_arg_list):
    """
    Internal function that iterates through and executes each registered hook.

    Args:
        method_name (str): The name of the method corresponding to the current test lifecycle stage.
        hooks_sequence (list): A list of hook functions to execute.
        context_arg_list (list): Arguments to pass to the hook functions, typically including the test context.

    Handles exceptions by logging warnings, including the filename and line number where the exception occurred.
    """
    for hook in hooks_sequence:
        try:
            obj = hook()
            getattr(obj, method_name)(*context_arg_list)
        except AttributeError:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_hook_target = exc_tb.tb_next
            file = os.path.split(error_hook_target.tb_frame.f_code.co_filename)[1]
            line = error_hook_target.tb_lineno
            msg = str(exc_obj)
            log.warning(f"HOOKS EXCEPTION: {file} line: {line} message: {msg}\n")
