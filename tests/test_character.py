from src.models.CharacterModel import CharacterModel
from src.models.HatModel import HatModel
import json


# ----------------------------------------------
#              CREATE TESTS
# ----------------------------------------------
def test_create_p_char_with_yellow_hat(testapp):
    request_data = {
        'name': 'Pierre',
        'age': 23,
        'weight': 66.5,
        'human': True,
        'hat':  {
            'color': 'YELLOW'
        }
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert not CharacterModel.get_char(1)
    assert not HatModel.get_hat(1)


def test_create_non_human_char_with_hat(testapp):
    request_data = {
        'name': 'Bjork',
        'age': 83,
        'weight': 600,
        'human': False,
        'hat':  {
            'color': 'PURPLE'
        }
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 400
    assert not CharacterModel.get_char(1)
    assert not HatModel.get_hat(1)


def test_create_char_negative_age(testapp):
    request_data = {
        'name': 'Alexandre',
        'age': -1,
        'weight': 62,
        'human': True
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 400
    assert not CharacterModel.get_char(1)


def test_create_human_fat_char_under_ten_years_old(testapp):
    request_data = {
        'name': 'Tristan',
        'age': 8,
        'weight': 85,
        'human': True
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 400
    assert not CharacterModel.get_char(1)


def test_create_char(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 201
    assert CharacterModel.get_char(1)
    assert not HatModel.get_hat_by_char(1)


def test_create_char_with_hat(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True,
        'hat':  {
            'color': 'YELLOW'
        }
    }
    resp = testapp.post('/character/', content_type='application/json',
                        data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 201
    assert CharacterModel.get_char(2)
    assert HatModel.get_hat_by_char(2)


# ----------------------------------------------
#              DELETE TESTS
# ----------------------------------------------
def test_delete_char(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    resp = testapp.delete('/character/3')

    # Tests
    assert resp.status_code == 200
    assert not CharacterModel.get_char(3)


def test_delete_char_with_hat(testapp):
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
    resp = testapp.delete('/character/4')

    # Tests
    assert resp.status_code == 200
    assert not CharacterModel.get_char(4)
    assert not HatModel.get_hat_by_char(4)


def test_delete_char_doesnt_exit(testapp):
    resp = testapp.delete('/character/1')

    # Tests
    assert resp.status_code == 400
    assert not CharacterModel.get_char(1)


# ----------------------------------------------
#              UPDATE TESTS
# ----------------------------------------------
def test_update_char(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 66.5,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))
    request_data = {
        'name': 'Maxime'
    }
    resp = testapp.put('/character/5', content_type='application/json',
                       data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 200
    assert CharacterModel.get_char(5).name == 'Maxime'


def test_add_p_in_name_to_char_with_yellow_hat(testapp):
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
    request_data = {
        'name': 'Pierre'
    }
    resp = testapp.put('/character/6', content_type='application/json',
                       data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(6).name == 'Leo'


def test_update_human_false_to_char_with_hat(testapp):
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
        'human': False
    }
    resp = testapp.put('/character/7', content_type='application/json',
                       data=json.dumps(request_data))
    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(7).human is True


def test_update_char_negative_age(testapp):
    request_data = {
        'name': 'Leo',
        'age': 23,
        'weight': 62,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'age': -2
    }
    resp = testapp.put('/character/8', content_type='application/json',
                       data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(8).age == 23


def test_update_human_fat_char_to_under_ten_years_old(testapp):
    request_data = {
        'name': 'Tristan',
        'age': 30,
        'weight': 85,
        'human': True
    }
    testapp.post('/character/', content_type='application/json',
                 data=json.dumps(request_data))

    request_data = {
        'age': 7
    }
    resp = testapp.put('/character/9', content_type='application/json',
                       data=json.dumps(request_data))

    # Tests
    assert resp.status_code == 400
    assert CharacterModel.get_char(9).age == 30


# ----------------------------------------------
#                GET TESTS
# ----------------------------------------------
def test_get_char_doesnt_exist(testapp):
    response = testapp.get("/character/2")
    assert response.status_code == 404


def test_get_all_char(testapp):
    response = testapp.get("/character/")
    assert response.status_code == 200
