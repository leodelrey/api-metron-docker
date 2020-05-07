from src.models.CharacterModel import CharacterModel
from src.models.HatModel import HatModel, ColorType
import json


# ----------------------------------------------
#              CREATE TESTS
# ----------------------------------------------
def test_create_yellow_hat_to_p_name_char(testapp):
    request_data = {
        'name': 'Pierre',
        'age': 23,
        'weight': 66.5,
        'human': True,
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'YELLOW',
        'character_id': 1
    }
    resp = testapp.post('/hat/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(10)
    assert not HatModel.get_hat(3)


def test_create_hat_to_non_human_char(testapp):
    request_data = {
        'name': 'Bjork',
        'age': 83,
        'weight': 600,
        'human': False
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'PURPLE',
        'character_id': 1
    }
    resp = testapp.post('/hat/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(11)
    assert not HatModel.get_hat(3)


def test_create_hat_to_char_with_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 65.5,
        'human': True,
        'hat':  {
            'color': 'PURPLE'
        }
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'GREEN',
        'character_id': 12
    }
    resp = testapp.post('/hat/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(12)
    assert HatModel.get_hat(5)
    assert not HatModel.get_hat(6)


def test_create_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 65.5,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'GREEN',
        'character_id': 13
    }
    resp = testapp.post('/hat/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 201
    assert CharacterModel.get_char(13)
    assert HatModel.get_hat(6)


# ----------------------------------------------
#              DELETE TESTS
# ----------------------------------------------
def test_delete_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True,
        'hat':  {
            'color': 'YELLOW'
        }
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    resp = testapp.delete('/hat/7')

    # Tests
    assert resp.status_code == 200
    assert not HatModel.get_hat(7)


def test_delete_char_doesnt_exit(testapp):
    resp = testapp.delete('/hat/1')

    # Tests
    assert resp.status_code == 400
    assert not HatModel.get_hat(1)


# ----------------------------------------------
#              UPDATE TESTS
# ----------------------------------------------
def test_update_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True,
        'hat':  {
            'color': 'PURPLE'
        }
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'YELLOW'
    }
    resp = testapp.put('/hat/8', content_type='application/json',
                       data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 200
    assert HatModel.get_hat(8).color == ColorType.YELLOW


def test_update_yellow_hat_to_char_with_p_name(testapp):
    request_data = {
        'name': 'Pierre',
        'age': 23,
        'weight': 66.5,
        'human': True,
        'hat':  {
            'color': 'PURPLE'
        }
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'color': 'YELLOW'
    }
    resp = testapp.put('/hat/9', content_type='application/json',
                       data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert HatModel.get_hat(9).color == ColorType.PURPLE


def test_update_character_related_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))
    request_data = {
        'name': 'Alexandre',
        'age': 28,
        'weight': 70,
        'human': True,
        'hat':  {
            'color': 'PURPLE'
        }
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'character_id':  17
    }
    resp = testapp.put('/hat/10', content_type='application/json',
                       data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 200
    assert CharacterModel.get_char(17).hat
    assert not CharacterModel.get_char(18).hat
    assert HatModel.get_hat(10).character_id == 17


# ----------------------------------------------
#                 GET TESTS
# ----------------------------------------------
def test_get_hat_doesnt_exist(testapp):
    response = testapp.get("/hat/1")
    assert response.status_code == 404


def test_get_all_hat(testapp):
    response = testapp.get("/hat/")
    assert response.status_code == 200
