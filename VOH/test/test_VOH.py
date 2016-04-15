import unittest
from VOH import main
from werkzeug.security import generate_password_hash
class TestVOH(unittest.TestCase):

    def setUp(self):
        self.client, self.db = main.open_db_connection()
        self.test_table = self.db["test_table"]
        self.test_table.remove()
        self.insert_dummy_data()

    def insert_dummy_data(self):

        dummy_data = {
            "password":generate_password_hash('11111'),
            "net_id":"abcd",
            "type":"TA",
            "name":"Chris"
        }
        self.test_table.insert(dummy_data)

    def test_login(self):
        """
        Tests for Login
        :return:
        """
        # False Login
        self.assertFalse(main.authentication.authenticate_user("abcd",'11112',"test"))
        # True Login
        self.assertTrue(main.authentication.authenticate_user("abcd",'11111',"test"))

    def test_registration(self):
        """
        Test for registration parameters
        :return:
        """

        self.assertFalse(main.TA.check_in_ta_list("abcd"))

        self.assertTrue(main.TA.check_ta_registration("nmshah4"))





if __name__ == "__main__":
    unittest.main()