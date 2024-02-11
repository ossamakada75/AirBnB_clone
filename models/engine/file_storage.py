#!/usr/bin/python3
"""Module for FileStorage class."""
import datetime
import json
import os


class CustomFileStorage:

    """Class for storing and retrieving data"""
    __file_path = "custom_file.json"
    __objects = {}

    def get_all_objects(self):
        """Returns the dictionary __objects"""
        return CustomFileStorage.__objects

    def add_new_object(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        CustomFileStorage.__objects[key] = obj

    def save_data(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(CustomFileStorage.__file_path, "w", encoding="utf-8") as file:
            data = {key: value.to_dict() for key, value in CustomFileStorage.__objects.items()}
            json.dump(data, file)

    def get_valid_classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload_data(self):
        """Reloads the stored objects"""
        if not os.path.isfile(CustomFileStorage.__file_path):
            return
        with open(CustomFileStorage.__file_path, "r", encoding="utf-8") as file:
            obj_dict = json.load(file)
            obj_dict = {key: self.get_valid_classes()[value["__class__"]](**value)
                        for key, value in obj_dict.items()}
            CustomFileStorage.__objects = obj_dict

    def get_valid_attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                {"id": str,
                 "created_at": datetime.datetime,
                 "updated_at": datetime.datetime},
            "User":
                {"email": str,
                 "password": str,
                 "first_name": str,
                 "last_name": str},
            "State":
                {"name": str},
            "City":
                {"state_id": str,
                 "name": str},
            "Amenity":
                {"name": str},
            "Place":
                {"city_id": str,
                 "user_id": str,
                 "name": str,
                 "description": str,
                 "number_rooms": int,
                 "number_bathrooms": int,
                 "max_guest": int,
                 "price_by_night": int,
                 "latitude": float,
                 "longitude": float,
                 "amenity_ids": list},
            "Review":
                {"place_id": str,
                 "user_id": str,
                 "text": str}
        }
        return attributes

