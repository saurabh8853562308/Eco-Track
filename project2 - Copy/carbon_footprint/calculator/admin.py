from django.contrib import admin
from .models import CarbonFootprint, IssueReport, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CarbonFootprint)
class CarbonFootprintAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_carbon')
    readonly_fields = ('created_at', 'updated_at', 'total_food_carbon', 'total_energy_carbon', 'total_carbon')
    fieldsets = (
        ('Food Consumption', {
            'fields': ('beef_consumption', 'chicken_consumption', 'fish_consumption', 'vegetable_consumption', 'total_food_carbon')
        }),
        ('Energy Consumption', {
            'fields': ('electricity_usage', 'natural_gas_usage', 'total_energy_carbon')
        }),
        ('Transport', {
            'fields': ('car_miles', 'public_transport_miles')
        }),
        ('Results', {
            'fields': ('total_carbon',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('subject', 'issue_type', 'page', 'status', 'created_at', 'email')
    list_filter = ('issue_type', 'page', 'status', 'created_at')
    search_fields = ('subject', 'description', 'email', 'name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Report Information', {
            'fields': ('name', 'email', 'user')
        }),
        ('Issue Details', {
            'fields': ('issue_type', 'page', 'subject', 'description')
        }),
        ('Status', {
            'fields': ('status', 'follow_up')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
