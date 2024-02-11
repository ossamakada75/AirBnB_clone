#!/usr/bin/python3
"""Defines unittests for my_models/custom_place.py.

Unittest classes:
    TestCustomPlaceInstantiation
    TestCustomPlaceSave
    TestCustomPlaceToDict
"""
import os
import my_models as my_models
import unittest
from datetime import datetime
from time import sleep
from my_models.custom_place import CustomPlace


class TestCustomPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomPlace class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomPlace, type(CustomPlace()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomPlace(), my_models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomPlace().unique_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomPlace().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomPlace().update_time))

    def test_city_id_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(str, type(CustomPlace.city_id))
        self.assertIn("city_id", dir(custom_pl))
        self.assertNotIn("city_id", custom_pl.__dict__)

    def test_user_id_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(str, type(CustomPlace.user_id))
        self.assertIn("user_id", dir(custom_pl))
        self.assertNotIn("user_id", custom_pl.__dict__)

    def test_name_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(str, type(CustomPlace.name))
        self.assertIn("name", dir(custom_pl))
        self.assertNotIn("name", custom_pl.__dict__)

    def test_description_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(str, type(CustomPlace.description))
        self.assertIn("description", dir(custom_pl))
        self.assertNotIn("desctiption", custom_pl.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(int, type(CustomPlace.number_rooms))
        self.assertIn("number_rooms", dir(custom_pl))
        self.assertNotIn("number_rooms", custom_pl.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(int, type(CustomPlace.number_bathrooms))
        self.assertIn("number_bathrooms", dir(custom_pl))
        self.assertNotIn("number_bathrooms", custom_pl.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(int, type(CustomPlace.max_guest))
        self.assertIn("max_guest", dir(custom_pl))
        self.assertNotIn("max_guest", custom_pl.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(int, type(CustomPlace.price_by_night))
        self.assertIn("price_by_night", dir(custom_pl))
        self.assertNotIn("price_by_night", custom_pl.__dict__)

    def test_latitude_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(float, type(CustomPlace.latitude))
        self.assertIn("latitude", dir(custom_pl))
        self.assertNotIn("latitude", custom_pl.__dict__)

    def test_longitude_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(float, type(CustomPlace.longitude))
        self.assertIn("longitude", dir(custom_pl))
        self.assertNotIn("longitude", custom_pl.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        custom_pl = CustomPlace()
        self.assertEqual(list, type(CustomPlace.amenity_ids))
        self.assertIn("amenity_ids", dir(custom_pl))
        self.assertNotIn("amenity_ids", custom_pl.__dict__)

    def test_two_places_unique_ids(self):
        custom_pl1 = CustomPlace()
        custom_pl2 = CustomPlace()
        self.assertNotEqual(custom_pl1.unique_id, custom_pl2.unique_id)

    def test_two_places_different_created_at(self):
        custom_pl1 = CustomPlace()
        sleep(0.05)
        custom_pl2 = CustomPlace()
        self.assertLess(custom_pl1.creation_time, custom_pl2.creation_time)

    def test_two_places_different_updated_at(self):
        custom_pl1 = CustomPlace()
        sleep(0.05)
        custom_pl2 = CustomPlace()
        self.assertLess(custom_pl1.update_time, custom_pl2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        custom_pl = CustomPlace()
        custom_pl.unique_id = "123456"
        custom_pl.creation_time = custom_pl.update_time = dt
        pl_str = custom_pl.__str__()
        self.assertIn("[CustomPlace] (123456)", pl_str)
        self.assertIn("'unique_id': '123456'", pl_str)
        self.assertIn("'creation_time': " + dt_repr, pl_str)
        self.assertIn("'update_time': " + dt_repr, pl_str)

    def test_args_unused(self):
        custom_pl = CustomPlace(None)
        self.assertNotIn(None, custom_pl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        custom_pl = CustomPlace(unique_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(custom_pl.unique_id, "345")
        self.assertEqual(custom_pl.creation_time, dt)
        self.assertEqual(custom_pl.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomPlace(unique_id=None, creation_time=None, update_time=None)


class TestCustomPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the CustomPlace class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        custom_pl = CustomPlace()
        sleep(0.05)
        first_update_time = custom_pl.update_time
        custom_pl.save_data()
        self.assertLess(first_update_time, custom_pl.update_time)

    def test_two_saves(self):
        custom_pl = CustomPlace()
        sleep(0.05)
        first_update_time = custom_pl.update_time
        custom_pl.save_data()
        second_update_time = custom_pl.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        custom_pl.save_data()
        self.assertLess(second_update_time, custom_pl.update_time)

    def test_save_with_arg(self):
        custom_pl = CustomPlace()
        with self.assertRaises(TypeError):
            custom_pl.save_data(None)

    def test_save_updates_file(self):
        custom_pl = CustomPlace()
        custom_pl.save_data()
        custom_pl_id = "CustomPlace." + custom_pl.unique_id
        with open("file.json", "r") as f:
            self.assertIn(custom_pl

