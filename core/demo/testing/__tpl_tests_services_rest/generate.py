import argparse
import os
import time
from datetime import datetime

from core.apps.mustache.generators.rest import GENERATOR_PATH_REST
from core.apps.mustache.generators.rest.generate import TestGeneratorServiceRest

from core.apps.gpt.assistants.base import BaseAssistant
from core.apps.gpt.models.assistants.message import MessageCreate
from core.apps.gpt.models.assistants.run import RunCreate
from core.utilities.files import zip_folder, remove_files_with_patterns

if __name__ == '__main__':
    #  region Create the argument parser
    parser = argparse.ArgumentParser(description='Converts OpenAPI specs to test cases')
    parser.add_argument('--spec', type=str, default="tasks_api_specs.yaml",
                        help='The OpenAPI specifications file can be a YAML, JSON or URL')
    parser.add_argument('--gpt', action='store_true', default=True,
                        help='Set this flag to generate GPT generated test cases')
    #  endregion

    #  region Run Generated Code using Mustache
    generator = TestGeneratorServiceRest(source=parser.parse_args().spec)
    data = generator.load_source()

    generator.create_directories()
    generator.parse_spec(data)
    generator.write_files()
    #  endregion

    created_tests = generator.tests

    if parser.parse_args().gpt:
        #  region Create and load GPT assistant
        assistant = BaseAssistant()
        assistant.load()
        #  endregion

        #  region Archive and upload files

        zip_folder(GENERATOR_PATH_REST, 'mustache.zip')
        zip_folders = ['generated', 'specs']
        for folder in zip_folders:
            zip_folder(f'{folder}', f'{folder}.zip')

        files = assistant.upload_files(base_directory=os.getcwd(), file_patterns=['*.zip'])
        file_ids = [f.id for f in files]
        #  endregion

        #  region Load GPT instructions
        with open("GPT_INSTRUCTIONS.md", 'r') as file:
            instructions = file.read()

        if instructions:
            messages = [
                MessageCreate(role='user', content=f"Example data: {created_tests}"),
                MessageCreate(role='user', content=instructions, file_ids=file_ids),
            ]
            assistant.add_messages_to_thread(messages)

            trigger = RunCreate(assistant_id=assistant.properties.id,
                                tools=[{'type': 'code_interpreter'}],
                                temperature=0)

            assistant.run_thread(run=trigger, )
            assistant.wait_for_runs_to_complete()

            #  region Download GPT responses
            replies = assistant.get_replies()

            try:
                test_file = 'test_cases.log'
                target_file = replies[0].file_ids[0]
                assistant.download_file(target_file, test_file)
                with open(test_file, 'r') as file:
                    output = file.read()
            except IndexError:
                output = {}

            with open("GPT_RESPONSES.md", 'a') as file:
                now = datetime.now()
                file.write(f'\n#### {now.strftime('%Y-%m-%d %H:%M:%S')}\n')
                for reply in reversed(replies):
                    file.write(f'{reply.content[0].text.value}\n')
                file.write(f"\n```python\n{output}\n```")
                file.write(f'\n---\n')
            #  endregion

        #  endregion

    remove_files_with_patterns(['*.zip'])
