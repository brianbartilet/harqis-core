from typing import Type, TypeVar, cast

from behave.runner import Context

from web.services.core.contracts import IResponse

T = TypeVar("T")


class ApiServiceManager:

    __services = {}

    @staticmethod
    def add_service(service):
        ApiServiceManager.__services[type(service)] = service

    @staticmethod
    def get_service(type_service: Type[T]) -> T:
        return ApiServiceManager.__services.get(type_service, T)

    @staticmethod
    def save_response(context, response):
        context.response = response

    @staticmethod
    def get_response(context: Context, type_hook: Type[T]) -> IResponse[T]:
        return cast(type_hook, context.response)
