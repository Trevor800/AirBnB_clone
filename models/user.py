#!/usr/bin/python3
from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""

    def __str__(self):
        return "[{}] ({}) {} - {} - {}".format(
            self.__class__.__name__, self.id, self.email, self.first_name, self.last_name
        )

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict["email"] = self.email
        obj_dict["password"] = self.password
        obj_dict["first_name"] = self.first_name
        obj_dict["last_name"] = self.last_name
        return obj_dict
