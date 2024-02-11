#!/usr/bin/python3
"""Defines unittests for my_models/custom_review.py.

Unittest classes:
    TestCustomReviewInstantiation
    TestCustomReviewSave
    TestCustomReviewToDict
"""
import os
import my_models as my_models
import unittest
from datetime import datetime
from time import sleep
from my_models.custom_review import CustomReview


class TestCustomReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomReview class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomReview, type(CustomReview()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomReview(), my_models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomReview().unique_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomReview().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomReview().update_time))

    def test_place_id_is_public_class_attribute(self):
        custom_rv = CustomReview()
        self.assertEqual(str, type(CustomReview.place_id))
        self.assertIn("place_id", dir(custom_rv))
        self.assertNotIn("place_id", custom_rv.__dict__)

    def test_user_id_is_public_class_attribute(self):
        custom_rv = CustomReview()
        self.assertEqual(str, type(CustomReview.user_id))
        self.assertIn("user_id", dir(custom_rv))
        self.assertNotIn("user_id", custom_rv.__dict__)

    def test_text_is_public_class_attribute(self):
        custom_rv = CustomReview()
        self.assertEqual(str, type(CustomReview.text))
        self.assertIn("text", dir(custom_rv))
        self.assertNotIn("text", custom_rv.__dict__)

    def test_two_reviews_unique_ids(self):
        custom_rv1 = CustomReview()
        custom_rv2 = CustomReview()
        self.assertNotEqual(custom_rv1.unique_id, custom_rv2.unique_id)

    def test_two_reviews_different_created_at(self):
        custom_rv1 = CustomReview()
        sleep(0.05)
        custom_rv2 = CustomReview()
        self.assertLess(custom_rv1.creation_time, custom_rv2.creation_time)

    def test_two_reviews_different_updated_at(self):
        custom_rv1 = CustomReview()
        sleep(0.05)
        custom_rv2 = CustomReview()
        self.assertLess(custom_rv1.update_time, custom_rv2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        custom_rv = CustomReview()
        custom_rv.unique_id = "123456"
        custom_rv.creation_time = custom_rv.update_time = dt
        rv_str = custom_rv.__str__()
        self.assertIn("[CustomReview] (123456)", rv_str)
        self.assertIn("'unique_id': '123456'", rv_str)
        self.assertIn("'creation_time': " + dt_repr, rv_str)
        self.assertIn("'update_time': " + dt_repr, rv_str)

    def test_args_unused(self):
        custom_rv = CustomReview(None)
        self.assertNotIn(None, custom_rv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        custom_rv = CustomReview(unique_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(custom_rv.unique_id, "345")
        self.assertEqual(custom_rv.creation_time, dt)
        self.assertEqual(custom_rv.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomReview(unique_id=None, creation_time=None, update_time=None)


class TestCustomReviewSave(unittest.TestCase):
    """Unittests for testing save method of the CustomReview class."""

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
        custom_rv = CustomReview()
        sleep(0.05)
        first_update_time = custom_rv.update_time
        custom_rv.save_data()
        self.assertLess(first_update_time, custom_rv.update_time)

    def test_two_saves(self):
        custom_rv = CustomReview()
        sleep(0.05)
        first_update_time = custom_rv.update_time
        custom_rv.save_data()
        second_update_time = custom_rv.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        custom_rv.save_data()
        self.assertLess(second_update_time, custom_rv.update_time)

    def test_save_with_arg(self):
        custom_rv = CustomReview()
        with self.assertRaises(TypeError):
            custom_rv.save_data(None)

    def test_save_updates_file(self):
        custom_rv = CustomReview()
        custom_rv.save_data()
        custom_rv_id = "CustomReview." + custom_rv.unique_id
        with open("file.json", "r") as f:
            self.assertIn(custom_rv_id, f.read())


class TestCustomReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the CustomReview class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(CustomReview().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        custom_rv = CustomReview()
        self.assertIn("unique_id", custom_rv.to_dict())
        self.assertIn("creation_time", custom_rv.to_dict())
        self.assertIn("update_time", custom_rv.to_dict())
        self.assertIn("__class__", custom_rv.to_dict())

    def test_to_dict_contains_added_attributes(self):
        custom_rv = CustomReview()
        custom_rv.middle_name = "Holberton"
        custom_rv.my_number = 98
        self.assertEqual("Holberton", custom_rv.middle_name)
        self.assertIn("my_number", custom_rv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        custom_rv = CustomReview()
        custom_rv_dict = custom_rv.to_dict()
        self.assertEqual(str, type(custom_rv_dict["unique_id"]))
        self.assertEqual(str, type(custom_rv_dict["creation_time"]))
        self.assertEqual(str, type(custom_rv_dict["update_time"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        custom_rv = CustomReview()
        custom_rv.unique_id = "123456"
        custom_rv.creation_time = custom_rv.update_time = dt
        tdict = {
            'unique_id': '123456',
            '__class__': 'CustomReview',
            'creation_time': dt.isoformat(),
            'update_time': dt.isoformat(),
        }
        self.assertDictEqual(custom_rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        custom_rv = CustomReview()
        self.assertNotEqual(custom_r

