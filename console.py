#!/usr/bin/python3
"""The HBNB Console Module"""
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
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        command_parts = line.split()

        if len(command_parts) >= 2 and '.' in command_parts[0]:
            class_cmd_parts = command_parts[0].split('.')
            class_name = class_cmd_parts[0]
            command = class_cmd_parts[1]
            obj_id = command_parts[1]

            if len(command_parts) > 2:
                args = command_parts[2:]
                line = f"{command} {class_name} {obj_id} {' '.join(args)}"
            else:
                line = f"{command} {class_name} {obj_id}"

        return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit(0)

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit(0)

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        class_name, *params = args.split()

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()

        for param in params:
            key, value = param.split('=')
            if key in self.types:
                value = self.types[key](value)
            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates an instance of a class")
        print("Usage: create <className> [<param1>=<value1> ...]\n")

    def do_show(self, args):
        """Method to show an individual object"""
        if not args:
            print("** class name missing **")
            return

        class_name, obj_id = args.split()

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        obj_key = f"{class_name}.{obj_id}"
        if obj_key in storage.all():
            print(storage.all()[obj_key])
        else:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("Usage: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        if not args:
            print("** class name missing **")
            return

        class_name, obj_id = args.split()

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        obj_key = f"{class_name}.{obj_id}"
        if obj_key in storage.all():
            del storage.all()[obj_key]
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("Usage: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            class_name = args.split()[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            for obj_key, obj in storage.all().items():
                if obj_key.split('.')[0] == class_name:
                    print_list.append(str(obj))
        else:
            for obj_key, obj in storage.all().items():
                print_list.append(str(obj))

        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all objects of a class")
        print("Usage: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print("** class name missing **")
            return

        class_name = args.split()[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        count = sum(1 for obj_key in storage.all() if obj_key.split('.')[0] == class_name)
        print(count)

    def help_count(self):
        """Help information for the count command"""
        print("Counts the number of instances of a class")
        print("Usage: count <className>\n")

    def do_update(self, args):
        """Updates a certain object with new info"""
        if not args:
            print("** class name missing **")
            return

        parts = args.split()
        if len(parts) < 2:
            print("** instance id missing **")
            return

        class_name, obj_id, *attr_args = parts
        obj_key = f"{class_name}.{obj_id}"

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if obj_key not in storage.all():
            print("** no instance found **")
            return

        obj = storage.all()[obj_key]

        if not attr_args:
            print("** attribute name missing **")
            return

        if len(attr_args) < 2:
            print("** value missing **")
            return

        attr_name, attr_value = attr_args[:2]
        if attr_name in self.types:
            attr_value = self.types[attr_name](attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()

    def help_update(self):
        """Help information for the update command"""
        print("Updates an object with new information")
        print("Usage: update <className> <objectId> <attrName> <attrValue>\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
