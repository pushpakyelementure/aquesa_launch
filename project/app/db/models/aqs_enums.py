from enum import Enum


# Define an Enum for a custom status
class user_status_enum(str, Enum):
    inactive = "inactive"
    active = "active"
    blocked = "blocked"


# Define an Enum for a role
class roles(str, Enum):
    owner = "owner"
    tenant = "tenant"
    family = "family"


class valve_status_enum(str, Enum):
    open = "open"
    close = "close"
    open_request = "open_request"
    close_request = "close_request"


class action_status_enum(str, Enum):
    open = "open"
    close = "close"
    open_request = "open_request"
    close_request = "close_request"


class flag_enum(str, Enum):
    success = "success"
    failure = "failure"
    requested = "requested"


class activity_type_enum(str, Enum):
    valve = "valve"
    leakage = "leakage"
    billing = "billing"
    limit = "limit"


class aggregation_enum(str, Enum):
    day = "day"
    week = "week"
    month = "month"
