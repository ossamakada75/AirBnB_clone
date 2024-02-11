#!/usr/bin/python3
"""Defines unittests for my_models/custom_state.py.

Unittest classes:
    TestCustomStateInstantiation
    TestCustomStateSave
    TestCustomStateToDict
"""
import os
import my_models as my_models
import unittest
from datetime import datetime
from time import sleep
from my_models.custom_state import CustomState


class TestCustomStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomState class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomState, type(CustomState()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomState(), my_models.storage.get_all_objects().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomState().unique_id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomState().creation_time))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomState().update_time))

    def test_name_is_public_class_attribute(self):
        custom_st = CustomState()
        self.assertEqual(str, type(CustomState.name))
        self.assertIn("name", dir(custom_st))
        self.assertNotIn("name", custom_st.__dict__)

    def test_two_states_unique_ids(self):
        custom_st1 = CustomState()
        custom_st2 = CustomState()
        self.assertNotEqual(custom_st1.unique_id, custom_st2.unique_id)

    def test_two_states_different_created_at(self):
        custom_st1 = CustomState()
        sleep(0.05)
        custom_st2 = CustomState()
        self.assertLess(custom_st1.creation_time, custom_st2.creation_time)

    def test_two_states_different_updated_at(self):
        custom_st1 = CustomState()
        sleep(0.05)
        custom_st2 = CustomState()
        self.assertLess(custom_st1.update_time, custom_st2.update_time)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        custom_st = CustomState()
        custom_st.unique_id = "123456"
        custom_st.creation_time = custom_st.update_time = dt
        st_str = custom_st.__str__()
        self.assertIn("[CustomState] (123456)", st_str)
        self.assertIn("'unique_id': '123456'", st_str)
        self.assertIn("'creation_time': " + dt_repr, st_str)
        self.assertIn("'update_time': " + dt_repr, st_str)

    def test_args_unused(self):
        custom_st = CustomState(None)
        self.assertNotIn(None, custom_st.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        custom_st = CustomState(unique_id="345", creation_time=dt_iso, update_time=dt_iso)
        self.assertEqual(custom_st.unique_id, "345")
        self.assertEqual(custom_st.creation_time, dt)
        self.assertEqual(custom_st.update_time, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomState(unique_id=None, creation_time=None, update_time=None)


class TestCustomStateSave(unittest.TestCase):
    """Unittests for testing save method of the CustomState class."""

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
        custom_st = CustomState()
        sleep(0.05)
        first_update_time = custom_st.update_time
        custom_st.save_data()
        self.assertLess(first_update_time, custom_st.update_time)

    def test_two_saves(self):
        custom_st = CustomState()
        sleep(0.05)
        first_update_time = custom_st.update_time
        custom_st.save_data()
        second_update_time = custom_st.update_time
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        custom_st.save_data()
        self.assertLess(second_update_time, custom_st.update_time)

    def test_save_with_arg(self):
        custom_st = CustomState()
        with self.assertRaises(TypeError):
            custom_st.save_data(None)

    def test_save_updates_file(self):
        custom_st = CustomState()
        custom_st.save_data()
        custom_st_id = "CustomState." + custom_st.unique_id
        with open("file.json", "r") as f:
            self.assertIn(custom_st_id, f.read())


class TestCustomStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the CustomState class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(CustomState().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        custom_st = CustomState()
        self.assertIn("unique_id", custom_st.to_dict())
        self.assertIn("creation_time", custom_st.to_dict())
        self.assertIn("update_time", custom_st.to_dict())
        self.assertIn("__class__", custom_st.to_dict())

    def test_to_dict_contains_added_attributes(self):
        custom_st = CustomState()
        custom_st.middle_name = "Holberton"
        custom_st.my_number = 98
        self.assertEqual("Holberton", custom_st.middle_name)
        self.assertIn("my_number", custom_st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        custom_st = CustomState()
        custom_st_dict = custom_st.to_dict()
        self.assertEqual(str, type(custom_st_dict["unique_id"]))
        self.assertEqual(str, type(custom_st_dict["creation_time"]))
        self.assertEqual(str, type(custom_st_dict["update_time"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        custom_st = CustomState()
        custom_st.unique_id = "123456"
        custom_st.creation_time = custom_st.update_time = dt
        tdict = {
            'unique_id': '123456',
            '__class__': 'CustomState',
            'creation_time': dt.isoformat(),
            'update_time': dt.isoformat(),
        }
        self.assertDictEqual(custom_st.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        custom_st = CustomState()
        self.assertNotEqual(custom_st.to_dict(), custom_st.__dict__)

    def test_to_dict_with_arg(self):
        custom_st = CustomState()
        with self.assertRaises(TypeError):
            custom_st.to_dict(None)


if __name__ == "__main__":
    unittest.main()

