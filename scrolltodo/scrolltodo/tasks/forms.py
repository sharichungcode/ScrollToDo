from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import ItemList, Item

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class ItemListForm(forms.ModelForm):
    class Meta:
        model = ItemList
        fields = ['name', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ItemForm(forms.ModelForm):
    new_list_name = forms.CharField(required=False, max_length=100, label='New List Name')

    class Meta:
        model = Item
        fields = ['title', 'description', 'deadline', 'item_list', 'new_list_name']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        item_list = cleaned_data.get('item_list')
        new_list_name = cleaned_data.get('new_list_name')

        if not item_list and not new_list_name:
            raise forms.ValidationError(
                "Please select an existing list or provide a new list name."
            )

        if new_list_name:
            item_list = ItemList.objects.create(name=new_list_name, user=self.request.user)
            cleaned_data['item_list'] = item_list

        return cleaned_data