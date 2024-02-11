#!/usr/bin/python3
"""Defines unittests for my_models/custom_city.py.

Unittest classes:
    TestCustomCityInstantiation
    TestCustomCitySave
    TestCustomCityToDict
"""
import os
import my_models as my_models
import unittest
from datetime import datetime
from time import sleep
from my_models.custom_city import CustomCity


class TestCustomCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomCity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomCity, type(CustomCity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomCity(), my_models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomCity().unique_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomCity().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomCity().update_time))

    def test_state_id_is_public_class_attribute(self):
        custom_cy = CustomCity()
        self.assertEqual(str, type(CustomCity.state_id))
        self.assertIn("state_id", dir(custom_cy))
        self.assertNotIn("state_id", custom_cy.__dict__)

    def test_name_is_public_class_attribute(self):
        custom_cy = CustomCity()
        self.assertEqual(str, type(CustomCity.name))
        self.assertIn("name", dir(custom_cy))
        self.assertNotIn("name", custom_cy.__dict__)

    def test_two_cities_unique_ids(self):
        custom_cy1 = CustomCity()
        custom_cy2 = CustomCity()
        self.assertNotEqual(custom_cy1.unique_id, custom_cy2.unique_id)

    def test_two_cities_different_created_at(self):
        custom_cy1 = CustomCity()
        sleep(0.05)
        custom_cy2 = CustomCity()
        self.assertLess(custom_cy1.creation_time, custom_cy2.creation_time)

    def test_two_cities_different_updated_at(self):
        custom_cy1 = CustomCity()
        sleep(0.05)
        custom_cy2 = CustomCity()
        self.assertLess(custom_cy1.update_time, custom_cy2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        custom_cy = CustomCity()
        custom_cy.unique_id = "123456"
        custom_cy.creation_time = custom_cy.update_time = dt
        cy_str = custom_cy.__str__()
        self.assertIn("[CustomCity] (123456)", cy_str)
        self.assertIn("'unique_id': '123456'", cy_str)
        self.assertIn("'creation_time': " + dt_repr, cy_str)
        self.assertIn("'update_time': " + dt_repr, cy_str)

    def test_args_unused(self):
        custom_cy = CustomCity(None)
        self.assertNotIn(None, custom_cy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        custom_cy = CustomCity(unique_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(custom_cy.unique_id, "345")
        self.assertEqual(custom_cy.creation_time, dt)
        self.assertEqual(custom_cy.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomCity(unique_id=None, creation_time=None, update_time=None)


class TestCustomCitySave(unittest.TestCase):
    """Unittests for testing save method of the CustomCity class."""

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
        custom_cy = CustomCity()
        sleep(0.05)
        first_update_time = custom_cy.update_time
        custom_cy.save_data()
        self.assertLess(first_update_time, custom_cy.update_time)

    def test_two_saves(self):
        custom_cy = CustomCity()
        sleep(0.05)
        first_update_time = custom_cy.update_time
        custom_cy.save_data()
        second_update_time = custom_cy.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        custom_cy.save_data()
        self.assertLess(second_update_time, custom_cy.update_time)

    def test_save_with_arg(self):
        custom_cy = CustomCity()
        with self.assertRaises(TypeError):
            custom_cy.save_data(None)

    def test_save_updates_file(self):
        custom_cy = CustomCity()
        custom_cy.save_data()
        custom_cy_id = "CustomCity." + custom_cy.unique_id
        with open("file.json", "r") as f:
            self.assertIn(custom_cy_id, f.read())


class TestCustomCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the CustomCity class."""

    def test_to_dict_type(self):
        custom_cy = CustomCity()
        self.assertTrue(dict, type(custom_cy.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        custom_cy = CustomCity()
        self.assertIn("unique_id", custom_cy.to_dict())
        self.assertIn("creation_time", custom_cy.to_dict())
        self.assertIn("update_time", custom_cy.to_dict())
        self.assertIn("__class__", custom_cy.to_dict())

    def test_to_dict_contains_added_attributes(self):
        custom_cy = CustomCity()
        custom_cy.middle_name = "Holberton"
        custom_cy.my_number = 98
        self.assertEqual("Holberton", custom_cy.middle_name)
        self.assertIn("my_number", custom_cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        custom_cy = CustomCity()
        custom_cy_dict = custom_cy.to_dict()
        self.assertEqual(str, type(custom_cy_dict["unique_id"]))
        self.assertEqual(str, type(custom_cy_dict["creation_time"]))
        self.assertEqual(str, type(custom_cy

