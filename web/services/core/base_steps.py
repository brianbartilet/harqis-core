from typing import Type, TypeVar, cast

from behave.runner import Context

from web.services.core.contracts.response import IResponse

Service = TypeVar("Service")


class ApiServiceManager:

    __services = {}

    @staticmethod
    def add_service(service):
        ApiServiceManager.__services[type(service)] = service

    @staticmethod
    def get_service(type_service: Type[Service]) -> Service:
        return ApiServiceManager.__services.get(type_service, Service)

    @staticmethod
    def save_response(context, response):
        context.response = response

    @staticmethod
    def get_response(context: Context, type_hook: Type[Service]) -> IResponse[Service]:
        return cast(type_hook, context.response)
