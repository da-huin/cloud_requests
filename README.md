<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./static/icon.png" alt="Project logo" ></a>
 <br>

 
</p>

<h3 align="center">Cloud Requests</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/da-huin/cloud_requests.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/da-huin/cloud_requests.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> When making a requests to Google Cloud REST Service, it allows you to make a simple request without complicated authentication.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

When making a requests to Google Cloud REST Service, it allows you to make a simple request without complicated authentication. 

You can use following functions.

* [Post](#post)

* [Get](#get)

## 🏁 Getting Started <a name = "getting_started"></a>

### Installing

```
pip install cloud_requests
```

<a name="prerequisites"></a>

### Prerequisites

#### 1. (Required) Download Authentication JSON

1. From [Google Cloud Platform Console](https://console.developers.google.com/project), `create project`, if you already have a project, you can omit it.

    ![create_project](./static/create_project.png)

1. From [Google Credential](https://console.developers.google.com/apis/api/iamcredentials.googleapis.com/credentials) choose `Create credentials` > `Service Account`.

    ![credentials_service_account](./static/credentials_service_account.png)

1. Fill out the form and click `Create Key`. 
    
    <img src="./static/credentials_service_account_form.png" alt="credentials_service_account_form" width="500"/>
    <img src="./static/create_service_account_2.png" alt="create_service_account_2" width="500"/>
    <img src="./static/create_service_account_3.png" alt="create_service_account_3" width="500"/>

1. Click the `account you just created`, from the `Service Accounts list`.

    <img src="./static/select_just.png" alt="select_just" />

1. click the `ADD KEY` > `Create new key`

    ![credential_create_new_key](./static/credential_create_new_key.png)

1. Set the `Key type` to JSON and click `CREATE` button

    ![credential_create_new_key_create](./static/credential_create_new_key_create.png)

1. The JSON file automatically saved, which is used to authenticate the spreadsheet.

    ![private_key_saved](./static/private_key_saved.png)

#### 2. (Required) Create Handler

Use this code to create handler.

```python
import cloud_requests

with open("your_auth_file.json") as fp:
    auth = json.loads(fp.read())

handler = cloud_requests.CloudRequests(auth)

print(handler)
```

result:
```
<cloud_requests.CloudRequests object at 0x1016d4828>
```

## 🎈 Usage <a name="usage"></a>

Please check [Prerequisites](#prerequisites) before starting `Usage`.

### 🌱 POST <a name="post"></a>

This function is POST request that automatically authenticates.

**Parameters**

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

**Examples**

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

**Returns**

* Your Cloud REST Service Response: `requests.models.Response`


### 🌱 GET <a name="get"></a>

This function is POST request that automatically authenticates.

**Parameters**

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

**Examples**

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

**Returns**

* Your Cloud REST Service Response: `requests.models.Response`

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Title icon made by [Freepik](https://www.flaticon.com/kr/authors/freepik).

- If you have a problem. please make [issue](https://github.com/da-huin/cloud_requests/issues).

- Please help develop this project 😀

- Thanks for reading 😄
