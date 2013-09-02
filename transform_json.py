"""
Module for parsing and validating the json for each transform.

{
    "model_tags": [],
    "inputs": [],
    "outputs": [],
    "parameters": {
        "float_with_bounds": [0.1, 0.2],
        "unordered_enum": [1,2,3],
        "int_with_bounds": [10,90],
        "sample_distribution": {
            "name": "normal",
            "mean": 0.8,
            "std": 0.3
        }
    },
    "removed_tags": [],
    "other_settings_with_default": 2
}
"""

import json

from distributions import DistributionFactory


def parameter_parser(val):
    """ parses a distribution for a parameter
    """
    if isinstance(val, dict):
        params = val  # the input is a distribution
    elif isinstance(val, list):
        params = dict(name="enum", enum=val)
        if len(val) == 2:
            if isinstance(val[0], int) and isinstance(val[1], int):
                params = dict(name="quniform", low=val[0], high=val[1], q=1)
            elif isinstance(val[0], (int, float)) and isinstance(val[1], (int, float)):
                params = dict(name="uniform", low=val[0], high=val[1], q=1)
    else:
        raise Exception("Incorrect transform parameter")
    return DistributionFactory.create(params)


def parameters_parser(parsed, parameter_dict):
    """ parses input parameters for the transform
    """
    parameters = {}
    if parameter_dict is not None:
        assert isinstance(parameter_dict, dict), parameter_dict
        for param_name, val in parameter_dict.items():
            parameters[param_name] = parameter_parser(val)
    parsed["parameters"] = parameters
    return parsed


def input_parser(val):
    pass  # TODO


def inputs_parser(parsed, input_list):
    assert isinstance(input_list, list), input_list
    inputs = [input_parser(item) for item in input_list]
    parsed["inputs"] = inputs
    return parsed


def transform_json_pipeline(transform_json):
    """ applies all parsers for the transform json
    """
    transform_dict = json.loads(transform_json)

    pipeline = (
        ('parameters', parameters_parser),
    )

    parsed = {}
    for key, function in pipeline:
        try:
            value = transform_dict.pop(key)
        except KeyError:
            value = None
        parsed = function(parsed, value)
    return parsed
