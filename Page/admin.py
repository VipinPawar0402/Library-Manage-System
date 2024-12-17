from django.contrib import admin
from .models import Person

# Admin customization for the Person model
class PersonAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Person model in the Django admin interface.
    """
    list_display = ['id', 'name', 'email', 'mobile']

# Register the Person model with the customized admin class
admin.site.register(Person, PersonAdmin)
