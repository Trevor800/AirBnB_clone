#!/usr/bin/python3
"""The HBNB Console Module """
import cmd
import sys
import re
import os
from datetime import datetime
import uuid
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """The HBNB console"""
    
    # The prompt
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit(0)

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit(0)

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        obj_kwargs = {}
        for arg in args[1:]:
            key, value = arg.split('=')
            obj_kwargs[key] = value

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in obj_kwargs.items():
                setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates an instance of a class")
        print("Usage: create <className> [<attribute1=value1> <attribute2=value2> ...]\n")

    def do_show(self, args):
        """ Method to show an individual object """
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        obj_key = class_name + "." + obj_id

        try:
            print(storage.all()[obj_key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows the details of an instance")
        print("Usage: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        obj_key = class_name + "." + obj_id

        try:
            del storage.all()[obj_key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an instance")
        print("Usage: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class """
        obj_list = []

        if args:
            class_name = args.split()[0]

            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            for key, obj in storage.all().items():
                if key.split('.')[0] == class_name:
                    obj_list.append(str(obj))
        else:
            for obj in storage.all().values():
                obj_list.append(str(obj))

        print(obj_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all instances, or instances of a specific class")
        print("Usage: all [className]\n")

    def do_count(self, args):
        """ Count current number of class instances """
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        count = sum(1 for key in storage.all() if key.split('.')[0] == class_name)
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Count the number of instances of a class")
        print("Usage: count <className>\n")

    def do_update(self, args):
        """ Updates a certain object with new info """
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        obj_key = class_name + "." + obj_id

        if obj_key not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]

        setattr(storage.all()[obj_key], attr_name, attr_value)
        storage.all()[obj_key].save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an instance with new information")
        print("Usage: update <className> <objectId> <attributeName> <attributeValue>\n")


if __name__ == '__main__':
    HBNBCommand().cmd
