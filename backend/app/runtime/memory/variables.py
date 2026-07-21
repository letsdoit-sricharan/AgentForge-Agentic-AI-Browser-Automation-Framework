"""
Well-known runtime memory variable names.
"""

from enum import StrEnum


class RuntimeVariable(StrEnum):
    """
    Common runtime memory keys.

    Plugins may use additional custom keys as needed.
    """

    CITY = "city"
    MOVIE = "movie"
    THEATRE = "theatre"
    SHOW_TIME = "show_time"
    SEAT = "seat"

    PAYMENT_STATUS = "payment_status"
    PAYMENT_ID = "payment_id"

    CURRENT_URL = "current_url"

    DOWNLOAD_PATH = "download_path"

    TICKET_PATH = "ticket_path"

    RETRY_COUNT = "retry_count"
