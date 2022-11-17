# coding: utf-8

from flask import url_for
from OnlineCV.exceptions import USER_ALREADY_REGISTERED


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("user.register_user"), {
        "user": {
            "username": "batman",
            "email": "bwayne@gotham.com",
            "password": 'imbatman'
        }
    }, **kwargs)


class TestAuthentication:
    def test_register_user(self, testapp):
        response = _register_user(testapp)
        assert response.json['user']['email'] == 'bwayne@gotham.com'
        assert response.json['user']['token'] is not None

    def test_user_login(self, testapp):
        _register_user(testapp)
        response = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': 'bwayne@gotham.com',
            'password': 'imbatman'
        }})

        assert response.json['user']['email'] == 'bwayne@gotham.com'
        assert response.json['user']['token'] is not None

    def test_get_user(self, testapp):
        response = _register_user(testapp)
        token = str(response.json['user']['token'])
        print('----------->>>>{}<<<<---------------'.format(response.json))
        response=testapp.get(url_for('user.get_user'), headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert response.json['user']['email'] == 'bwayne@gotham.com'
        assert response.json['user']['token'] == token

    def test_register_already_registered_user(self, testapp):
        _register_user(testapp)
        response = _register_user(testapp, expect_errors=True)
        assert response.status_int == 422
        assert response.json == USER_ALREADY_REGISTERED['message']
