#!/usr/bin/python3
"""
    Unittests for Review model.
    Classes for Unittest:
        TestReview_instantiation
        TestReview_save
        TestReview_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Testing the instantiation of Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_ispublic_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rvw))
        self.assertNotIn("place_id", rvw.__dict__)

    def test_user_id_ispublic_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rvw))
        self.assertNotIn("user_id", rvw.__dict__)

    def test_text_ispublic_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rvw))
        self.assertNotIn("text", rvw.__dict__)

    def test_2_reviews_unique_ids(self):
        rvw_1 = Review()
        rvw_2 = Review()
        self.assertNotEqual(rvw_1.id, rvw_2.id)

    def test_2_reviews_different_created_at(self):
        rvw_1 = Review()
        sleep(0.05)
        rvw_2 = Review()
        self.assertLess(rvw_1.created_at, rvw_2.created_at)

    def test_2_reviews_different_updated_at(self):
        rvw_1 = Review()
        sleep(0.05)
        rvw_2 = Review()
        self.assertLess(rvw_1.updated_at, rvw_2.updated_at)

    def test_str_representation(self):
        date_t = datetime.today()
        date_t_repr = repr(date_t)
        rvw = Review()
        rvw.id = "123456"
        rvw.created_at = rvw.updated_at = date_t
        rvstr = rvw.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + date_t_repr, rvstr)
        self.assertIn("'updated_at': " + date_t_repr, rvstr)

    def test_args_unused(self):
        rvw = Review(None)
        self.assertNotIn(None, rvw.__dict__.values())

    def test_init_with_kwargs(self):
        date_t = datetime.today()
        date_t_iso = date_t.isoformat()
        rvw = Review(id="345", created_at=date_t_iso, updated_at=date_t_iso)
        self.assertEqual(rvw.id, "345")
        self.assertEqual(rvw.created_at, date_t)
        self.assertEqual(rvw.updated_at, date_t)

    def test_init_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Testing the save method of Review class."""

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

    def test_1_save(self):
        rvw = Review()
        sleep(0.05)
        first_updated_at = rvw.updated_at
        rvw.save()
        self.assertLess(first_updated_at, rvw.updated_at)

    def test_2_saves(self):
        rvw = Review()
        sleep(0.05)
        first_updated_at = rvw.updated_at
        rvw.save()
        second_updated_at = rvw.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rvw.save()
        self.assertLess(second_updated_at, rvw.updated_at)

    def test_save_with_arg(self):
        rvw = Review()
        with self.assertRaises(TypeError):
            rvw.save(None)

    def test_save_updates_file(self):
        rvw = Review()
        rvw.save()
        rvid = "Review." + rvw.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Testing to_dict method of Review class."""

    def test_to_dicttype(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_todict_contains_correct_keys(self):
        rvw = Review()
        self.assertIn("id", rvw.to_dict())
        self.assertIn("created_at", rvw.to_dict())
        self.assertIn("updated_at", rvw.to_dict())
        self.assertIn("__class__", rvw.to_dict())

    def test_todict_contains_added_attrb(self):
        rvw = Review()
        rvw.middle_name = "ALXAfrica"
        rvw.my_number = 98
        self.assertEqual("ALXAfrica", rvw.middle_name)
        self.assertIn("my_number", rvw.to_dict())

    def test_todict_datetime_attrb_are_strs(self):
        rvw = Review()
        rv_dict = rvw.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_todict_output(self):
        date_t = datetime.today()
        rvw = Review()
        rvw.id = "123456"
        rvw.created_at = rvw.updated_at = date_t
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': date_t.isoformat(),
            'updated_at': date_t.isoformat(),
        }
        self.assertDictEqual(rvw.to_dict(), tdict)

    def test_contrast_todict_dunder_dict(self):
        rvw = Review()
        self.assertNotEqual(rvw.to_dict(), rvw.__dict__)

    def test_todict_with_arg(self):
        rvw = Review()
        with self.assertRaises(TypeError):
            rvw.to_dict(None)


if __name__ == "__main__":
    unittest.main()
