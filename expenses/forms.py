from django import forms
from .models import Expense


class DateInput(forms.DateInput):
    input_type = 'date'


class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name', 'date', 'category', )
        widgets = {
            'date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['date'].required = False
        self.fields['category'].required = False
