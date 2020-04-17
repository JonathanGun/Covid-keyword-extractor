import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_post(self):
        # send data as POST form to endpoint
        sent = {
            "keywords": ["ODP", "PDP", "terkonfirmasi positif", "orang", "kasus positif"],
            "texts": [],
            "filenames": [],
            "algorithm": "boyer-moore"  # or "kmp" or "regex" (default: "regex")
        }
        sent["texts"].append(self.app.get('/sample/kompas1.txt').data.decode("utf-8"))
        sent["texts"].append(self.app.get('/sample/detik1.txt').data.decode("utf-8"))
        rv = self.app.post(
            '/extractor',
            data=sent
        )
        # check result from server with expected data
        self.assertEqual(rv.status_code, 200)

    def test_extractor_page_works(self):
        rv = self.app.get('/extractor')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    # def test_default_redirecting(self):
    #     rv = self.app.get('/extractor')
    #     self.assertEqual(rv.status_code, 301)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/sample/kompas1.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()
