import unittest
import app as myapp
import json

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = myapp.app.test_client()
        self.host = 'http://localhost:5000'

    def test_corret_get_company_info(self):
        # parameter : companyname
        response = self.app.get(self.host+'/company?companyname=ted')
        ret = json.loads(response.get_data().decode("utf-8"))
        if len(ret):
            print("OK", ret)

        # parameter : tagname
        response = self.app.get(self.host+'/company?tagname=ソウル31')
        ret = json.loads(response.get_data().decode("utf-8"))
        if len(ret):
            print("OK", ret)

        response = self.app.get(self.host+'/company?tagname=HR')
        ret = json.loads(response.get_data().decode("utf-8"))
        if len(ret):
            print("OK", ret)

    def test_wrong_get_company_info(self):
        # parameter : wrong parameter
        response = self.app.get(self.host+'/company?wrongparameter=ted')
        ret = json.loads(response.get_data().decode("utf-8"))
        if 'fail' in ret['responsemessage'] :
            print("OK")

    def test_correct_add_tag(self):
        response = self.app.post(self.host + '/tag/wanted/한국')
        ret = json.loads(response.get_data().decode("utf-8"))
        if 'success' in ret['responsemessage']:
            print("OK")

    def test_wrong_add_tag(self):
        # 중복으로 오류
        response = self.app.post(self.host + '/tag/wanted/한국')
        ret = json.loads(response.get_data().decode("utf-8"))
        if 'fail' in ret['responsemessage']:
            print("OK")
    
    def test_correct_delete_tag(self):
        response = self.app.delete(self.host + '/tag/wanted/한국')
        ret = json.loads(response.get_data().decode("utf-8"))
        if 'success' in ret['responsemessage']:
            print("OK")

    def test_wrong_delete_tag(self):
        # 없는 데이터 요청으로 오류
        response = self.app.delete(self.host + '/tag/wanted/한국')
        ret = json.loads(response.get_data().decode("utf-8"))
        if 'fail' in ret['responsemessage']:
            print("OK")

if __name__ == '__main__':
    unittest.main()

