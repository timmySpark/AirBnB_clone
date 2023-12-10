#!/usr/bin/python3
''' Defines a File Storage Class '''
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    '''Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    '''

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        ''' Return the dictionary object '''
        return FileStorage.__objects

    def new(self, obj):
        ''' sets in __objects the obj with key <obj class name>.id '''
        cls_name = obj.__class__.__name__
        FileStorage.__objects['{}.{}'.format(cls_name, obj.id)] = obj

    def save(self):
        ''' serializes __objects to the JSON file (path: __file_path)'''
        objects = FileStorage.__objects
        object_dict = {}
        for obj_key in objects.keys():
            obj = objects[obj_key]
            object_dict[obj_key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf8') as writeFile:
            json.dump(object_dict, writeFile)

    def reload(self):
        ''' deserializes the JSON file to __objects'''
        file_path = FileStorage.__file_path

        try:
            with open(file_path, 'r') as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
