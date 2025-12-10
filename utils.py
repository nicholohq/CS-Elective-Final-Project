from flask import jsonify, Response, request
from dicttoxml import dicttoxml

def to_json(data):
    return jsonify(data)

def to_xml(data, root="data"):
    xml_data = dicttoxml(data, custom_root=root, attr_type=False)
    return Response(xml_data, mimetype="application/xml")

def format_response(data, root="data"):
    fmt = request.args.get("format", "json").lower()

    if fmt == "xml":
        return to_xml(data, root=root)

    return to_json(data)
