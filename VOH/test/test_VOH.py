import unittest
from VOH import main
from werkzeug.security import generate_password_hash
import time
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


    def test_time(self):
        """
        Tests Timing functions for TA
        :return:
        """
        main.TA.set_ta_status("agupta60", "online")
        ta_time_old = main.TA.get_ta_timings()
        old_time = ""
        new_time = ""
        for ta in ta_time_old:
            if ta["name"] == "agupta60":
                old_time = ta["time in minutes"]

        time.sleep(60)

        main.TA.set_ta_status("agupta60", "offline")
        ta_time_new = main.TA.get_ta_timings()
        for ta in ta_time_new:
            if ta["name"] == "agupta60":
                new_time = ta["time in minutes"]

        self.assertTrue(new_time -old_time >= 1)
        # self.assertEquals(new_time - old_time , 1)

    def test_rating(self):
        """
        Tests addition of Rating for TA
        :return:
        """
        ta_rating_old = main.TA.get_ta_ratings()
        old_rating = ""
        new_rating = ""
        for ta in ta_rating_old:
            if ta["name"] == "agupta60":
                old_rating = ta["score"]

        data = {
            "rating_for":"agupta60",
            "rating_by":"agou2",
            "rating":5
        }
        main.TA.add_ta_rating(data)
        ta_rating_new = main.TA.get_ta_ratings()
        for ta in ta_rating_new:
            if ta["name"] == "agupta60":
                new_rating = ta["score"]
        self.assertTrue(new_rating - old_rating == 5)


if __name__ == "__main__":
    unittest.main()