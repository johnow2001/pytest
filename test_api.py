import mysql.connector
import pytest
import requests

url =  "https://jsonplaceholder.typicode.com/posts"

def test_set_up_db(set_up_db):
    try:
        set_up_db
    except Exception as err:
        print("Setup error ", err)

def test_get_by_id():
    rsp = requests.get(url=url + "/1")
    assert rsp.status_code == 200
    assert rsp.json()["userId"] == 1
    assert rsp.json()["id"] == 1
    assert "sunt aut facere repellat provident" in rsp.json()["title"]
    assert "quia et suscipit\nsu" in rsp.json()["body"]


def test_getsa(select_data):
    rsp = requests.get(url= url + "/1")
    rsp_data = rsp.json()
    exp_data = select_data

    print(rsp_data)
    print(exp_data)

    assert exp_data[0][0] ==  rsp_data["userId"]
    assert exp_data[0][1] ==  rsp_data["id"]
    assert exp_data[0][2] in rsp_data["title"]
    assert exp_data[0][3] in rsp_data["body"]

def test_tear_db_down(tear_db_down):
    try:
      tear_db_down
    except Exception as err:
      print("Teardown error ", err)
