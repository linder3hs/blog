# import unittest
import unittest

from flask import jsonify
from app import create_app, suma
from app.models.roles import Role
from app.models.usuarios import User
from app.db import db

# ❯ python3 -m unittest

class APITestCase(unittest.TestCase):
    def setUp(self):
        print("Setup test")

    # def test_post(self):
    #     app = create_app()
    #     app.app_context().push()
    #     db.create_all()
    #     user_role = Role(name="User")
    #     db.session.add(user_role)
    #     db.session.commit()

    def test_suma(self):
        self.assertEqual(suma(2, 2), 5)



    # def test_post(self):
    #     with self.app.app_context():
    #         r = Role.query.filter_by(name="User").first()
    #         self.assertIsNotNone(r)
    #         u = User(username="marc", email="marc@example.com", role=r)
    #         u.set_password("password")
    #         self.assertIsNotNone(u)
    #         db.session.add(u)
    #         db.session.commit()
    #         response = self.client.post(
    #             "/postJson/",
    #             headers=self.get_api_headers("john@example.com", "password"),
    #             data=jsonify.dumps({"body": "body of the *blog* post"}),
    #         )

    #         self.assertEqual(response.status_code, 201)


if __name__ == " __main__":
    unittest.main()
