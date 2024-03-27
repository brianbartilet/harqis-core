import unittest

from core.apps.gpt.assistants.base import BaseAssistant
from core.apps.gpt.dto.assistants.message import DtoMessageCreate
from core.apps.gpt.dto.assistants.run import DtoRunCreate

from core.utilities.data.qlist import QList


class TestServiceAssistant(unittest.TestCase):

    def test_simple_flow(self):
        assistant = BaseAssistant()
        assistant.load()
        messages = [
            DtoMessageCreate(role='user', content='100'),
            DtoMessageCreate(role='user', content='101'),
            DtoMessageCreate(role='user', content='132')
            ]

        assistant.add_messages_to_thread(messages)

        trigger = DtoRunCreate(assistant_id=assistant.properties.id,
                               instructions='Add all numbers. Give me numeric value only.')
        assistant.run_thread(run=trigger)
        assistant.wait_for_runs_to_complete()

        replies = assistant.get_replies()
        answer = QList(replies).first()
        self.assertEqual(answer.content[0].text.value, '333')


