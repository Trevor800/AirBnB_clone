#!/usr/bin/python3

import unittest
from datetime import datetime
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def test_init(self):
        base_model = BaseModel()
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_save(self):
        base_model = BaseModel()
        initial_updated_at = base_model.updated_at
        base_model.save()
        self.assertNotEqual(initial_updated_at, base_model.updated_at)

    def test_to_dict(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()

        self.assertIsInstance(base_model_dict, dict)
        self.assertEqual(base_model_dict['__class__'], 'BaseModel')
        self.assertEqual(base_model_dict['id'], base_model.id)
        self.assertEqual(base_model_dict['created_at'], base_model.created_at.isoformat())
        self.assertEqual(base_model_dict['updated_at'], base_model.updated_at.isoformat())

    def test_delete(self):
        base_model = BaseModel()
        self.assertTrue(models.storage.all().get(base_model.__class__.__name__ + '.' + base_model.id))
        base_model.delete()
        self.assertIsNone(models.storage.all().get(base_model.__class__.__name__ + '.' + base_model.id))

    def test_str(self):
        base_model = BaseModel()
        base_model_str = str(base_model)

        self.assertIsInstance(base_model_str, str)
        self.assertIn(base_model.__class__.__name__, base_model_str)
        self.assertIn(base_model.id, base_model_str)

if __name__ == '__main__':
    unittest.main()
