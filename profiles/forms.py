from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels without setting autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user's name and email.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes to user fields
        and set autofocus only on the first_name field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
        }

        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = placeholders[field]
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False

        # Set autofocus only on the first_name field
        self.fields["first_name"].widget.attrs["autofocus"] = True
