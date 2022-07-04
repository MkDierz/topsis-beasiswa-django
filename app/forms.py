from django import forms
from app.models import Data
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.add_input(Submit("submit", "Submit"))
