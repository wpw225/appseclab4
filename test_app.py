import unittest
import requests
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

server_address="http://127.0.0.1:5000"
server_login=server_address + "/login"
user_register = server_address + "/register"
spell_check_url = server_address + "/spell_check"

def getCsrfToken(url, session):
    soup = BeautifulSoup(session.get(url).content, "html.parser")
    return soup.find('input', dict(name='csrf_token'))['value']

def getElementById(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    result = soup.find(id=eid)
    return result

def login_bypass(session=None):
    if session is None:
        session = requests.Session()
        session.verify = False
    csrftoken = getCsrfToken(spell_check_url, session)
    spell_check_data = {"post": "something", "csrf_token": csrftoken}
    r = session.post(spell_check_url, data=spell_check_data)
    result = getElementById(r.text, "result").get_text()
    return result

def login(uname, pword, twofactor, session=None):
    if session is None:
        session = requests.Session()
        session.verify = False
    csrftoken = getCsrfToken(server_login, session) 
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor, "csrf_token": csrftoken}
    r = session.post(server_login, data=test_creds)
    success = getElementById(r.text, "result")
    assert success != None, "Missing id='result' in your login respons"
    return "Success" in success.text

def register(uname, pword, twofactor, session=None):
    if session is None:
        session = requests.Session()
        session.verify = False
    csrftoken = getCsrfToken(user_register, session)
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor, "csrf_token": csrftoken}
    r = session.post(user_register, data=test_creds)
    success = getElementById(r.text, "success")
    if success is None:
        return False
    return "Success" in success.text

def spell_check(uname, pword, twofactor, inputtext, session=None):
    if session is None:
        session = requests.Session()
        session.verify = False
    csrftoken = getCsrfToken(server_login, session)
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor, "csrf_token": csrftoken}
    r = session.post(server_login, data=test_creds)
    success = getElementById(r.text, "result")
    assert success != None, "Missing id='result' in your login respons"
    if ("Success" in success.text):
        csrftoken = getCsrfToken(spell_check_url, session)
        spell_check_data = {"post": inputtext, "csrf_token": csrftoken}
        r = session.post(spell_check_url, data=spell_check_data)
        result = getElementById(r.text, "misspelled").get_text()
        return result
    else:
        return "" 



class FeatureTest(unittest.TestCase):

    def test_page_exists(self):
        PAGES = ["/","/register","/login","/spell_check"]
        for page in PAGES:
            req = requests.get(server_address + page, verify=False)
            self.assertEqual(req.status_code, 200)

    def test_login_bypass(self):
        resp = login_bypass()
        self.assertEqual(resp, "Please log in to access this page.")

    def test_registration(self):
        resp = register("test60","test60","")
        self.assertTrue(resp, "Registration successful")

    def test_2fa_registration(self):
        resp = register("test61","test61","01234567890")
        self.assertTrue(resp, "2FA Registration successful")

    def test_invalid_registration(self):
        resp = register("test30","test30","") #Duplicate ID
        self.assertFalse(resp, "Duplicate registration successful")

    def test_invalid_2fa_registration(self):
        resp = register("test31","test31","0123456789")
        self.assertFalse(resp, "Duplicate 2FA registration successful")

    def test_valid_login(self):
        resp = login("test60","test60","")
        self.assertTrue(resp, "success! you are logged in")

    def test_valid_2fa_login(self):
        resp = login("test61","test61","01234567890")
        self.assertTrue(resp, "success! you are logged in with 2fa")

#    def test_invalid_login(self):
#        resp = login("test30","badpass","")
#        self.assertFalse(resp, "Login authenticated an invalid uname/password")

#    def test_invalid_2fa_login(self):
#        resp = login("test31","test31","2222222222")
#        self.assertFalse(resp, "Login authenticated an invalid 2fa")

    def test_spellcheck_with_err(self):
        resp =  spell_check("test60","test60","","ther arre no wrong").strip().replace("\n", " ")
        self.assertEqual(resp, "Misspelled Words: ther arre")

    def test_spellcheck_wo_err(self):
        resp =  spell_check("test60","test60","","there are no wrong").strip().replace("\n", " ")
        self.assertEqual(resp, "Misspelled Words:")

    def test_spellcheck_with_special_char(self):
        resp =  spell_check("test60","test60","","th3re are 0 wrong!").strip().replace("\n", " ")
        self.assertEqual(resp, "Misspelled Words: th3re")



if __name__ == '__main__':
    unittest.main()

