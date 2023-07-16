#!/usr/bin/python3
from datetime import datetime
import uuid

def create_base_model(**kwargs):
    base_model = {
        'id': str(uuid.uuid4()),
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    base_model.update(kwargs)
    
    def __str__():
        return "[{}] ({}) {}".format(base_model['__class__'], base_model['id'], base_model)
    
    def save():
        base_model['updated_at'] = datetime.now()
    
    def to_dict():
        obj_dict = base_model.copy()
        obj_dict['__class__'] = base_model['__class__']
        obj_dict['created_at'] = base_model['created_at'].isoformat()
        obj_dict['updated_at'] = base_model['updated_at'].isoformat()
        return obj_dict
    
    base_model['__str__'] = __str__
    base_model['save'] = save
    base_model['to_dict'] = to_dict
    
    return base_model
