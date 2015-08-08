# importiruem from file api_utils class Calls, class TestCase
from api_utils import Calls
from unittest import TestCase
# eto class, v kot hranyatsa status codes v chitaemom vide: 404:
import httplib

# inherit from class TestCase, kotoriy yavlyaetsa chastyu UnitTest
class TestClass(TestCase):
    #initialization
    # decorator proranit classmethod automatically kogda mi ranim , sam sebya executed, eto metod TestCase:
    @classmethod
    # default method setUpClass - resreved name 'setUpClass'
    # unit test will execute

    def setUpClass(cls):
        cls.calls = Calls()


    def test_create_folder_positive(self):
        folder = self.calls.get_random_name()
        resp = self.calls.create_folder(folder)
        assert resp.http_code == httplib.CREATED

    def test_create_folder_incorrect_credentials(self):
        folder = self.calls.get_random_name()
        resp = self.calls.create_folder(folder, password='hfhfh')
        assert resp.http_code == httplib.UNAUTHORIZED
        # ? POMOGI RAZOBRATSA S ETIMI KVADRATNIMI SKOBKAMI I ZNACHENIYAMI V NIH, POGALUYSTA:
        assert resp.json['inputErrors']['credentials'][0]['msg'] == 'This request is unauthenticated. Please provide ' \
                                                                    'credentials and try again.'
        # ? POCHEMU MI PRINTUEM resp.json, EGO U NAS NE NASHLA NIGDE. EST' r.json tolko. CHTO ETO TAKOE, resp.json?
        print(resp.json)

    # HW TC1 - delete folder that doesn't exist
    def test_delete_folder(self):
        folder = self.calls.get_random_name()
        resp = self.calls.delete_folder('privet')
        assert resp.http_code == httplib.NOT_FOUND

    def test_delete_non_existantfolder(self):
        folder_name = self.calls.get_random_name()
        resp = self.calls.delete_folder(folder_name)
        assert resp.http_code == httplib.NOT_FOUND
        print(resp.body[errorMessage] == 'Item does not exist')

    def test_delete_folder_wrong_accept_header(self):
        folder_name = self.calls.get_random_name()
        resp = self.calls.delete_folder(folder_name, accept='application/xml')
        assert resp.http_code == httplib.NOT_ACCEPTABLE
        assert resp.body['errorMessage'] == 'Not Acceptable'
        print(resp.http_code)
        print (resp.body)