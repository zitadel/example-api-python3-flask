import unittest
from validator import ZitadelIntrospectTokenValidator as v
from validator import ValidatorError

class TestValidatorToken(unittest.TestCase):
    def test_invalid_token(self):
        token = {'active': False}
        scopes = None
        request = None
        with self.assertRaises(ValidatorError) as error: 
            v.validate_token(None, token, scopes, request)
        self.assertEqual("{'code': 'invalid_token', 'description': 'Invalid token (active: false)'}", str(error.exception.error))

class TestValidatorMatchTokenScopes(unittest.TestCase):

    def test_no_scope_required(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}, 'write:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = None
        self.assertEqual(v.match_token_scopes(self, token, scopes), True)

    def test_one_valid_scope(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}, 'write:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = ['read:messages']
        self.assertEqual(v.match_token_scopes(self, token, scopes), True)
        
    def test_wrong_scope(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = ['write:messages']
        self.assertEqual(v.match_token_scopes(self, token, scopes), False)

    def test_and_scopes(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}, 'write:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = ['read:messages write:messages']
        self.assertEqual(v.match_token_scopes(self, token, scopes), True)
    
    def test_and_scopes_missing_claim(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = ['read:messages write:messages']
        self.assertEqual(v.match_token_scopes(self, token, scopes), False)
    
    def test_or_scopes(self):
        token = {'urn:zitadel:iam:org:project:roles': {'read:messages': {'170086305978381234': 'example.zitadel.cloud'}}}
        scopes = ['read:messages', 'write:messages']
        self.assertEqual(v.match_token_scopes(self, token, scopes), True)

if __name__ == '__main__':
    unittest.main()