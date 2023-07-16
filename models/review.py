#!/usr/bin/python3
from models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.place_id = ""
        self.user_id = ""
        self.text = ""

    def __str__(self):
        return "[{}] ({}) {} - {}".format(
            self.__class__.__name__, self.id, self.place_id, self.user_id
        )

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict["place_id"] = self.place_id
        obj_dict["user_id"] = self.user_id
        obj_dict["text"] = self.text
        return obj_dict
