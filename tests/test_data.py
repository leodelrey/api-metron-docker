import json


# ----------------------------------------------
#              CREATE TESTS
# ----------------------------------------------
def test_create_data(testapp):
    request_data = {
        "data": [
            {"name": "a", "value": 10},
            {"name": "a", "value": 30},
            {"name": "a", "value": 50},
            {"name": "b", "value": 50},
            {"name": "b", "value": 100},
            {"name": "c", "value": 100}
        ]
    }
    resp = testapp.post('/data/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 201


# ----------------------------------------------
#                 GET TESTS
# ----------------------------------------------
def test_get_all_data(testapp):
    response = testapp.get("/data/")
    assert response.status_code == 200
