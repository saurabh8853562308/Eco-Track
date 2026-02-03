#!/usr/bin/env python
"""
Script to setup test users for the dual-dashboard system
Run with: python manage.py shell < setup_test_users.py
Or copy-paste the contents into: python manage.py shell
"""

from django.contrib.auth.models import User
from calculator.models import UserProfile

# ============================================================
# CREATE TEST USERS
# ============================================================

print("=" * 60)
print("Setting up test users for dual-dashboard system")
print("=" * 60)

# Test Customer User
print("\n1. Creating customer test user...")
customer_user, created = User.objects.get_or_create(
    username='customer_demo',
    defaults={
        'email': 'customer@example.com',
        'first_name': 'John',
        'last_name': 'Customer',
    }
)

if created:
    customer_user.set_password('customer123')
    customer_user.save()
    print("   ✓ Customer user created")
else:
    print("   ℹ Customer user already exists")

# Ensure customer has correct role
customer_profile, _ = UserProfile.objects.get_or_create(user=customer_user)
customer_profile.role = 'customer'
customer_profile.phone_number = '+1-555-0001'
customer_profile.save()
print(f"   ✓ Profile set: Role = {customer_profile.get_role_display()}")

# ============================================================

# Test Company Member User
print("\n2. Creating company member test user...")
company_user, created = User.objects.get_or_create(
    username='company_admin',
    defaults={
        'email': 'admin@company.com',
        'first_name': 'Jane',
        'last_name': 'Admin',
    }
)

if created:
    company_user.set_password('company123')
    company_user.save()
    print("   ✓ Company member user created")
else:
    print("   ℹ Company member user already exists")

# Ensure company member has correct role
company_profile, _ = UserProfile.objects.get_or_create(user=company_user)
company_profile.role = 'company_member'
company_profile.company_name = 'EcoTrack Inc.'
company_profile.phone_number = '+1-555-0002'
company_profile.save()
print(f"   ✓ Profile set: Role = {company_profile.get_role_display()}")
print(f"   ✓ Company Name: {company_profile.company_name}")

# ============================================================

# Display test credentials
print("\n" + "=" * 60)
print("TEST CREDENTIALS")
print("=" * 60)

print("\n📱 CUSTOMER LOGIN:")
print("   Username: customer_demo")
print("   Password: customer123")
print("   Select:  Customer - Track my carbon footprint")
print("   Dashboard: Home page with calculator")

print("\n🏢 COMPANY MEMBER LOGIN:")
print("   Username: company_admin")
print("   Password: company123")
print("   Select:  Company Member - View platform data")
print("   Dashboard: Analytics and user management")

print("\n" + "=" * 60)
print("✅ Test users setup complete!")
print("=" * 60)

# ============================================================
# OPTIONAL: Create sample carbon footprints
# ============================================================

try:
    from calculator.models import CarbonFootprint
    
    # Check if customer already has footprints
    if not customer_user.carbon_footprints.exists():
        print("\n3. Creating sample carbon footprints for customer...")
        
        # Create 3 sample footprints
        for i in range(1, 4):
            CarbonFootprint.objects.create(
                user=customer_user,
                beef_consumption=2.5 + (i * 0.5),
                chicken_consumption=1.0 + (i * 0.2),
                fish_consumption=0.8 + (i * 0.1),
                vegetable_consumption=3.0 + (i * 0.3),
                electricity_usage=150 + (i * 20),
                natural_gas_usage=20 + (i * 2),
                car_miles=100 + (i * 15),
                public_transport_miles=50 + (i * 10),
                total_food_carbon=round(9.2 + (i * 1.5), 2),
                total_energy_carbon=round(330 + (i * 40), 2),
                total_carbon=round(481.2 + (i * 100), 2)
            )
            print(f"   ✓ Sample {i} created: {481.2 + (i * 100):.1f} kg CO2e")
        
        print("   ℹ Customer now has data for analytics comparison")
    else:
        print("\n3. Customer already has carbon footprints")
        
except Exception as e:
    print(f"\n⚠ Note: Could not create sample data: {e}")

print("\n" + "=" * 60)
print("Ready to test! Go to: http://localhost:8000/calculator/login/")
print("=" * 60)
