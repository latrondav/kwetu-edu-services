from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Profile)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'contact_email',)
    ordering = ('contact_name',)
    search_fields = ('contact_name', 'contact_email',)

admin.site.register(Testimonial)
admin.site.register(Service)
admin.site.register(Event)
