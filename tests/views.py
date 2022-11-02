""" testing the pages

    This requires the server to be running on http://0.0.0.0:8260

"""
import unittest
import requests


class TestViews(unittest.TestCase):

    BASE_URL = 'http://0.0.0.0:8260/'
    ordinary_user = {'usr': 'user@space.net', 'pwd': '1234'}
    admin_user = {'usr': 'adm@nowhere.here', 'pwd': '1234'}

    def test_home(self):
        """ test whether home is served """
        url = TestViews.BASE_URL
        response = requests.get(url)
        assert response.status_code == 200
        assert 'Home' in response.text

    def test_login(self):
        """ test to go to login page """
        url = TestViews.BASE_URL + 'login'
        response = requests.get(url)
        assert response.status_code == 200
        assert 'Login form' in response.text

    def test_no_access_authenticated(self):
        """ test no access to authenticated page without authentication """
        url = TestViews.BASE_URL + 'authenticated'
        response = requests.get(url)
        assert response.status_code == 200
        assert 'Hurrah' not in response.text

    def test_do_login_no_success(self):
        """ test the unsuccessful login """
        url = TestViews.BASE_URL + 'login'
        wrong = {
            'usr': 'abd@def.ghi',
            'pwd': 'not a password'
        }
        response = requests.post(url, data=wrong)
        assert response.status_code == 200
        assert 'Login form' in response.text
        assert not response.cookies.get('session')

    def test_do_login_with_success(self):
        """ do a successful login """
        url = TestViews.BASE_URL + 'login?next=authenticated'  # should go to authenticated page
        response = requests.post(url, data=TestViews.ordinary_user)
        assert response.status_code == 200
        assert 'Hurrah' in response.text
        assert response.cookies.get('session')

    def test_do_logout(self):
        """ test logout """
        url = TestViews.BASE_URL + 'login?next=authenticated'  # should go to authenticated page
        response = requests.post(url, data=TestViews.ordinary_user)
        assert 'Hurrah' in response.text  # check we logged in
        url2 = TestViews.BASE_URL + 'logout'
        response2 = requests.get(url2)
        assert response2.status_code == 200
        assert 'Home' in response2.text
        assert not response2.cookies.get('session')

    def test_page_without_scope(self):
        """ test no access to page without proper scope """
        url = TestViews.BASE_URL + 'login?next=auth/test'
        response = requests.post(url, data=TestViews.ordinary_user)
        assert response.status_code == 200
        assert 'Home' in response.text
        assert 'Testing data access' not in response.text
        assert response.cookies.get('session')

    def test_page_with_scope(self):
        """ test access to page with scope admin """
        url = TestViews.BASE_URL + 'login?next=auth/test'
        response = requests.post(url, data=TestViews.admin_user)
        assert response.status_code == 200
        assert 'Testing data access' in response.text
        assert response.cookies.get('session')


if __name__ == '__main__':
    unittest.main()
