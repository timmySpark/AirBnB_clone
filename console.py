#!/usr/bin/python3
''' Defining HBNBCommand console'''
import re
import cmd
from shlex import split
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    ''' Define Hbnb Command line Interpreter

        Attrs:
            prompt (str) : Command prompt
    '''

    prompt = "(hbnb) "
    class_obj = storage.all()
    class_dict = {}
    class_list = set(["BaseModel", "User", "Amenity",
                      "City", "Place", "Review", "State"])
    for obj in class_obj.values():
        class_dict[obj.id] = obj.__class__.__name__

    def do_quit(self, line):
        ''' Quit command to exit the program '''
        return True

    def do_EOF(self, line):
        ''' exit the Interpreter on EOF '''
        return True

    def emptyline(self):
        ''' Do not execute anything '''
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        '''
            Creates a new instance of BaseModel,
            saves it (to the JSON file) and prints the id
        '''
        if not arg:
            print('** class name missing **')
        elif arg not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{arg}()")
            new_instance.save()
            HBNBCommand.class_dict[new_instance.id] = arg
            print(new_instance.id)

    def do_count(self, arg):
        '''
            Retrieve the number of instances of a class:
                <class name>.count().
        '''
        argv = split(arg)
        cls_name = argv[0]
        class_obj = storage.all()
        count = 0
        for obj in class_obj.values():
            if cls_name == obj.__class__.__name__:
                count += 1
        print(count)

    def do_destroy(self, arg):
        '''
            Deletes an instance based on the class name and id
            (save the change into the JSON file)
        '''
        if not arg:
            print('** class name missing **')
            return
        argv = split(arg)
        class_object = storage.all()
        cls_name = argv[0]
        if cls_name not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return
        if len(argv) < 2:
            print('** instance id missing **')
            return
        cls_id = argv[1]
        if (cls_id in HBNBCommand.class_dict.keys() and
                HBNBCommand.class_dict[cls_id] == cls_name):
            key = f"{cls_name}.{cls_id}"
            del class_object[key]
            del HBNBCommand.class_dict[cls_id]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """
            Prints all string representation
            of all instances based or not on the class name.
            Ex: $ all BaseModel or $ all.
        """
        obj_list = []
        if not args:
            for obj in storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
        else:
            args_list = split(args)
            class_name = args_list[0]
            if class_name in HBNBCommand.class_list:
                for obj in storage.all().values():
                    if obj.__class__.__name__ == class_name:
                        obj_list.append(str(obj))
                print(obj_list)
            else:
                print("** class doesn't exist **")

    def do_show(self, arg):
        '''
            Prints the string representation of an instance based on the
            class name and id
        '''
        if not arg:
            print('** class name missing **')
            return
        argv = split(arg)
        cls_name = argv[0]
        if cls_name not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return
        if len(argv) < 2:
            print('** instance id missing **')
            return
        cls_id = argv[1]
        if (cls_id in HBNBCommand.class_dict.keys() and
                HBNBCommand.class_dict[cls_id] == cls_name):
            key = f"{cls_name}.{cls_id}"
            print(f"{HBNBCommand.class_obj[key]}")
        else:
            print("** no instance found **")

    def do_update(self, args):
        '''
            Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).
        '''

        args_list = split(args)
        arg_len = len(args_list)
        if arg_len < 1:
            print("** class name missing **")
            return
        class_name = args_list[0]
        if class_name not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return
        if arg_len < 2:
            print("** instance id missing **")
            return
        class_id = args_list[1]
        key = f"{class_name}.{class_id}"
        if key not in HBNBCommand.class_obj.keys():
            print("** no instance found **")
            return
        if arg_len < 3:
            print("** attribute name missing **")
            return
        attr_name = args_list[2]
        if arg_len < 4:
            print("** value missing **")
            return
        val_name = args_list[3]
        obj = HBNBCommand.class_obj[key]
        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            setattr(obj, attr_name, attr_type(val_name))
        else:
            setattr(obj, attr_name, val_name)

        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
