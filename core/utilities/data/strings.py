import re
from typing import Type, TypeVar, List
import textwrap

TObject = TypeVar('TObject')


def convert_to_snake_case(stream: str) -> str:
    """
    Convert a given text from camelCase or PascalCase to snake_case.

    Args:
        stream: The text to be converted.

    Returns:
        The text in snake_case.
    """
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', stream)
    return '_'.join(word.lower() for word in words)


def convert_dict_keys_to_snake(cur_object: TObject) -> TObject:
    """
    Convert the keys of a dictionary representing an object's attributes to snake_case.

    Args:
        cur_object: The object whose attributes need to be converted.

    Returns:
        A new object with attributes in snake_case.
    """
    object_type = type(cur_object)
    obj_dict = cur_object.__dict__
    for key, value in obj_dict.copy().items():
        snake_case_key = convert_to_snake_case(key)
        if snake_case_key != key:
            obj_dict[snake_case_key] = obj_dict.pop(key)
    new_obj = object_type(**obj_dict)
    return new_obj


def convert_objects_to_snake(object_collection: List[TObject]) -> List[TObject]:
    """
    Convert the keys of dictionaries representing a list of objects' attributes to snake_case.

    Args:
        object_collection: The list of objects whose attributes need to be converted.

    Returns:
        A new list of objects with attributes in snake_case.
    """
    return [convert_dict_keys_to_snake(item) for item in object_collection]


def convert_object_keys_to_snake(object_item: TObject) -> TObject:
    """
    Convert the keys of a dictionary or a list of dictionaries representing an object's or objects' attributes to snake_case.

    Args:
        object_item: The object or list of objects whose attributes need to be converted.

    Returns:
        The object or list of objects with attributes in snake_case.
    """
    if isinstance(object_item, list):
        return convert_objects_to_snake(object_item)
    else:
        return convert_dict_keys_to_snake(object_item)


def convert_dict_values_to_snake(data: dict) -> TObject:
    """
    Convert the values of a dictionary representing an object's attributes to snake_case.
    Args:
        data: The dictionary whose attributes need to be converted.
    """
    for key in data.keys():
        try:
            data[key] = convert_to_snake_case(data[key])
        except TypeError:
            data[key] = data[key]

    return data


def convert_object_list(object_collection: List, object_type: Type[TObject]) -> List[TObject]:
    """
    Convert a list of objects to a new list of objects of a specific type.

    Args:
        object_collection: The list of objects to be converted.
        object_type: The new type of objects.

    Returns:
        A new list of objects of the specified type.
    """
    return [object_type(**item.__dict__) for item in object_collection]


def remove_special_chars(input_string):
    """
    Removes special characters from the input string, retaining only letters and numbers.

    Args:
        input_string (str): The string from which to remove special characters.

    Returns:
        str: A new string with special characters removed.
    """
    # This regular expression matches anything that is NOT a letter or number.
    return re.sub(r'[^a-zA-Z0-9]', '', input_string)


def wrap_text(strings: list, width=65, line_breaks=True, indent_paragraphs=True, indent="\t") -> str:
    """
    Wraps text to a specific width, optionally inserting paragraph breaks
    after sentence-ending punctuation AND applying paragraph indentation.

    Args:
        strings (list): List of text parts to combine.
        width (int): Maximum characters per line before wrapping.
        line_breaks (bool): Insert line breaks after sentences.
        indent_paragraphs (bool): Indent new paragraphs.
        indent (str): The indent string (default: 4 spaces).
    """
    # Combine into one large string
    text = " ".join(strings).strip()

    words = text.split()
    lines = []
    current_line = ""
    new_paragraph = True  # First line should be indented

    def sentence_ended(w):
        return w.endswith(('.', '!', '?'))

    for word in words:
        # If starting new paragraph, ensure indent is applied
        if new_paragraph:
            current_line = indent
            new_paragraph = False

        # Check if adding the word exceeds width
        if len(current_line) + len(word) + (1 if current_line.strip() else 0) > width:
            lines.append(current_line)
            current_line = indent + word if indent_paragraphs else word
        else:
            if current_line.strip():  # If not empty except indent
                current_line += " " + word
            else:
                current_line += word

        # If sentence ends → force paragraph break
        if line_breaks and sentence_ended(word):
            lines.append(current_line)
            current_line = ""
            new_paragraph = indent_paragraphs  # Next line begins a paragraph

    # Append final line
    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

def make_separator(count=100):
    """
    Creates a string separator consisting of a specified number of '=' characters."""
    s = ""
    for _ in range(count):
        s += "="
    return s