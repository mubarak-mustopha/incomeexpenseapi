from rest_framework import status
from ..models import User
from .test_setup import TestSetUp


class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        # import pdb

        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, data=self.user_data, format="json")
        self.assertEqual(res.data["email"], self.user_data["email"])
        self.assertEqual(res.data["username"], self.user_data["username"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data)
        res = self.client.post(self.login_url, self.user_data)
        # import pdb

        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verified_user_can_login(self):
        self.client.post(self.register_url, self.user_data)
        # verify user
        user_email = self.user_data["email"]
        user = User.objects.get(email=user_email)
        user.is_verified = True
        user.save()

        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
