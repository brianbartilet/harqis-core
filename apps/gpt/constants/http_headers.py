from enum import Enum


# This class is an enumeration for common HTTP header names.
# It is used to standardize the HTTP header names across the application.
# Currently, it only contains one member: OPEN_API_BETA.
class HttpHeadersGPT(Enum):
    """
    Enum for common HTTP header names.
    """
    # This member represents the "OpenAI-Beta" HTTP header.
    # It is used when making requests to the OpenAI API in its beta version.
    OPEN_API_BETA = "OpenAI-Beta"
