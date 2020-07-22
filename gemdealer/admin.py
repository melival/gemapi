from django.contrib import admin
from .models import Deals

# Register your models here.


class DealsAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'total', 'quantity', 'date')
    list_display_links = ('id', 'customer')
    search_fields = ('id', 'customer', 'item')
    list_filter = ('customer', 'item')


admin.site.register(Deals, DealsAdmin)
