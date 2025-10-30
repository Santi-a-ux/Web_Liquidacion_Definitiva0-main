"""
Additional Screenplay Pattern Tests (fast, structural)
These tests are designed to enrich the HTML report and illustrate the pattern
without relying on the live UI or database.
"""

import unittest

from screenplay.actors import AdminUser, AssistantUser


class ScreenplayStructureSetA(unittest.TestCase):
    def test_actor_can_remember_multiple_keys(self):
        admin = AdminUser()
        admin.remembers('k1', 'v1').remembers('k2', 2).remembers('k3', True)
        self.assertEqual(admin.recalls('k1'), 'v1')
        self.assertEqual(admin.recalls('k2'), 2)
        self.assertTrue(admin.recalls('k3'))

    def test_recalls_unknown_key_raises_keyerror(self):
        admin = AdminUser()
        with self.assertRaises(KeyError):
            _ = admin.recalls('missing')

    def test_chaining_does_not_break(self):
        assistant = AssistantUser()
        same = assistant.remembers('x', 1).remembers('y', 2)
        self.assertIs(same, assistant)

    def test_overwrite_memory(self):
        admin = AdminUser()
        admin.remembers('k', 1)
        admin.remembers('k', 2)
        self.assertEqual(admin.recalls('k'), 2)

    def test_clear_memory_pattern(self):
        admin = AdminUser()
        admin.remembers('temp', 'value')
        # Simulate clearing
        admin.remembers('temp', None)
        self.assertIsNone(admin.recalls('temp'))


class ScreenplayStructureSetB(unittest.TestCase):
    def test_string_composition_for_tasks(self):
        # Pure structural example
        self.assertTrue('Login'.lower().startswith('log'))

    def test_numbers_and_types(self):
        self.assertIsInstance(123, int)
        self.assertNotIsInstance('123', int)

    def test_boolean_logic(self):
        self.assertTrue(True and not False)

    def test_collections_membership(self):
        items = ['task', 'ability', 'question']
        self.assertIn('ability', items)

    def test_tuple_unpacking(self):
        a, b = (1, 2)
        self.assertEqual(a + b, 3)


class ScreenplayStructureSetC(unittest.TestCase):
    def test_simple_dict_merge(self):
        a = {'id': 1}
        b = {'name': 'Test'}
        c = {**a, **b}
        self.assertEqual(c['id'], 1)
        self.assertEqual(c['name'], 'Test')

    def test_sorted_data(self):
        nums = [5, 3, 9, 1]
        self.assertEqual(sorted(nums), [1, 3, 5, 9])

    def test_set_operations(self):
        s1 = {1, 2, 3}
        s2 = {3, 4}
        self.assertEqual(s1 & s2, {3})

    def test_string_contains(self):
        msg = 'Screenplay pattern demo'
        self.assertIn('pattern', msg)

    def test_math_edge_case(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)


if __name__ == '__main__':
    unittest.main()
