import unittest

from tracker.manager import Manager
from tracker.logger import Logger
from tracker.base import Task


class TestUserMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Logger()
        cls.manager = Manager()

    def test_save_task(self):
        key_first = self.manager.get_free_key_task()
        key_second = self.manager.get_free_key_task()
        task = Task(None, 'task', 'andrew', key_first,  3, 'waiting', '2018-08-09 10:20', '', '')
        task.key = key_first
        second_task = Task(None, 'task2', 'andrew', key_second,  3, 'waiting', '2018-08-09 10:20', '', '')
        second_task.key = key_second
        self.manager.save_task(task)
        self.manager.save_task(second_task)

        new_task = self.manager.get_task(key_first)
        self.assertEqual(new_task.host, 'andrew')
        self.assertEqual(new_task.key, key_first)
        self.manager.save_task(new_task)

    def test_add_task(self):
        key_task = self.manager.add_task(Task(None, 'task', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))

        task = self.manager.get_task(key_task)

        self.assertEqual(task.key, key_task)
        self.assertEqual(task.host, 'andrew')

    def test_type_exception(self):
        self.assertRaisesRegex(TypeError, 'Object type is not Task', self.manager.add_task, 'task')

    def test_add_subtask(self):
        key_parent = self.manager.add_task(Task(None, 'task', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_task = self.manager.add_task(Task(key_parent, 'sub', None, 3, 'waiting', '2018-08-09 10:20', '', ''))

        task = self.manager.get_task(key_task)
        par = self.manager.get_task(key_parent)

        self.assertIsNotNone(task)
        self.assertIsNotNone(par)
        self.assertEqual(task.parent, par.key)
        self.assertIn(task.key, par.subtasks)
        self.assertEqual(task.host, par.host)

    def test_not_found_parent(self):
        self.assertRaisesRegex(Exception, 'Task N1000 not found in file', self.manager.add_task, Task('1000', 'sub', None, 3, 'waiting', '2018-08-09 10:20', '', ''))

    def test_created_link(self):
        key_first = self.manager.add_task(Task(None, 'task1', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_second = self.manager.add_task(Task(None, 'task2', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_link(key_first, key_second)

        first = self.manager.get_task(key_first)
        second = self.manager.get_task(key_second)

        self.assertIn(key_second, first.links)
        self.assertIn(key_first, second.links)

    def test_create_double_link(self):
        key_first = self.manager.add_task(Task(None, 'task1', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_second = self.manager.add_task(Task(None, 'task2', 'andrew', 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_link(key_first, key_second)
        self.assertRaisesRegex(Exception, 'Link between tasks N{1} and N{0} already exist'.format(key_first, key_second), self.manager.add_link, key_second, key_first)

    def test_exist_task(self):
        key_second = self.manager.add_task(Task(None, 'task2', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.assertRaisesRegex(Exception, 'Task N1000 not found in file', self.manager.add_link, key_second, '1000')

    def test_removed_link(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_second = self.manager.add_task(
            Task(None, 'task2', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_link(key_first, key_second)
        self.manager.delete_link(key_first, key_second)

        first = self.manager.get_task(key_first)
        second = self.manager.get_task(key_second)

        self.assertNotIn(key_second, first.links)
        self.assertNotIn(key_first, second.links)

    def test_add_admin(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_admin_in_task(key_first, 'kot')
        task = self.manager.get_task(key_first)

        self.assertIn('kot', task.admins)

    def test_add_member(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_member_in_task(key_first, 'kot')
        task = self.manager.get_task(key_first)

        self.assertIn('kot', task.members)

    def test_delete_member(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_member_in_task(key_first, 'kot')
        self.manager.delete_member_in_task(key_first, 'kot')
        task = self.manager.get_task(key_first)

        self.assertNotIn('kot', task.members)

    def test_delete_member_double(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_member_in_task(key_first, 'kot')
        self.manager.delete_member_in_task(key_first, 'kot')

        self.assertRaisesRegex(Exception, "Member {0} not found in task N{1}".format('kot', key_first),
                               self.manager.delete_member_in_task, key_first, 'kot')

    def test_delete_admin(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_admin_in_task(key_first, 'kot')
        self.manager.delete_admin_in_task(key_first, 'kot')
        task = self.manager.get_task(key_first)

        self.assertNotIn('kot', task.admins)

    def test_delete_admin_double(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.add_admin_in_task(key_first, 'kot')
        self.manager.delete_admin_in_task(key_first, 'kot')

        self.assertRaisesRegex(Exception, "Admin {0} not found in task N{1}".format('kot', key_first), self.manager.delete_admin_in_task, key_first, 'kot')

    def test_delete_1_task(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.delete_task(key_first)

        self.assertIsNone(self.manager.get_task(key_first))

    def test_delete_2_task(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_second = self.manager.add_task(
            Task(key_first, 'task2', None, self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.delete_task(key_second)

        task = self.manager.get_task(key_first)

        self.assertNotIn(key_second, task.subtasks)
        self.assertIsNone(self.manager.get_task(key_second))

    def test_delete_3_task(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_second = self.manager.add_task(
            Task(key_first, 'task2', None, self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))
        key_third = self.manager.add_task(
            Task(key_first, 'task3', None, self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))

        self.manager.delete_task(key_first)

        self.assertIsNone(self.manager.get_task(key_second))
        self.assertIsNone(self.manager.get_task(key_first))
        self.assertIsNone(self.manager.get_task(key_third))

    def test_change_status_task(self):
        key_first = self.manager.add_task(
            Task(None, 'task1', 'andrew', self.manager.get_free_key_task(), 3, 'waiting', '2018-08-09 10:20', '', ''))
        self.manager.change_status_task(key_first, 'ended')

        task = self.manager.get_task(key_first)
        self.assertEqual('ended', task.status)

    def test_login_user(self):
        Logger.enter('andrew')


if __name__ == '__main__':
    unittest.main()
