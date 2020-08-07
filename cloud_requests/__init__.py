import json
import requests
import time
import jwt
import urllib

class CloudRequests():
"""
When making a requests to Google Cloud REST Service, it allows you to make a simple request without complicated authentication.

Parameters
----------
* external_auth_json: dict
    
    GCP Authentication JSON

    you can omit auth Parameter if request from Cloud REST Service internal to internal.

"""
    def __init__(self, external_auth_json = {}):
        self.inetral_cache = {}
        self.external_cache = {}
        
        self.client_email = external_auth_json.get("client_email")
        self.private_key_id = external_auth_json.get("private_key_id")
        self.private_key = external_auth_json.get("private_key")


    def post(self, url, data={}, external=True, **kwargs):
        """

        This function is POST request that automatically authenticates.

        Parameters
        ----------

        * `(required) url`: str

            Your Cloud REST Service URL.

            ```
            https://spider-yfir3gc5lx-an.a.run.app
            ```

        * `data`: dict (default: json)

            This parameter requested with application/json header.

            ```python
            {
                "fruit": "apple"
            }
            ```
        * `external`: bool (default: True)

            Set this value True to Send requests from outside of Cloud REST Service.

            Set this value False to Send requests from inside of Cloud REST Service (In Cloud Run Service to Cloud REST Service)

        * `kwargs`: kwargs

            additional `requests.post` parameters.

            ```python
            {
                "headers": {'Authorization': 'ABCDE'},
                "json": {"fruit":"apple"}
            }
            ```

        Examples
        --------

        ```python
        data = {}
        response = handler.post("YOUR Cloud REST Service URI (like Cloud Run URL)", data, external=True)

        print(response.status_code)
        print(response.json())
        ```

        result:

        * Your Cloud REST Service Response Returned.
        ```
        {"message":"hello world"}
        ```

        Returns
        -------

        * Your Cloud REST Service Response: `requests.models.Response`

        """
        if external:
            return self.external_post(url, data, **kwargs)
        else:
            return self.internal_post(url, data, **kwargs)

    def get(self, url, data={}, external=True, **kwargs):
        """
        This function is POST request that automatically authenticates.

        Parameters
        ----------

        * `(required) url`: str

            Your Cloud REST Service URL.

            ```
            https://spider-yfir3gc5lx-an.a.run.app
            ```

        * `data`: dict (default: json)

            This parameter requested with application/json header.

            ```python
            {
                "fruit": "apple"
            }
            ```
        * `external`: bool (default: True)

            Set this value True to Send requests from outside of Cloud REST Service.

            Set this value False to Send requests from inside of Cloud REST Service (In Cloud Run Service to Cloud REST Service)

        * `kwargs`: kwargs

            additional `requests.post` parameters.

            ```python
            {
                "headers": {'Authorization': 'ABCDE'},
                "json": {"fruit":"apple"}
            }
            ```

        Examples
        --------

        ```python
        data = {}
        response = handler.get("YOUR Cloud REST Service URI (like Cloud Run URL)", data, external=True)

        print(response.status_code)
        print(response.json())
        ```

        result:

        * Your Cloud REST Service Response Returned.

        ```
        {"message":"hello world"}
        ```

        Returns
        -------

        * Your Cloud REST Service Response: `requests.models.Response`
        """
        if external:
            return self.external_get(url, data, **kwargs)
        else:
            return self.external_get(url, data, **kwargs)

    def external_post(self, url, data={}, **kwargs):
        token = self._get_external_token(url)
        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "json":data
        })

        return requests.post(url, **kwargs)

    def internal_post(self, url, data={}, **kwargs):
        token = self._get_inetral_token(url)

        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "json":data
        })

        return requests.post(url, **kwargs)

    def external_get(self, url, data={}, **kwargs):
        token = self._get_external_token(url)
        kwargs.update({
            "headers": {'Authorization': 'Bearer %s'%(token)},
            "params":data
        })

        return requests.get(url, **kwargs)

    def internal_get(self, url, data={}, **kwargs):
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

