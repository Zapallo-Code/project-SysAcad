from django.test import TestCase
from django.db import connection


class ConnectionTestCase(TestCase):

    # test connection to db
    def test_db_connection(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Hello world'")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'Hello world')
