
import unittest

from sql_table import *


class SQLTableTestCase(unittest.TestCase):

    def test_no_empty_table(self):
        
        class EmptyTable(SQLTable):
            pass

        self.assertRaises(SQLDeclarationError, EmptyTable)


    def test_no_primary_keys_a(self):

        class TestTable(SQLTable):
            table_name = 'test_table'
            a = Integer()

        self.assertIs(TestTable.a.abstract_table, TestTable)

        self.assertTrue(not TestTable.a.primary_key)

        table = TestTable()

        self.assertTrue(not TestTable.a.primary_key)
        self.assertTrue(not table.a.is_primary_key())
        self.assertEqual(table.primary_key.columns, tuple())

    def test_no_primary_keys_b(self):

        class TestTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()

        self.assertIs(TestTable.a.abstract_table, TestTable)
        self.assertIs(TestTable.b.abstract_table, TestTable)


        self.assertTrue(not TestTable.a.primary_key)
        self.assertTrue(not TestTable.b.primary_key)

        table = TestTable()

        self.assertTrue(not TestTable.a.primary_key)
        self.assertTrue(not TestTable.b.primary_key)
        self.assertTrue(not table.a.is_primary_key())
        self.assertTrue(not table.b.is_primary_key())
        self.assertEqual(table.primary_key.columns, tuple())


    def test_first_primary_keys(self):

        class TestTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()
            primary_key(a)

        self.assertIs(TestTable.a.abstract_table, TestTable)
        self.assertIs(TestTable.b.abstract_table, TestTable)

        self.assertTrue(TestTable.a.primary_key)
        self.assertTrue(not TestTable.b.primary_key)

        table = TestTable()

        self.assertTrue(TestTable.a.primary_key)
        self.assertTrue(not TestTable.b.primary_key)
        self.assertTrue(table.a.is_primary_key())
        self.assertTrue(not table.b.is_primary_key())
        self.assertEqual(table.primary_key.columns, (table.a,))


