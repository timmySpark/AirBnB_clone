#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_quit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_destroy
    TestHBNBCommand_help
    TestHBNBCommand_all
    TestHBNBCommand_update
"""
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """Test cases for HBNBCommand class methods."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_quit_command(self, mock_stdout):
        """Test quit command"""
        cmd = HBNBCommand()
        cmd.onecmd("quit")
        self.assertEqual("", mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        """Test help command"""
        cmd = HBNBCommand()
        cmd.onecmd("help")
        self.assertIn("Documented commands", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_command(self, mock_stdout):
        """Test create command"""
        cmd = HBNBCommand()
        cmd.onecmd("create BaseModel")
        self.assertIn("BaseModel", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_command(self, mock_stdout):
        """Test show command"""
        instance = BaseModel()
        instance.save()
        instance_id = instance.id
        class_name = instance.__class__.__name__

        with patch('models.storage.all') as mock_all:
            mock_all.return_value = {f"{class_name}.{instance_id}": instance}
            cmd = HBNBCommand()
            cmd.onecmd(f'show {class_name} {instance_id}')
            self.assertIn(str(instance), mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_command(self, mock_stdout):
        """Test all command"""
        with patch('models.storage.all') as mock_all:
            # Create a BaseModel instance before testing the 'all' command
            storage.new(BaseModel())
            mock_all.return_value = storage.all()
            cmd = HBNBCommand()
            cmd.onecmd('all BaseModel')
            self.assertIn('BaseModel', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy_command(self, mock_stdout):
        """Test destroy command"""
        instance = BaseModel()
        instance.save()
        instance_id = instance.id
        class_name = instance.__class__.__name__

        with patch('models.storage.all') as mock_all, \
             patch('models.storage.save') as mock_save:
            mock_all.return_value = {f"{class_name}.{instance_id}": instance}
            cmd = HBNBCommand()
            cmd.onecmd(f'destroy {class_name} {instance_id}')
            self.assertNotIn(instance, storage.all().values())
            self.assertTrue(mock_save.called)

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_command(self, mock_stdout):
        """Test update command"""
        instance = BaseModel()
        instance.save()
        instance_id = instance.id
        class_name = instance.__class__.__name__

        with patch('models.storage.all') as mock_all, \
             patch('models.storage.save') as mock_save:
            mock_all.return_value = {f"{class_name}.{instance_id}": instance}
            cmd = HBNBCommand()
            cmd.onecmd(f'update {class_name} {instance_id} name "John"')
            self.assertEqual(instance.name, "John")
            self.assertTrue(mock_save.called)


if __name__ == '__main__':
    unittest.main()
