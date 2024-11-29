from typing import NamedTuple


class UserCart(NamedTuple):

    pk: int = 0
    name: str = "no_name"
    email: str = "no_email"
    gender: str = "no_gender"
    refrence_id: int = None
    # status: str = "no_status"


class UserApp(NamedTuple):

    pk: int = 0
    name: str = "no_name"
    email: str = "no_email"
    gender: str = "no_gender"
    refrence_id: int = None
    # status: str = "no_status"


class Parellel(NamedTuple):

    pk: int = 0
    name: str = "no_name"
    email: str = "no_email"
    gender: str = "no_gender"
    refrence_id: int = None
    # status: str = "no_status"

class UserAppPost(NamedTuple):

    pk: int = 0
    name: str = "no_name"
    email: str = "no_email"
    gender: str = "no_gender"
    refrence_id: int = None