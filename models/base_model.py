#!/usr/bin/python3
''' Defines a Base Model Class '''
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    '''  Representing a Base Model of the Hnbnb Project '''

    def __init__(self, *args, **kwargs):
        ''' Initializing a new base model

            Arguments:
                *args (any): Unused.
                **kwargs (dict): Key/value pairs of attributes.
        '''

        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if len(kwargs) != 0:
            for j, k in kwargs.items():
                if j == "created_at" or j == "updated_at":
                    self.__dict__[j] = datetime.strptime(k, time_format)
                else:
                    self.__dict__[j] = k
        else:
            models.storage.new(self)

    def save(self):
        '''
            Updates the public instance updated_at attribute with
            the current datetime
        '''
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        '''
            Returns a dictionary containing all keys/values of __dict__
            of the instance
        '''
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict

    def __str__(self):
        ''' Return the string representation of the Base Model Instance '''
        cls_name = self.__class__.__name__
        return ('[{}] ({}) <{}>'.format(cls_name, self.id, self.__dict__))
