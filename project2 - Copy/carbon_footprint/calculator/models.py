from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('company_member', 'Company Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', help_text="User role")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="User's phone number")
    company_name = models.CharField(max_length=200, blank=True, null=True, help_text="Company name for company members")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile - {self.user.username} ({self.get_role_display()})"


class CarbonFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carbon_footprints', null=True, blank=True)
    
    # Food carbon footprint
    beef_consumption = models.FloatField(default=0, help_text="kg per month")
    chicken_consumption = models.FloatField(default=0, help_text="kg per month")
    fish_consumption = models.FloatField(default=0, help_text="kg per month")
    vegetable_consumption = models.FloatField(default=0, help_text="kg per month")
    
    # Energy consumption
    natural_gas_usage = models.FloatField(default=0, help_text="cubic meters per month")
    electricity_usage = models.FloatField(default=0, help_text="kWh per month")
    
    # Transport (optional)
    car_miles = models.FloatField(default=0, help_text="miles per month")
    public_transport_miles = models.FloatField(default=0, help_text="miles per month")
    
    # Calculations
    total_food_carbon = models.FloatField(default=0, help_text="kg CO2e per month")
    total_energy_carbon = models.FloatField(default=0, help_text="kg CO2e per month")
    total_carbon = models.FloatField(default=0, help_text="kg CO2e per month")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    
    def __str__(self):
        return f"Carbon Footprint - {self.created_at.strftime('%Y-%m-%d')}"


class IssueReport(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('performance', 'Performance Issue'),
        ('ui', 'UI/UX Issue'),
        ('calculation', 'Calculation Error'),
        ('other', 'Other'),
    ]
    
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('calculator', 'Calculator'),
        ('tips', 'Tips Page'),
        ('about', 'About Page'),
        ('comparison', 'Community Comparison'),
        ('login', 'Login/Signup'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_reports')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    page = models.CharField(max_length=20, choices=PAGE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    follow_up = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='open', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.issue_type}"