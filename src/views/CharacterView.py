# /src/views/CharacterView

from flask import request, json, Response, Blueprint
from ..models.CharacterModel import CharacterModel, CharacterSchema
from ..models.HatModel import HatModel, ColorType

character_api = Blueprint('character_api', __name__)
character_schema = CharacterSchema()


@character_api.route('/', methods=['POST'])
def create():
    """
    The function to create a character (with or without hat associated)
    Returns:
        Response: The HTTP response (201 if created, 400 if error)
    """

    # Retrieve the data
    req_data = request.get_json()
    hat_data = req_data.pop('hat', None)

    # Check rules
    err = CharacterModel.verify_char_rules(req_data)
    if err:
        return custom_response(err, 400)

    # Create the character
    character = CharacterModel(req_data)

    # Create an associated hat if requested
    if hat_data:
        # Color doens't exist
        if (req_data.get('color') and
                req_data.get('color') not in ColorType._member_names_):
            return custom_response({'message': 'color doesn\'t exist'}, 400)
        # Check hat rules
        err = HatModel.verify_hat_rules(req_data, hat_data)
        if err:
            return custom_response(err, 400)
        # Save the character and create the hat
        character.save()
        hat = HatModel({'color': hat_data.get('color'),
                        'character_id': character.id})
        hat.save()

    # Create a character without hat
    else:
        character.save()

    return custom_response({'message': 'character created'}, 201)


@character_api.route('/', methods=['GET'])
def get_all_char():
    """
    The function to get all the characters in database
    Returns:
        Response: The HTTP response (200)
    """
    # Retrieve all the characters
    characters = CharacterModel.get_all_chars()
    # Serialize the characters with schema
    ser_chars = character_schema.dump(characters, many=True)
    return custom_response(ser_chars, 200)


@character_api.route('/<int:character_id>', methods=['GET'])
def get_char(character_id):
    """
    The function to get a single character
    Parameters:
        character_id (int): The primary key of the character
    Returns:
        Response: The HTTP response (200 if updated, 404 if not found)
    """
    # Search the character
    character = CharacterModel.get_char(character_id)
    # The character doesn't exist
    if not character:
        return custom_response({'error': 'character not found'}, 404)

    # Serialize the characters with schema
    ser_char = character_schema.dump(character)
    return custom_response(ser_char, 200)


@character_api.route('/<int:character_id>', methods=['PUT'])
def update(character_id):
    """
    The function to update a character
    Parameters:
        character_id (int): The primary key of the character
    Returns:
        Response: The HTTP response (200 if updated, 400 if error)
    """
    # We retrieve the data and search the character
    req_data = request.get_json()
    character = CharacterModel.get_char(character_id)

    # The character doesn't exist
    if not character:
        return custom_response({'error': 'character not found'}, 400)

    # Serialize the character and update values
    ser_char = character_schema.dump(character)
    for key in req_data:
        ser_char[key] = req_data[key]
    # Check character rules
    err = CharacterModel.verify_char_rules(ser_char)
    if err:
        return custom_response(err, 400)

    # Check hat rules if character has a hat
    if HatModel.char_has_hat(character_id):
        hat_d = HatModel.get_hat_by_char(character_id)
        err = HatModel.verify_hat_rules(ser_char, {'color': hat_d.color.value})
        if err:
            return custom_response(err, 400)

    # Update the data
    character.update(ser_char)

    return custom_response(ser_char, 200)


@character_api.route('/<int:character_id>', methods=['DELETE'])
def delete(character_id):
    """
    The function to delete a character
    Parameters:
        character_id (int): The primary key of the character
    Returns:
        Response: The HTTP response (200 if deleted, 400 if error)
    """

    # We search the character
    character = CharacterModel.get_char(character_id)

    # The caracter doesn't exist
    if not character:
        return custom_response({'error': 'character not found'}, 400)

    # The character has a hat : we delete it
    if HatModel.char_has_hat(character_id):
        hat = HatModel.get_hat_by_char(character_id)
        hat.delete()

    # We delete the character
    character.delete()
    return custom_response({'message': 'deleted'}, 200)


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
