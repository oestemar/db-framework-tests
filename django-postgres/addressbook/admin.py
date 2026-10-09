from django.contrib import admin
from .models import AddressBook

#admin.site.register(AddressBook)
@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "kana",
        "age",
        "gender",
        "email"
    )

    search_fields = (
        "name",
        "kana",
        "email"
        )
        
    list_filter = (
        "gender",
        "blood_type"
    )