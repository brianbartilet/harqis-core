from typing import Type, TypeVar, Dict, Any, Iterable

from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.core.contracts.response import IResponse

from core.utilities.logging.custom_logger import create_logger

T = TypeVar('T')


class WebServiceManager:
    """
    Manages web service instances and their responses, facilitating easy access and interaction
    with various web services. It uses a common configuration for initializing these services and
    provides methods to store and retrieve responses from operations performed by these services.

    Attributes:
        config (AppConfigWSClient): Configuration object used for service initialization.
        services (Dict[Type[T], T]): Dictionary holding initialized service instances.
        responses (Dict[str, Any]): Storage for responses, keyed by unique identifiers.
        kwargs (dict): Additional keyword arguments that might be used for service initialization.
    """
    def __init__(self, config: AppConfigWSClient, register: Iterable[Type[T]] = None, **kwargs):
        """
        Initializes the WebServiceManager with a configuration object and an optional
        dictionary of pre-initialized services.

        Args:
            config: Configuration object necessary for initializing services.
            register: Optional dictionary of service types to pre-initialized service instances.
            **kwargs: Additional keyword arguments for future extensions or custom initialization logic.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.config = config
        self.services: Dict[Type[T], T] = {}
        self.responses: Dict[str, Any] = {}
        self.kwargs = kwargs

        if register is not None:
            for service_type in register:
                service_instance = service_type(self.config, **kwargs)
                self.services[service_type] = service_instance

    def register(self, service_type: Type[T], config: AppConfigWSClient = None, **kwargs) -> None:
        """
        Registers a pre-initialized service instance with the manager.

        Args:
            service_type: The type (class) of the service to be registered.
            config: pass config if available
        """
        use_config = config if config is not None else self.config

        self.services[service_type] = service_type(use_config, **kwargs)

    def get(self, service_type: Type[T]) -> T:
        """
        Retrieves or initializes a service instance of the specified type.

        Args:
            service_type: The type (class) of the service to be retrieved or initialized.

        Returns:
            An instance of the specified service type.
        """
        # Check if the instance already exists
        if service_type not in self.services:
            # Initialize the service with the stored configuration
            self.log.info(f"Add service to manager: {service_type.__name__}")
            service_instance = service_type(self.config)
            self.services[service_type] = service_instance

        return self.services[service_type]

    def save_response(self, identifier: str, response: IResponse) -> None:
        """
        Saves a response object with a specified identifier for later retrieval.

        Args:
            identifier: Unique identifier for the response.
            response: The response object to be saved.
        """
        self.responses[identifier] = response

    def get_response(self, identifier: str) -> Any:
        """
        Retrieves a previously saved response by its identifier.

        Args:
            identifier: The unique identifier of the response to retrieve.

        Returns:
            The response associated with the identifier, or None if not found.
        """
        return self.responses.get(identifier, None)


