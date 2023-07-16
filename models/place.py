#!/usr/bin/python3
from models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_id = ""
        self.user_id = ""
        self.name = ""
        self.description = ""
        self.number_rooms = 0
        self.number_bathrooms = 0
        self.max_guest = 0
        self.price_by_night = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.amenity_ids = []

    def __str__(self):
        return "[{}] ({}) {} - {} - {}".format(
            self.__class__.__name__, self.id, self.name, self.city_id, self.user_id
        )

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict["city_id"] = self.city_id
        obj_dict["user_id"] = self.user_id
        obj_dict["name"] = self.name
        obj_dict["description"] = self.description
        obj_dict["number_rooms"] = self.number_rooms
        obj_dict["number_bathrooms"] = self.number_bathrooms
        obj_dict["max_guest"] = self.max_guest
        obj_dict["price_by_night"] = self.price_by_night
        obj_dict["latitude"] = self.latitude
        obj_dict["longitude"] = self.longitude
        obj_dict["amenity_ids"] = self.amenity_ids
        return obj_dict
