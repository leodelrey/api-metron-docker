#/src/views/HatView

from flask import request, json, Response, Blueprint
from ..models.CharacterModel import CharacterModel, CharacterSchema
from ..models.HatModel import HatModel, HatSchema, ColorType

hat_api = Blueprint('hat_api', __name__)
hat_schema = HatSchema()
character_schema = CharacterSchema()

@hat_api.route('/',methods=['POST'])
def create():
    """
    The function to create a hat
    Returns:
        Response: The HTTP response (201 if created, 400 if error)
    """

    req_data = request.get_json()

    # Retrieve the character id
    char_id=req_data.get('character_id')

    # No character specified
    if not char_id:
        return custom_response({'message':'character not specified'}, 400)
    
    # Color doens't exist
    if req_data.get('color') and req_data.get('color') not in ColorType._member_names_ :
        return custom_response({'message':'color doesn\'t exist'}, 400)
    
    # Search the character
    character = CharacterModel.get_char(char_id)
    # The character doens't exist
    if not character:
        return custom_response({'message':'character doesn\'t exist'}, 400)

    # Serialize the character with schema
    ser_char = character_schema.dump(character)

    # The character already has a hat
    if HatModel.char_has_hat(char_id):
        return custom_response({'message':'the character specified already has a hat'}, 400)

    # Check rules
    err=HatModel.verify_hat_rules(ser_char,req_data)
    if err:
        return err

    # Create the hat
    hat = HatModel(req_data)
    hat.save()

    return custom_response({'message':'hat created'}, 201)


@hat_api.route('/', methods=['GET'])
def get_all_hat():
    """
    The function to get all the hats in database
    Returns:
        Response: The HTTP response (200)
    """
    hats = HatModel.get_all_hats()
    ser_hats = hat_schema.dump(hats, many=True)
    return custom_response(ser_hats, 200)  


@hat_api.route('/<int:hat_id>', methods=['GET'])
def get_hat(hat_id):
    """
    The function to get a single hat
    Parameters:
        hat_id (int): The primary key of the character
    Returns:
        Response: The HTTP response (200 if updated, 404 if hat not found)
    """
    hat = HatModel.get_hat(hat_id)
    if not hat:
        return custom_response({'error': 'hat not found'}, 404)
    
    ser_hat = hat_schema.dump(hat)

    return custom_response(ser_hat, 200)


@hat_api.route('/<int:hat_id>', methods=['PUT'])
def update(hat_id):
    """
    The function to update a hat
    Parameters:
        hat_id (int): The primary key of the hat
    Returns:
        Response: The HTTP response (200 if updated, 400 if error)
    """

    # We retrieve and search the data
    req_data = request.get_json()
    hat = HatModel.get_hat(hat_id)

    # The hat doesn't exist
    if not hat:
        return custom_response({'error':'hat not found'}, 400)

    # Get and serialize the character with schema
    character = CharacterModel.get_char(hat.character_id)
    ser_char = character_schema.dump(character)

    # Check rules
    err=HatModel.verify_hat_rules(ser_char,req_data)
    if err:
        return err

    # Update the hat
    hat = HatModel.get_hat(hat_id)
    hat.update(req_data)

    # Serialize new hat to print
    ser_hat = hat_schema.dump(hat)

    return custom_response(ser_hat, 200)

@hat_api.route('/<int:hat_id>', methods=['DELETE'])
def delete(hat_id):
    """
    The function to delete a hat
    Parameters:
        hat_id (int): The primary key of the hat
    Returns:
        Response: The HTTP response (200 if deleted, 400 if error)
    """
    # We search the hat
    hat = HatModel.get_hat(hat_id)

    # The hat doesn't exist
    if not hat:
        return custom_response({'error':'hat not found'}, 400)

    # We delete the hat
    hat.delete()
    return custom_response({'message':'deleted'}, 200)

def custom_response(res, status_code):
    """
    Create a JSON response with status code to the HTTP request
    Parameters:
        res (dict): The result to print
        status_code (int): The status code of the response
    Returns:
        Response: The HTTP response in JSON format
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )