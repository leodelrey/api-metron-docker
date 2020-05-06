# /src/views/DataView

from flask import request, json, Response, Blueprint
from collections import defaultdict
from ..models.DataModel import DataModel, DataSchema
data_api = Blueprint('data_api', __name__)
data_schema = DataSchema()


@data_api.route('/', methods=['POST'])
def create():
    """
    The function to create a character (with or without hat associated)
    Returns:
        Response: The HTTP response (201 if created, 400 if error)
    """

    # Retrieve the data
    req_data = request.get_json()

    # Create dictionaries to sum and count data with same name
    sums = defaultdict(int)
    counts = defaultdict(int)

    # Iterate over the array
    for item in req_data['data']:
        sums[item['name']] += item['value']
        counts[item['name']] += 1

    # Calculate the mean for each item
    means = {k: float(sums[k])/counts[k] for k in sums.keys()}

    for name in means:
        # Create the data row
        data = DataModel(name, means[name])
        data.save()

    return custom_response({'message': 'Data created'}, 201)


@data_api.route('/', methods=['GET'])
def get_data():
    """
    The function to get all the data in database
    Returns:
        Response: The HTTP response (200)
    """
    # Retrieve all the data
    data = DataModel.get_data()
    # Serialize the data with schema
    ser_data = data_schema.dump(data, many=True)
    return custom_response(ser_data, 200)


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
