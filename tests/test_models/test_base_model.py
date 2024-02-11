#!/usr/bin/python3
"""Defines unittests for my_models/base_model.py.

Unittest classes:
    TestMyBaseModelInstantiation
    TestMyBaseModelSave
    TestMyBaseModelToDict
"""
import os
import my_models as my_models
import unittest
from datetime import datetime
from time import sleep
from my_models.my_base_model import MyBaseModel


class TestMyBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the MyBaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(MyBaseModel, type(MyBaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(MyBaseModel(), my_models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(MyBaseModel().custom_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(MyBaseModel().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(MyBaseModel().update_time))

    def test_two_models_unique_ids(self):
        bm1 = MyBaseModel()
        bm2 = MyBaseModel()
        self.assertNotEqual(bm1.custom_id, bm2.custom_id)

    def test_two_models_different_created_at(self):
        bm1 = MyBaseModel()
        sleep(0.05)
        bm2 = MyBaseModel()
        self.assertLess(bm1.creation_time, bm2.creation_time)

    def test_two_models_different_updated_at(self):
        bm1 = MyBaseModel()
        sleep(0.05)
        bm2 = MyBaseModel()
        self.assertLess(bm1.update_time, bm2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = MyBaseModel()
        bm.custom_id = "123456"
        bm.creation_time = bm.update_time = dt
        bmstr = bm.__str__()
        self.assertIn("[MyBaseModel] (123456)", bmstr)
        self.assertIn("'custom_id': '123456'", bmstr)
        self.assertIn("'creation_time': " + dt_repr, bmstr)
        self.assertIn("'update_time': " + dt_repr, bmstr)

    def test_args_unused(self):
        bm = MyBaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = MyBaseModel(custom_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(bm.custom_id, "345")
        self.assertEqual(bm.creation_time, dt)
        self.assertEqual(bm.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            MyBaseModel(custom_id=None, creation_time=None, update_time=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = MyBaseModel("12", custom_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(bm.custom_id, "345")
        self.assertEqual(bm.creation_time, dt)
        self.assertEqual(bm.update_time, dt)


class TestMyBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the MyBaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        bm = MyBaseModel()
        sleep(0.05)
        first_update_time = bm.update_time
        bm.save_data()
        self.assertLess(first_update_time, bm.update_time)

    def test_two_saves(self):
        bm = MyBaseModel()
        sleep(0.05)
        first_update_time = bm.update_time
        bm.save_data()
        second_update_time = bm.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        bm.save_data()
        self.assertLess(second_update_time, bm.update_time)

    def test_save_with_arg(self):
        bm = MyBaseModel()
        with self.assertRaises(TypeError):
            bm.save_data(None)

    def test_save_updates_file(self):
        bm = MyBaseModel()
        bm.save_data()
        bmid = "MyBaseModel." + bm.custom_id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestMyBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the MyBaseModel class."""

    def test_to_dict_type(self):
        bm = MyBaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bm = MyBaseModel()
        self.assertIn("custom_id", bm.to_dict())
        self.assertIn("creation_time", bm.to_dict())
        self.assertIn("update_time", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bm = MyBaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = MyBaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["creation_time"]))
        self.assertEqual(str, type(bm_dict["update_time"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bm = MyBaseModel()
        bm.custom_id = "123456"
        bm.creation_time = bm.update_time = dt
        tdict = {
            'custom_id': '123456',
            '__class__': 'MyBaseModel',
            'creation_time': dt.isoformat(),
            'update_time': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm =

