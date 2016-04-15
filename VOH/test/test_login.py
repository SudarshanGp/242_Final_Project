import unittest
from VOH import main
class TestVOH(unittest.TestCase):

    def setUp(self):
        self.client, self.db = main.open_db_connection()
        self.test_table = self.db["test_table"]
        self.insert_dummy_data()

    def insert_dummy_data(self):
        dummy_data = {
            "password":'11111',
            "netid":"abcd",
            "type":"TA",
            "name":"Chris"
        }
        self.test_table.insert(dummy_data)

    def test_login(self):
        self.assertFalse(main.authentication)




if __name__ == "__main__":
    unittest.main()