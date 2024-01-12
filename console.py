#!/usr/bin/python3
"""
Interactive shell for AirBnB project.
"""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parser(arg):
    """Input parser"""
    _brace = re.search(r"\{(.*?)\}", arg)
    _brackets = re.search(r"\[(.*?)\]", arg)
    if _brace is None:
        if _brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:_brackets.span()[0]])
            result = [i.strip(",") for i in lexer]
            result.append(_brackets.group())
            return result
    else:
        lexer = split(arg[:_brace.span()[0]])
        result = [i.strip(",") for i in lexer]
        result.append(_brace.group())
        return result


class HBNBCommand(cmd.Cmd):
    """
    Command interpteter
    """

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def empty_line(self):
        """
        If empty line, do nothing
        """
        pass

    def default(self, arg):
        """
        The default behaviour of the interpreter
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        _match = re.search(r"\.", arg)
        if _match is not None:
            _arg = [arg[:_match.span()[0]], arg[_match.span()[1]:]]
            _match = re.search(r"\((.*?)\)", _arg[1])
            if _match is not None:
                _command = [_arg[1][:_match.span()[0]], _match.group()[1:-1]]
                if _command[0] in argdict.keys():
                    call = "{} {}".format(_arg[0], _command[1])
                    return argdict[_command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return (False)

    def do_quit(self, arg):
        """Quit the shell"""
        return True

    def do_EOF(self, arg):
        """Exit on EOF (Ctrl-D)"""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the id"""
        _arg = parser(arg)
        if len(_arg) == 0:
            print("** class name missing **")
        elif _arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(_arg[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        _arg = parser(arg)
        dict_obj = storage.all()
        if len(_arg) == 0:
            print("** class name missing **")
        elif _arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(_arg[0], _arg[1]) not in dict_obj:
            print("** no instance found **")
        else:
            print(dict_obj["{}.{}".format(_arg[0], _arg[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        _arg = parser(arg)
        dict_obj = storage.all()
        if len(_arg) == 0:
            print("** class name missing **")
        elif _arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(_arg[0], _arg[1]) not in dict_obj.keys():
            print("** no instance found **")
        else:
            del dict_obj["{}.{}".format(_arg[0], _arg[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        _arg = parser(arg)
        if len(_arg) > 0 and _arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            _obj = []
            for obj in storage.all().values():
                if len(_arg) > 0 and _arg[0] == obj.__class__.__name__:
                    _obj.append(obj.__str__())
                elif len(_arg) == 0:
                    _obj.append(obj.__str__())
            print(_obj)

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        _arg = parser(arg)
        _count = 0
        for obj in storage.all().values():
            if _arg[0] == obj.__class__.__name__:
                _count += 1
        print(_count)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        _arg = parser(arg)
        dict_obj = storage.all()

        if len(_arg) == 0:
            print("** class name missing **")
            return (False)
        if _arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return (False)
        if len(_arg) == 1:
            print("** instance id missing **")
            return (False)
        if "{}.{}".format(_arg[0], _arg[1]) not in dict_obj.keys():
            print("** no instance found **")
            return (False)
        if len(_arg) == 2:
            print("** attribute name missing **")
            return (False)
        if len(_arg) == 3:
            try:
                type(eval(_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return (False)

        if len(_arg) == 4:
            obj = dict_obj["{}.{}".format(_arg[0], _arg[1])]
            if _arg[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[_arg[2]])
                obj.__dict__[_arg[2]] = valtype(_arg[3])
            else:
                obj.__dict__[_arg[2]] = _arg[3]
        elif type(eval(_arg[2])) == dict:
            obj = dict_obj["{}.{}".format(_arg[0], _arg[1])]
            for k, v in eval(_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
