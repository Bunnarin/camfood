from django import forms
from django.forms.models import modelform_factory

def get_default_form(flat_fields, model):
    """
    This exists because the easier option (modelform_factory attach its field validation to the text area and I don't want that)
    """
    class DefaultImportForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # create the flat fields
            for field in flat_fields:
                self.fields[field] = forms.CharField(
                    required=False, widget=forms.Textarea
                    )

            # check if the model field not in flat field, then we use the model-form's
            model_form = modelform_factory(model, fields='__all__')()
            for field in model_form.fields:
                if field not in flat_fields:
                    self.fields[field] = model_form.fields[field]
    return DefaultImportForm
            
