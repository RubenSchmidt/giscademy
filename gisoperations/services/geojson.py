import json


def get_feature_dict(geom):
    dict = json.loads(geom.json)
    # The json property of the geos geometries only return the geometry part of the geojson.
    # We need to create the correct geojson feature.
    feature_dict = {
        "type": "Feature",
        "properties": {},
        "geometry": dict
    }
    return feature_dict
