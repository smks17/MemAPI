import json
import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.sql import crud, schemas, get_db

client = TestClient(app)


class TestAPI:
    def test_successfully_get(self):
        """It tests the home page could be loaded or not"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Hello, This is a test of API task. For usage see '/docs'"
        }

    @classmethod
    def _create_fake_user(cls):
        """A function to create a fake user to work with it"""
        rand_name = f"fake{random.randint(0, 10000)}"
        fake_user = schemas.UserCreate(username=rand_name,
                                       email=f"{rand_name}@example.com",
                                       password="1234")
        return fake_user

    def test_create_account(self):
        """It tests register a user by api"""
        fake_user = self._create_fake_user()
        form_data = {
            "username": fake_user.username,
            "email": fake_user.email,
            "password": fake_user.password
        }
        response = client.post(
            "/users/register",
            params=form_data,
            headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Your account has been created successfully!"

    @pytest.fixture()
    def create_fake_accounts(self):
        """A test fixture to create a fake account and add it to the database"""
        self.__class__.test_user = self._create_fake_user()
        crud.create_user(get_db(), self.test_user)
        # TODO: delete fake users from database after test

    def test_try_create_duplicate_username(self, create_fake_accounts):
        """It tests bad response for requesting duplicate username to register"""
        fake_user = self.test_user
        form_data = {
            "username": fake_user.username,
            "email": "mahdi@example.com",
            "password": fake_user.password
        }
        response = client.post(
            "/users/register",
            params=form_data,
            headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        assert response.status_code == 406
        assert response.json()["detail"] == "This username is already exist!"

    def test_try_create_duplicate_user(self, create_fake_accounts):
        """It tests bad response for requesting duplicate user to register"""
        fake_user = self.test_user
        form_data = {
            "username": fake_user.username,
            "email": fake_user.email,
            "password": fake_user.password
        }
        response = client.post(
            "/users/register",
            params=form_data,
            headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        assert response.status_code == 406
        assert response.json()["detail"] == "This account is already exist!"

    @pytest.fixture()
    def create_fake_token(self, create_fake_accounts):
        """A test fixture to get a token from API for a fake account. Also, it returns
        a function to use the fixture.
        """
        def create():
            fake_user = self.test_user
            form_data = {
                "username": fake_user.username,
                "password": fake_user.password
            }
            response = client.post(
                "/users/token",
                data=form_data,
                headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
            )
            return response
        return create

    def test_create_token(self, create_fake_token):
        """It tests the request to get a token"""
        response = create_fake_token()
        assert response.status_code == 201
        assert response.json()["token_type"] == "bearer"
        assert response.json()["access_token"] != ""

    def test_bad_request_token(self):
        """It tests the bad request to get a token for a non-exist user in the database"""
        form_data = {
            "username": "null",
            "password": "null"
        }
        response = client.post(
            "/users/token",
            data=form_data,
            headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        assert response.status_code == 401

    def test_use_token(self, create_fake_token):
        """It tests a valid token to get its own user by API"""
        response = create_fake_token()
        assert response.status_code == 201
        token = response.json()["access_token"]
        response = client.get("/users/me", headers={"Authorization": f'Bearer {token}'})
        assert response.status_code == 200
        # This user creates in create_fake_user from create_fake_token
        fake_user = self.test_user
        assert response.json() == {"username": fake_user.username, "activated": True}

    def test_bad_use_token(self):
        """It tests a non-valid token to get its own user by API that should return an error."""
        response = client.get("/users/me", headers={"Authorization": f'Bearer 0'})
        assert response.status_code == 401

    def test_getting_memory(self, create_fake_token):
        """It tests getting memory information from database."""
        response = create_fake_token()
        assert response.status_code == 201
        token = response.json()["access_token"]
        response = client.get("/memory/info?limit=1",
                              headers={"Authorization": f'Bearer {token}'})
        assert response.status_code == 200
        list_mem = crud.get_mem(get_db(), 1)
        assert response.json() == json.loads(list_mem.json())