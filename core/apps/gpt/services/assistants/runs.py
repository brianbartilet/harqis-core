from core.apps.gpt.base_service import BaseServiceHarqisGPT
from core.apps.gpt.constants.http_headers import HttpHeadersGPT
from core.apps.gpt.models.assistants.run import Run, RunCreate, ThreadRunCreate, RunStep, SubmitToolOutputs
from core.apps.gpt.models.assistants.common import ListQuery

from core.web.services.core.constants.http_methods import HttpMethod


class ServiceRuns(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Assistants API.
    https://platform.openai.com/docs/api-reference/runs
    """
    def __init__(self, config):
        """
        Initializes the ServiceAssistants instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceRuns, self).__init__(config)
        self.request\
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v1")\
            .add_uri_parameter('threads')

    def create_run(self, thread_id: str, payload: RunCreate):
        """
        Creates a new run.

        Args:
            thread_id: Thread ID
            payload: Data transfer object containing the run configuration.

        Returns:
            The created run as a Run object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs')\
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Run)

    def create_thread_and_run(self, payload: ThreadRunCreate):
        """
        Creates a new thread and runs it.

        Args:
            payload: Data transfer object containing the run configuration.

        Returns:
            The created run as a Run object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter('threads') \
            .add_uri_parameter('runs') \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Run)

    def get_runs(self, thread_id: str, query=ListQuery()):
        """
        Get runs by thread ID.

        Args:
            thread_id: Thread ID
            query: query object containing the list configuration.

        Returns:
            The runs as list of Run objects.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_json_body(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=list[Run])

    def get_run_steps(self, thread_id: str, run_id: str, query=ListQuery()):
        """
        Get run steps from run.

        Args:
            thread_id: Thread ID
            run_id: Run ID
            query: query object containing the list configuration.

        Returns:
            The steps as list of Run objects
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .add_uri_parameter('steps') \
            .add_json_body(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=list[RunStep])

    def get_run(self, thread_id: str, run_id: str):
        """
        Get thread object by ID.

        Args:
            thread_id: Thread ID
            run_id: Run ID

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .build()

        return self.client.execute_request(request, response_hook=Run)

    def get_run_step(self, thread_id: str, run_id: str, step_id: str):
        """
        Get run step of a run
        Args:
            thread_id: Thread ID
            run_id: Run ID
            step_id: Step ID

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .add_uri_parameter('steps') \
            .add_uri_parameter(step_id) \
            .build()

        return self.client.execute_request(request, response_hook=RunStep)

    def update_run(self, thread_id: str, run_id: str, payload: RunCreate):  # use .metadata only
        """
        Update run object by ID.

        Args:
            thread_id: Thread ID
            run_id: Run ID
            payload: Data transfer object containing the run configuration.

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Run)

    def submit_tool_options(self, thread_id: str, run_id: str, payload: SubmitToolOutputs):
        """
        Submit tool options for a run

        Args:
            thread_id: Thread ID
            run_id: Run ID
            payload: Data transfer object containing the thread's configuration.

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .add_uri_parameter('submit_tool_options') \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Run)

    def cancel_run(self, thread_id: str, run_id: str):
        """
        Cancel a run

        Args:
            thread_id: Thread ID
            run_id: Run ID

        Returns:
            The run object
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('runs') \
            .add_uri_parameter(run_id) \
            .add_uri_parameter('cancel') \
            .build()

        return self.client.execute_request(request, response_hook=Run)
