#!/usr/bin/python3
from models.base_model import BaseModel


class City(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state_id = ""
        self.name = ""

    def __str__(self):
        return "[{}] ({}) {} - {}".format(
            self.__class__.__name__, self.id, self.name, self.state_id
        )

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict["state_id"] = self.state_id
        obj_dict["name"] = self.name
        return obj_dict
