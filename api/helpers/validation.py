"""
Helper functions for validation.
"""

# pylint:disable=no-else-return


def validate_json(keys, json_like_object, empty=False):
    """
    Check if keys are present.
    """
    missing = ""
    for key in keys:
        try:
            value = json_like_object[key]
            if isinstance(value, str):
                if not value.strip():
                    if empty is True:
                        pass
                    else:
                        missing += key + ', '
            else:
                if value is None:
                    if empty is True:
                        pass
                    else:
                        missing += key + ', '
                else:
                    pass
        except KeyError:
            missing += key + ', '
    if missing:
        return missing[:-2]
    else:
        return True
