from django.contrib import admin
from TestModel.models import Test
from TestModel.models import Publisher,Author,Book

# Register your models here.
admin.site.register(Test)
class BookInline(admin.TabularInline):
    model = Book
class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookInline] 
    list_display = ('name','address', 'city')
    search_fields = ('name',)
    fieldsets = (
        ['Main',{
            'fields':('name','address'),
        }],
        ['Advance',{
            'classes': ('collapse',), 
            'fields': ('city',),
        }]
    )
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author)
admin.site.register(Book)