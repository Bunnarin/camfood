import json
from datetime import date, datetime
from django import template
from django.utils.formats import date_format

register = template.Library()

@register.filter
def get_attr_from_object(value, arg):
    """
    Gets an attribute of an object dynamically using its string name.
    Example: {{ obj|get_attr_from_object:'my_field_name' }}
    Handles cases where the attribute might be a callable (like get_FOO_display).
    """
    if "." in arg:
        # chain the attribute
        primary_attr = getattr(value, arg.split(".")[0])
        secondary_attr = getattr(primary_attr, arg.split(".")[1])
        val = secondary_attr
    else:
        val = getattr(value, arg)

    # check if attr is data obj
    if isinstance(val, (date, datetime)):
        return date_format(val, format="m/d/Y", use_l10n=True)
    # transform true false to yes no
    if isinstance(val, bool):
        return "Yes" if val else "No"
    # handle related managers (reverse many-to-one relationships)
    if hasattr(val, 'all'):
        return ", ".join(str(item) for item in val.all())
    return val

@register.filter
def replace(value, arg):
    """
    Usage: {{ value|replace:"old_string,new_string" }}
    """
    if isinstance(value, str) and isinstance(arg, str):
        parts = arg.split(',', 1)  # Split only on the first comma
        if len(parts) == 2:
            old_string, new_string = parts[0], parts[1]
            return value.replace(old_string, new_string)
    return value