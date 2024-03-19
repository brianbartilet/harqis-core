from typing_extensions import override
from openai import AssistantEventHandler
from utilities.logging.custom_logger import create_logger


class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.logger = create_logger(self.__class__.__name__)

    @override
    def on_text_created(self, text) -> None:
        self.logger.info(f"\nassistant > {text}\n", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.logger.info(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        self.logger.info(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                self.logger.info(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                self.logger.info(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.logger.info(f"\n{output.logs}", flush=True)


class StreamEventHandler:
    def __init__(self, stream):
        self.stream = stream

    def process_events(self):
        for event in self.stream.data:
            self.handle_event(event)

    def handle_event(self, event):
        # Process the event here
        print(event)
        # You can add more logic to handle different types of events

