#!/usr/bin/python3
from models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = ""

    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.name)

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict["name"] = self.name
        return obj_dict
