from pydantic import Basemodel


class User(Basemodel):
    user_id: int
    email: str
    lastname: str
    national_id: int
    IP: str
    image1: str
    image2: str
    state: str
