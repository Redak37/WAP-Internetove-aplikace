from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from pekarnaApp.models import Car, Resource, Order


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'first_name', 'last_name', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': ''})


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'first_name', 'last_name', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': ''})


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ('driver', 'title', 'spz', 'capacity',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ('title', 'price', 'stock', 'allergens',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'deliver_date', 'notes',)
        help_texts = {'deliver_date': 'Formát DD.MM.RRRR'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
