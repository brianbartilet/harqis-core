"""
This module configures and utilizes the Celery application `SPROUT` for task execution, importing all tasks from the `workflows.builder.tasks` module.

The import centralizes task definitions within the `workflows.builder.tasks` module, enabling direct execution of these tasks from other modules in the application without individual redefinitions or imports. This design supports a cleaner and more maintainable codebase by adhering to the DRY (Don't Repeat Yourself) principle.

Tasks defined in `workflows.builder.tasks` are designed for asynchronous operations, including data processing functions and scheduled activities essential for the application's workflow automation. Through the import of these tasks, the module engages the `SPROUT` Celery application to manage task execution asynchronously across different worker processes.

Usage:
- Invoke a task imported from `workflows.builder.tasks` using the `SPROUT` Celery application for task scheduling and execution. For example, execute `SPROUT.send_task('some_task_name', args=[arg1, arg2])` for asynchronous operation, where 'some_task_name' corresponds to the name of the task you intend to execute.
- Ensure Celery worker processes are active and configured to listen on the correct queues for task execution. The `SPROUT` application should be started with the appropriate command and configurations to facilitate this.

Note:
- While the `*` import pattern imports all task names not starting with an underscore (`_`), it's advisable to list imported tasks explicitly if the module encompasses a large number of tasks or if only a specific subset is necessary. This practice enhances code readability and minimizes the risk of namespace collisions.
- The `SPROUT.send_task` method allows for task invocation by name, providing flexibility in task management and execution across distributed environments.

Additionally, the module imports the `SPROUT` configuration from `workflows.builder.config`, ensuring that task execution is aligned with the predefined settings of the Celery application.
"""
import importlib

# Read the environment variable to determine which tasks module to import
from core.config.env_variables import ENV_WORKFLOW_CONFIG, get_env_variable_value

try:
    # Dynamically import the tasks module based on the environment variable
    tasks_module = importlib.import_module(get_env_variable_value(ENV_WORKFLOW_CONFIG))
except AttributeError:
    raise ImportError(f"Environment variable ENV_WORKFLOW_CONFIG is not set or invalid.")


# Import the SPROUT configuration from the dynamically imported tasks module
# Ensure your tasks modules have a consistent interface/structure for SPROUT
SPROUT = getattr(tasks_module, 'SPROUT', None)

# If needed, dynamically import tasks or other symbols from the tasks module
# Example: SomeTask = getattr(tasks_module, 'SomeTask', None)

# Include a check to ensure SPROUT is not None to handle import errors gracefully
if SPROUT is None:
    raise ImportError(f"Failed to import 'SPROUT' from '{ENV_WORKFLOW_CONFIG}'")
