import json
import requests
import time
import jwt
import urllib

class CloudRequests():

    def __init__(self, external_auth_json = {}):
        """
        클라우드런에 올라간 서비스는 기본적으로 인증이 필요한데, 그 인증을 자동으로 해주고 요청을 보내주는 클래스입니다.
        """
        self.inetral_cache = {}
        self.external_cache = {}
        
        self.client_email = external_auth_json.get("client_email")
        self.private_key_id = external_auth_json.get("private_key_id")
        self.private_key = external_auth_json.get("private_key")


    def post(self, url, data={}, external=True, **kwargs):
        if external:
            return self.external_post(url, data, **kwargs)
        else:
            return self.internal_post(url, data, **kwargs)

    def get(self, url, data={}, external=True, **kwargs):
        if external:
            return self.external_get(url, data, **kwargs)
        else:
            return self.external_get(url, data, **kwargs)

    def external_post(self, url, data={}, **kwargs):
        """
        외부에서 클라우드 런 서비스로 POST 요청을 보낼 때 사용되는 함수입니다.
        """
        token = self._get_external_token(url)
        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "json":data
        })

        return requests.post(url, **kwargs)

    def internal_post(self, url, data={}, **kwargs):
        """
        내부에서 클라우드 런 서비스로 POST 요청을 보낼 때 사용되는 함수입니다.
        """        
        token = self._get_inetral_token(url)

        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "json":data
        })

        return requests.post(url, **kwargs)

    def external_get(self, url, data={}, **kwargs):
        """
        외부에서 클라우드 런 서비스로 GET 요청을 보낼 때 사용되는 함수입니다.
        """                
        token = self._get_external_token(url)
        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "params":data
        })

        return requests.get(url, **kwargs)

    def internal_get(self, url, data={}, **kwargs):
        """
        내부에서 클라우드 런 서비스로 GET 요청을 보낼 때 사용되는 함수입니다.
        """
        token = self._get_inetral_token(url)

        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "params":data
        })

        return requests.get(url, **kwargs)


    def _has_token_expired(self, token):
        exp = jwt.decode(token, verify=False).get("exp")

        if exp == None or not isinstance(exp, int):
            raise Exception("cloud token exp is none.")

        now = int(time.time())
        return exp < now


    def _get_external_token(self, url):
        """
        외부에서 요청 할 때 필요한 토큰을 받아오는 함수입니다.
        """
        parse_result = urllib.parse.urlparse(url)
        base_url = "%s://%s"%(parse_result[0], parse_result[1])

        token = None
        cache_token = self.external_cache.get(base_url)

        if cache_token and not self._has_token_expired(cache_token):
            print("external_token cached.")
            token = cache_token
        else:
            signed_jwt = self._create_signed_jwt(url)
            token = self._exchange_jwt_for_token(signed_jwt)
            self.external_cache.update({base_url: token})

        return token


    # Cloud Run 내부
    def _get_inetral_token(self, url):
        """
        클라우드런 내부에서 요청 할 때 필요한 토큰을 받아오는 함수입니다.
        """        
        token = ""
        cache_token = self.inetral_cache.get(url)
        if cache_token != None and not self._has_token_expired(cache_token):
            print("interal_token cached."%(cache_token))
            token = cache_token
        else:
            metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

            token_request_url = metadata_server_token_url + url
            

            token_request_headers = {'Metadata-Flavor': 'Google'}


            token_response = requests.get(token_request_url, headers=token_request_headers)
            token = token_response.content.decode("utf-8")
            
            self.inetral_cache.update({url: token})

        return token

    def _create_signed_jwt(self, run_service_url):
        iat = time.time()
        exp = iat + 3600
        payload = {
            'iss': self.client_email,
            'sub': self.client_email,
            'target_audience': run_service_url,
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'iat': iat,
            'exp': exp
        }
        additional_headers = {
            'kid': self.private_key_id
        }
        signed_jwt = jwt.encode(
            payload,
            self.private_key,
            headers=additional_headers,
            algorithm='RS256'
        )

        return signed_jwt

    def _exchange_jwt_for_token(self, signed_jwt):
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': signed_jwt
        }
        token_request = requests.post(
            url='https://www.googleapis.com/oauth2/v4/token',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=urllib.parse.urlencode(body)
        )

        return token_request.json()['id_token']

