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
        
    return val

@register.filter
def pretty_json(value):
    """
    Format a JSON string or Python object as a simple string.
    Usage in template: {{ your_json|pretty_json }}
    Example: {'name': 'John', 'age': 30} becomes "name: John, age: 30"
    """
    if not value:
        return ""
    
    try:
        # If value is already a string, try to load it as JSON
        if isinstance(value, str):
            json_obj = json.loads(value)
        else:
            # If it's already a Python object, use it directly
            json_obj = value
            
        # Convert dictionary to string in format "key: val, key: val"
        if isinstance(json_obj, dict):
            formatted_str = ", ".join(f"{k}: {v}" for k, v in json_obj.items())
            return formatted_str
        # Handle lists/arrays
        elif isinstance(json_obj, (list, tuple)):
            return ", ".join(str(item) for item in json_obj)
        # Handle other JSON-serializable types
        else:
            return str(json_obj)
            
    except (TypeError, ValueError) as e:
        # If it's not valid JSON, return the string representation
        return str(value)
