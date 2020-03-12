import json
import requests
import urllib.parse
import urllib.request
import urllib.response
from urllib.error import URLError, HTTPError

__author__ = 'paulgullett'

#top_level_url = "http://thinqsteps.gullettdoherty.com/"
top_level_url = "https://www.thinqsteps.com/"

def rest_handler():

    username = 'paul.gullett@btopenworld.com'
    password = 'Longtek123'

    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, top_level_url, username, password)

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)

    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

    return True


def rest_handler_with_username(username, password):

    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, top_level_url, username, password)

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)

    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

    return True


def post_register_user(userdata, url, callback):

    rest_handler_with_username("", "")

    request_url = top_level_url + "api/userregister"
    req = urllib.request.Request(request_url)

    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(userdata)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    try:
        response = urllib.request.urlopen(req, jsondataasbytes)
        answer = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    except HTTPError as e:
        print('post_jsondata HTTPError code: ', e.code)
        return False
    except URLError as e:
        print('post_jsondata URLError Reason: ', e.reason)
        return False
    else:
        print(answer['data'])
        idaccounts = answer['data'][0]['idaccounts']
        post_register_user_image(idaccounts, userdata, url, callback)
        return True


def post_register_user_image(idaccounts, userdata, url, callback):

    identifier = userdata['userdata']['identifier']

    file_name = identifier + ".jpg"
    file_path = "../res/" + file_name

    urllib.request.urlretrieve(url, file_path)

    file = open(file_path, "rb")

    request_url = top_level_url + "api/userprofilepictureuploadprelogin"

    files = {'file': file}

    params = {'idaccounts': idaccounts, 'identifier': identifier}

    try:
        response = requests.post(request_url, files=files, auth=(userdata['email'], userdata['password']), data=params)
    except requests.exceptions.RequestException as e:
        print('post_jsondata HTTPError code: ', e)
        return False
    else:
        print(response.json())
        callback(idaccounts)


def delete_user_by_id(idaccounts):

    rest_handler()

    request_url = top_level_url + "api/userdatabyid/" + idaccounts
    req = urllib.request.Request(request_url)
    req.method = 'DELETE'

    try:
        response = urllib.request.urlopen(req)
        answer = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    except HTTPError as e:
        print('delete_user_by_id HTTPError code: ', e.code)
        return False
    except URLError as e:
        print('delete_user_by_id URLError Reason: ', e.reason)
        return False
    else:
        print(answer['data'])
        return True


def get_subscription_number():

    rest_handler()

    request_url = top_level_url + "api/subscriptionnumber"
    req = urllib.request.Request(request_url)

    try:
        response = urllib.request.urlopen(req)
        answer = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    except HTTPError as e:
        print('delete_user_by_id HTTPError code: ', e.code)
        return None
    except URLError as e:
        print('delete_user_by_id URLError Reason: ', e.reason)
        return None
    else:
        print(answer['data'][0])
        return answer['data'][0]['subscriptionnumber']


def add_dummy_subscription(data):

    rest_handler()

    request_url = top_level_url + "api/subscription"
    req = urllib.request.Request(request_url)

    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    try:
        response = urllib.request.urlopen(req, jsondataasbytes)
        answer = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    except HTTPError as e:
        print('add_dummy_subscription HTTPError code: ', e.code)
        return None
    except URLError as e:
        print('add_dummy_subscription URLError Reason: ', e.reason)
        return None
    else:
        print(answer['data'][0])
        return answer['data'][0]


def get_dummy_accounts():

    rest_handler()

    request_url = top_level_url + "api/dummyaccountslist/"
    req = urllib.request.Request(request_url)

    try:
        response = urllib.request.urlopen(req)
        answer = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    except HTTPError as e:
        print('get_dummy_accounts Error code: ', e.code)
        return None
    except URLError as e:
        print('get_dummy_accounts Reason: ', e.reason)
        return None
    else:
        return answer['data']