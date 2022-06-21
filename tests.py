import unittest

from app import app, db


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.db = db
        self.client = self.app.test_client()

    def tearDown(self):
        """Executed after reach test"""

    def test_index_returns_200(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_index_returns_hello_world(self):
        res = self.client.get("/")
        self.assertEqual(res.json.get("message"), "Hello World!")

    def test_get_all_contacts_returns_200(self):
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)

    def test_create_person_returns_201(self):
        person = {"first_name": "test person"}
        res = self.client.post("/people", json=person)
        self.assertEqual(res.status_code, 201)

    def test_create_person_returns_person_created(self):
        person = {"first_name": "test person"}
        res = self.client.post("/people", json=person)
        self.assertEqual(res.json.get("message"), "person created")

    def test_creating_person_with_no_data_returns_400(self):
        res = self.client.post("/people")
        self.assertEqual(res.status_code, 400)

    # def test_deleting_contact_returns_contact_deleted(self):
    #     res = self.client.delete("/contacts/2")
    #     self.assertTrue(res.status_code == 200)
    #     self.assertTrue(res.json.get("message") == "contact deleted")

    # def test_updating_contact_returns_contact_updated(self):
    #     res = self.client.patch("/contacts/3", json={"contact": "new contact"})
    #     self.assertTrue(res.status_code == 200)
    #     self.assertTrue(res.json.get("message") == "contact updated")

    def test_searching_for_people_should_return_matching_people(self):
        res = self.client.get("/people/search?first_name=test")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("test" in res.json[0].get("first_name"))

    def test_searching_for_people_should_return_404_if_missing(self):
        res = self.client.get("/people/search?first_name=el")
        self.assertEqual(res.status_code, 404)

    def test_searching_contacts_should_return_matching_contacts(self):
        res = self.client.post("/contacts/search", json={"contact": "00"})
        self.assertTrue("00" in res.json[0].get("contact"))


if __name__ == "__main__":
    unittest.main()
