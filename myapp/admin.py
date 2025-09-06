from django.contrib import admin
from .models import Contact, Child, Payment

# Contact Admin
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('submitted_at',)

# Child Admin
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name',)
    list_filter = ()

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'child', 'amount', 'payment_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'user__username', 'child__name')
    readonly_fields = ()  # कोई भी field readonly नहीं, सब editable
    ordering = ('-created_at',)  # latest payments पहले दिखें

# Register models with admin
admin.site.register(Contact, ContactAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Payment, PaymentAdmin)