class ForeignTableTestCase(unittest.TestCase):

    def test_foreign_table_declaration(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')

    def test_requires_foreign_table(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')
        
        self.assertRaises(ForeignTableError, TestTable)


    def test_requires_foreign_column(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')
        
        class TestKeys(SQLTable):
            table_name = 'test_keys'
            notkey = Integer()

        test_keys = TestKeys()

        self.assertRaises(ForeignTableError, TestTable, Keys=test_keys)


    def test_requires_foreign_column_type(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')

        class TestKeys(SQLTable):
            table_name = 'test_keys'
            notkey = Real()

        test_keys = TestKeys()

        self.assertRaises(ForeignTableError, TestTable, Keys=test_keys)


    def test_ok_with_column(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')
        
        class TestKeys(SQLTable):
            table_name = 'test_keys'
            key = Integer()

        test_keys = TestKeys()


    def test_ok_with_rename(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')
        
        class TestKeys(SQLTable):
            table_name = 'test_keys'
            key = Integer()

        test_keys = TestKeys(notkey_name='key')


    def test_ok_with_additional_columns(self):
        
        class TestTable(SQLTable):
            table_name = 'test_table'
            Keys = ForeignTable()
            key = Keys.Integer('key')
        
        class TestKeys(SQLTable):
            table_name = 'test_keys'
            key = Integer()
            otherkey = Integer()

        test_keys = TestKeys(notkey_name='key')

        test_table = TestTable(Keys=test_keys)
       

class TestTableEqualTestCase(unittest.TestCase):

    def assertEqual(self, a, b):
        unittest.TestCase.assertEqual(self, a, b)
        unittest.TestCase.assertEqual(self, b, a)

    def assertNotEqual(self, a, b):
        unittest.TestCase.assertNotEqual(self, a, b)
        unittest.TestCase.assertNotEqual(self, b, a)

    def test_single_int_equal_single_int(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_single_text_equal_single_text(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Text()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Text()


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_single_real_equal_single_real(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Real()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Real()


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_single_int_not_equal_single_real(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Real()


        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_single_int_not_equal_single_int_different_name_a(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            b = Integer()


        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_single_int_not_equal_single_int_different_name_b(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()


        first = FirstTable()
        second = SecondTable(a_name='b')

        self.assertNotEqual(first, second)        


    def test_single_primary_int_equal_single_primary_int(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            primary_key(a)


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_single_primary_int_not_equal_single_int(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()


        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_int_real_equal_int_real(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_real_int_not_equal_int_real(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Real()
            b = Integer()


        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()


        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)


    def test_int_real_not_equal_int_real_different_name(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Real()


        first = FirstTable()
        second = SecondTable(a_name='b', b_name='a')

        self.assertNotEqual(first, second)        


    def test_int_int_equal_int_int(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()


        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_int_int_not_equal_int_int_different_order(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            b = Integer()
            a = Integer()



        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_int_int_equal_int_int_different_order_renamed(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()

        class SecondTable(SQLTable):
            table_name = 'test_table'
            b = Integer()
            a = Integer()



        first = FirstTable()
        second = SecondTable(b_name='a', a_name='b')

        self.assertEqual(first, second)        


    def test_int_int_equal_int_int_same_primary_key(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)



        first = FirstTable()
        second = SecondTable()

        self.assertEqual(first, second)        


    def test_int_int_not_equal_int_int_different_primary_key(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(b)

        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_int_int_not_equal_int_int_same_primary_key_renamed(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            b = Integer()
            a = Integer()
            primary_key(b)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)

        first = FirstTable()
        second = SecondTable()

        self.assertNotEqual(first, second)        


    def test_int_int_equal_int_int_same_primary_key_re_renamed(self):
        class FirstTable(SQLTable):
            table_name = 'test_table'
            b = Integer()
            a = Integer()
            primary_key(b)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)

        first = FirstTable()
        second = SecondTable(a_name='b', b_name='a')

        self.assertEqual(first, second)


    def test_int_int_equal_int_int_same_foreignkey(self):
        class ReferenceTable(SQLTable):
            key = Integer()
            primary_key(key)

        ref_table = ReferenceTable()

        class FirstTable(SQLTable):
            table_name = 'test_table'
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Integer()
            primary_key(a)


        first = FirstTable(ref_table=ref_table)
        second = SecondTable(ref_table=ref_table)

        self.assertEqual(first, second)        


    def test_int_int_not_equal_int_int_lacking_foreignkey(self):
        class ReferenceTable(SQLTable):
            key = Integer()
            primary_key(key)

        ref_table = ReferenceTable()

        class FirstTable(SQLTable):
            table_name = 'test_table'
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Integer()
            primary_key(a)

        class SecondTable(SQLTable):
            table_name = 'test_table'
            a = Integer()
            b = Integer()
            primary_key(a)


        first = FirstTable(ref_table=ref_table)
        second = SecondTable()

        self.assertNotEqual(first, second)        




class ParseTableTestCase(unittest.TestCase):

    def assertOuroboros(self, table, ref_tables=[]):
        parsed_table = parse_table(table.sql_table(), ref_tables=ref_tables)

        self.assertEqual(table, parsed_table)

    # def test_oroubus_empty(self):
        
    #     class ExampleTable(SQLTable):
    #         pass


    #     self.assertOuroboros(ExampleTable())


    def test_oroubus_int(self):
        
        class ExampleTable(SQLTable):
            a = Integer()

        self.assertOuroboros(ExampleTable())


    def test_oroubus_int_real(self):
        # TODO: somehow this is being contaminated with primary keys
        class ExampleTable(SQLTable):
            a = Integer()
            b = Real()

        self.assertOuroboros(ExampleTable())


    def test_oroubus_int_real_primarykey(self):
        
        class ExampleTable(SQLTable):
            a = Integer()
            b = Real()
            primary_key(a)


        self.assertOuroboros(ExampleTable())


    def test_oroubus_double_int_primarykey(self):
        
        class ExampleTable(SQLTable):
            a = Integer()
            b = Integer()
            primary_key(a, b)


        self.assertOuroboros(ExampleTable())



    def test_oroubus_int_real_primarykey_foreignkey(self):
        
        
        class ReferenceTable(SQLTable):
            key = Integer()
            primary_key(key)

        class ExampleTable(SQLTable):
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Real()
            primary_key(a)

        ref_table = ReferenceTable()

        self.assertOuroboros(ExampleTable(ref_table=ref_table), ref_tables=[ref_table])


    def test_oroubus_int_real_primarykey_foreignkey_parsed(self):
        
        
        class ReferenceTable(SQLTable):
            key = Integer()
            primary_key(key)

        class ExampleTable(SQLTable):
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Real()
            primary_key(a)

        ref_table = parse_table(ReferenceTable().sql_table())

        self.assertOuroboros(ExampleTable(ref_table=ref_table), ref_tables=[ref_table])


    def test_oroubus_int_real_primarykey_foreignkey_needs_reftable(self):
        
        
        class ReferenceTable(SQLTable):
            key = Integer()
            primary_key(key)

        class ExampleTable(SQLTable):
            ref_table = ForeignTable()
            a = ref_table.Integer('key')
            b = Real()
            primary_key(a)

        ref_table = ReferenceTable()

        table = ExampleTable(ref_table=ref_table)
        self.assertRaises(SQLSyntaxError, parse_table, table.sql_table())


if __name__ == "__main__":
    unittest.main()
        
