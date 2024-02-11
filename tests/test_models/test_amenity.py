#!/usr/bin/python3
"""Defines unittests for custom_amenity.py.

Unittest classes:
    TestCustomAmenityInstantiation
    TestCustomAmenitySave
    TestCustomAmenityToDict
"""
import os
import custom_models as models
import unittest
from datetime import datetime
from time import sleep
from custom_models.custom_amenity import CustomAmenity


class TestCustomAmenityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomAmenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomAmenity, type(CustomAmenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomAmenity(), models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomAmenity().unique_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomAmenity().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomAmenity().update_time))

    def test_name_is_public_class_attribute(self):
        custom_am = CustomAmenity()
        self.assertEqual(str, type(CustomAmenity.name))
        self.assertIn("name", dir(CustomAmenity()))
        self.assertNotIn("name", custom_am.__dict__)

    def test_two_custom_amenities_unique_ids(self):
        am1 = CustomAmenity()
        am2 = CustomAmenity()
        self.assertNotEqual(am1.unique_id, am2.unique_id)

    def test_two_custom_amenities_different_created_at(self):
        am1 = CustomAmenity()
        sleep(0.05)
        am2 = CustomAmenity()
        self.assertLess(am1.creation_time, am2.creation_time)

    def test_two_custom_amenities_different_updated_at(self):
        am1 = CustomAmenity()
        sleep(0.05)
        am2 = CustomAmenity()
        self.assertLess(am1.update_time, am2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        custom_am = CustomAmenity()
        custom_am.unique_id = "123456"
        custom_am.creation_time = custom_am.update_time = dt
        amstr = custom_am.__str__()
        self.assertIn("[CustomAmenity] (123456)", amstr)
        self.assertIn("'unique_id': '123456'", amstr)
        self.assertIn("'creation_time': " + dt_repr, amstr)
        self.assertIn("'update_time': " + dt_repr, amstr)

    def test_args_unused(self):
        custom_am = CustomAmenity(None)
        self.assertNotIn(None, custom_am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        custom_am = CustomAmenity(unique_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(custom_am.unique_id, "345")
        self.assertEqual(custom_am.creation_time, dt)
        self.assertEqual(custom_am.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomAmenity(unique_id=None, creation_time=None, update_time=None)


class TestCustomAmenitySave(unittest.TestCase):
    """Unittests for testing save method of the CustomAmenity class."""

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
        custom_am = CustomAmenity()
        sleep(0.05)
        first_update_time = custom_am.update_time
        custom_am.save_data()
        self.assertLess(first_update_time, custom_am.update_time)

    def test_two_saves(self):
        custom_am = CustomAmenity()
        sleep(0.05)
        first_update_time = custom_am.update_time
        custom_am.save_data()
        second_update_time = custom_am.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        custom_am.save_data()
        self.assertLess(second_update_time, custom_am.update_time)

    def test_save_with_arg(self):
        custom_am = CustomAmenity()
        with self.assertRaises(TypeError):
            custom_am.save_data(None)

    def test_save_updates_file(self):
        custom_am = CustomAmenity()
        custom_am.save_data()
        amid = "CustomAmenity." + custom_am.unique_id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestCustomAmenityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the CustomAmenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(CustomAmenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        custom_am = CustomAmenity()
        self.assertIn("unique_id", custom_am.to_dict())
        self.assertIn("creation_time", custom_am.to_dict())
        self.assertIn("update_time", custom_am.to_dict())
        self.assertIn("__class__", custom_am.to_dict())

    def test_to_dict_contains_added_attributes(self):
        custom_am = CustomAmenity()
        custom_am.middle_name = "Holberton"
        custom_am.my_number = 98
        self.assertEqual("Holberton", custom_am.middle_name)
        self.assertIn("my_number", custom_am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        custom_am = CustomAmenity()
        custom_am_dict = custom_am.to_dict()
        self.assertEqual(str, type(custom_am_dict["unique_id"]))
        self.assertEqual(str, type(custom_am_dict["creation_time"]))
        self.assertEqual(str, type(custom_am_dict["update_time"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        custom_am = CustomAmenity()
        custom_am.unique_id = "123456"
        custom_am.creation_time = custom_am.update_time = dt
        am_dict = {
            'unique_id': '123456',
            '__class__': 'CustomAmenity',
            'creation_time': dt.isoformat(),
            'update_time': dt.isoformat(),
        }
        self.assertDictEqual(custom_am.to_dict(), am_dict)

    def test_contrast_to_dict_dunder_dict(self):
        custom_am = CustomAmenity()
        self.assertNotEqual(custom_am.to_dict(), custom_am.__dict
