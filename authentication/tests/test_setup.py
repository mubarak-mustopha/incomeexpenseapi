from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        fake = Faker()
        self.user_data = {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.email(),
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
