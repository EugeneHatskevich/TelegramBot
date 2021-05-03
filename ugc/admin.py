from django.contrib import admin
from .models import Profile
from .forms import ProfileForm
from .models import Message
from .models import Product
from .models import ActiveMonitoring, PassiveMonitoring
from import_export.admin import ImportExportModelAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'product', 'created_at')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'external_id', 'product_url', 'product_name', 'old_price', 'current_price', 'average_price',
        'operator_price',
        'operator_message')
    search_fields = ('external_id__startswith',)


@admin.register(ActiveMonitoring)
class ActiveMonitoringAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_monitoring', 'profile', 'text', 'waiting_price', 'time_published')
    search_fields = ('id_monitoring',)


@admin.register(PassiveMonitoring)
class PassiveMonitoringAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'monitoring_percent')


# @admin.register(OperatorMessage)
# class OperatorMessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'monitoring', 'operator_price', 'operator_url')
#     autocomplete_fields = ('monitoring',)
#
#
# @admin.register(OperatorMessageWaiting)
# class OperatorMessageWaitingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'monitoring', 'operator_price', 'operator_url')
#     autocomplete_fields = ('monitoring',)

