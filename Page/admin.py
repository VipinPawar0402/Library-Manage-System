
from django.contrib import admin
from .models import BookReturned, IssueBook, Person, Category, Book, Stuff

# Admin customization for the Person model
class PersonAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Person model in the Django admin interface.
    """
    list_display = ['id', 'name', 'email', 'mobile']

class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Category model in the Django admin interface.
    """
    list_display = ['id', 'subject']

class BookAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Book model in the Django admin interface.
    """
    list_display = ['id', 'title', 'author', 'category', 'price', 'date_added']

class StuffAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Stuff model in the Django admin interface.
    """
    list_display = ['id', 'name', 'email', 'mobile', 'crn', 'password']

class IssueBookAdmin(admin.ModelAdmin):
    """
    Customizes the display of the IssueBook model in the Django admin interface.
    """
    list_display = ['id','student', 'book', 'charges',  'issue_date', 'end_date', 'issue_time', 'staff', 'typeOf_issue']


# Register the models with the customized admin classes
admin.site.register(Person, PersonAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Stuff, StuffAdmin)
admin.site.register(IssueBook, IssueBookAdmin)
admin.site.register(BookReturned)