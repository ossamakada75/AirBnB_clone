#!/usr/bin/python3
"""This script defines the base model"""

import uuid
from datetime import datetime
from models import storage


class CustomBaseModel:

    """Class from which all other classes will inherit"""

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes

        Args:
            - *args: List of arguments
            - **kwargs: Dictionary of key-value arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.unique_id = str(uuid.uuid4())
            self.creation_time = datetime.now()
            self.update_time = datetime.now()
            storage.add_new_object(self)

    def __str__(self):
        """Returns official string representation"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.unique_id, self.__dict__)

    def save_data(self):
        """Updates the public instance attribute update_time"""

        self.update_time = datetime.now()
        storage.save_data()

    def to_dict_representation(self):
        """Returns a dictionary containing all keys/values of __dict__"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["creation_time"] = my_dict["creation_time"].isoformat()
        my_dict["update_time"] = my_dict["update_time"].isoformat()
        return my_dict
