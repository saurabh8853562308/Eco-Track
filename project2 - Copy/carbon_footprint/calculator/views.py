from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
import json


# Authentication Forms
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='At least 8 characters, mix of letters and numbers recommended'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if len(password2) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    ROLE_CHOICES = [
        ('customer', 'Customer - Track my carbon footprint'),
        ('company_member', 'Company Member - View platform data'),
    ]
    
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    role = forms.ChoiceField(
        label='Login As',
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        initial='customer'
    )


# Carbon emission factors (kg CO2e per unit)
CARBON_FACTORS = {
    'food': {
        'beef': 27.0,  # kg CO2e per kg
        'chicken': 6.9,  # kg CO2e per kg
        'fish': 5.0,  # kg CO2e per kg
        'vegetable': 2.0,  # kg CO2e per kg
    },
    'energy': {
        'electricity': 0.92,  # kg CO2e per kWh (average grid)
        'natural_gas': 2.04,  # kg CO2e per cubic meter
    },
    'transport': {
        'car': 0.411,  # kg CO2e per mile (average car)
        'public_transport': 0.089,  # kg CO2e per mile
    }
}


def index(request):
    """Render the main home page."""
    return render(request, 'home.html')


def home_view(request):
    """Render the home page."""
    return render(request, 'home.html')


def calculator_view(request):
    """Render the calculator page - requires login."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign up or login to access the calculator.')
        return redirect('calculator:signup')
    return render(request, 'calculator.html', {
        'carbon_factors': CARBON_FACTORS
    })


def tips_view(request):
    """Render the tips page - requires login."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign up or login to view sustainability tips.')
        return redirect('calculator:signup')
    return render(request, 'tips.html')


def about_view(request):
    """Render the about page - requires login."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign up or login to learn more about us.')
        return redirect('calculator:signup')
    return render(request, 'about.html')


@require_http_methods(["POST"])
def calculate_footprint(request):
    """Calculate carbon footprint based on user input."""
    try:
        data = json.loads(request.body)
        
        # Food carbon calculation
        food_carbon = 0
        food_carbon += data.get('beef', 0) * CARBON_FACTORS['food']['beef']
        food_carbon += data.get('chicken', 0) * CARBON_FACTORS['food']['chicken']
        food_carbon += data.get('fish', 0) * CARBON_FACTORS['food']['fish']
        food_carbon += data.get('vegetable', 0) * CARBON_FACTORS['food']['vegetable']
        
        # Energy carbon calculation
        energy_carbon = 0
        energy_carbon += data.get('electricity', 0) * CARBON_FACTORS['energy']['electricity']
        energy_carbon += data.get('natural_gas', 0) * CARBON_FACTORS['energy']['natural_gas']
        
        # Transport carbon calculation
        transport_carbon = 0
        transport_carbon += data.get('car_miles', 0) * CARBON_FACTORS['transport']['car']
        transport_carbon += data.get('public_transport_miles', 0) * CARBON_FACTORS['transport']['public_transport']
        
        total_carbon = food_carbon + energy_carbon + transport_carbon
        
        # Save to database if user is authenticated
        if request.user.is_authenticated:
            from .models import CarbonFootprint
            CarbonFootprint.objects.create(
                user=request.user,
                beef_consumption=data.get('beef', 0),
                chicken_consumption=data.get('chicken', 0),
                fish_consumption=data.get('fish', 0),
                vegetable_consumption=data.get('vegetable', 0),
                electricity_usage=data.get('electricity', 0),
                natural_gas_usage=data.get('natural_gas', 0),
                car_miles=data.get('car_miles', 0),
                public_transport_miles=data.get('public_transport_miles', 0),
                total_food_carbon=round(food_carbon, 2),
                total_energy_carbon=round(energy_carbon, 2),
                total_carbon=round(total_carbon, 2)
            )
        
        return JsonResponse({
            'status': 'success',
            'food_carbon': round(food_carbon, 2),
            'energy_carbon': round(energy_carbon, 2),
            'transport_carbon': round(transport_carbon, 2),
            'total_carbon': round(total_carbon, 2),
            'monthly_carbon': round(total_carbon, 2),
            'annual_carbon': round(total_carbon * 12, 2),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


def login_view(request):
    """Handle user login with role selection."""
    if request.user.is_authenticated:
        return redirect('calculator:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            selected_role = form.cleaned_data['role']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user's profile role matches selected role
                try:
                    user_profile = user.profile
                    if user_profile.role != selected_role:
                        messages.error(request, f'❌ This account is registered as a {user_profile.get_role_display()}. Please select the correct login role.')
                        return render(request, 'login.html', {'form': form})
                except:
                    # If profile doesn't exist, create one with the selected role
                    from .models import UserProfile
                    profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': selected_role})
                    
                    # If profile exists but role doesn't match
                    if not created and profile.role != selected_role:
                        messages.error(request, f'❌ This account is registered as a {profile.get_role_display()}. Please select the correct login role.')
                        return render(request, 'login.html', {'form': form})
                
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect based on role
                if selected_role == 'company_member':
                    return redirect('calculator:company_dashboard')
                else:
                    return redirect('calculator:index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('calculator:index')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        phone_number = request.POST.get('phone', '').strip()
        country_code = request.POST.get('country_code', '').strip()
        
        # Validate phone number format based on country code
        if phone_number and country_code:
            # Country code to expected digit count mapping
            country_digit_map = {
                '+1': (10, 'USA/Canada'),           # 10 digits
                '+44': (10, 'UK'),                   # 10 digits
                '+91': (10, 'India'),                # 10 digits
                '+86': (11, 'China'),                # 11 digits
                '+81': (10, 'Japan'),                # 10 digits
                '+33': (9, 'France'),                # 9 digits
                '+49': (10, 'Germany'),              # 10 digits
                '+39': (10, 'Italy'),                # 10 digits
                '+34': (9, 'Spain'),                 # 9 digits
                '+31': (9, 'Netherlands'),           # 9 digits
                '+41': (9, 'Switzerland'),           # 9 digits
                '+43': (10, 'Austria'),              # 10 digits
                '+47': (8, 'Norway'),                # 8 digits
                '+46': (9, 'Sweden'),                # 9 digits
                '+45': (8, 'Denmark'),               # 8 digits
                '+358': (10, 'Finland'),             # 10 digits
                '+61': (9, 'Australia'),             # 9 digits
                '+64': (10, 'New Zealand'),          # 10 digits
                '+55': (11, 'Brazil'),               # 11 digits
                '+27': (9, 'South Africa'),          # 9 digits
                '+234': (10, 'Nigeria'),             # 10 digits
                '+966': (9, 'Saudi Arabia'),         # 9 digits
                '+971': (9, 'UAE'),                  # 9 digits
                '+65': (8, 'Singapore'),             # 8 digits
                '+60': (9, 'Malaysia'),              # 9 digits
                '+66': (9, 'Thailand'),              # 9 digits
                '+62': (10, 'Indonesia'),            # 10 digits
                '+82': (10, 'South Korea'),          # 10 digits
                '+84': (9, 'Vietnam'),               # 9 digits
            }
            
            # Extract only digits from phone number
            digits_only = ''.join(filter(str.isdigit, phone_number))
            
            if country_code in country_digit_map:
                expected_digits, country_name = country_digit_map[country_code]
                if len(digits_only) != expected_digits:
                    messages.error(
                        request, 
                        f'Invalid phone number for {country_name}. Expected {expected_digits} digits, got {len(digits_only)}.'
                    )
                    return render(request, 'signup.html', {'form': form})
        
        if form.is_valid():
            user = form.save()
            
            # Combine country code with phone number and save to user profile
            if phone_number:
                full_phone = f"{country_code} {phone_number}" if country_code else phone_number
                from .models import UserProfile
                UserProfile.objects.create(user=user, phone_number=full_phone)
            
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to the Carbon Footprint Calculator!')
            return redirect('calculator:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('calculator:index')


def community_comparison_view(request):
    """Show user's carbon footprint ranking compared to other users."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign up or login to view community comparison.')
        return redirect('calculator:signup')
    
    from django.db.models import Avg, Q
    
    # Get all users with carbon footprints
    user_stats = []
    all_users = User.objects.filter(carbon_footprints__isnull=False).distinct()
    
    for user in all_users:
        footprints = user.carbon_footprints.all()
        if footprints.exists():
            avg_carbon = footprints.aggregate(Avg('total_carbon'))['total_carbon__avg'] or 0
            latest_carbon = footprints.first()
            
            user_stats.append({
                'user': user,
                'avg_carbon': round(avg_carbon, 2),
                'latest_carbon': round(latest_carbon.total_carbon, 2) if latest_carbon else 0,
                'footprint_count': footprints.count()
            })
    
    # Create two separate sorted lists
    # 1. user_stats_by_carbon: sorted by average carbon (lower is better)
    user_stats_by_carbon = sorted(user_stats, key=lambda x: x['avg_carbon'])
    
    # 2. user_stats_by_registration: sorted by user registration order (date_joined/ID)
    user_stats_by_registration = sorted(user_stats, key=lambda x: x['user'].id)
    
    # Find current user's ranking (by carbon footprint)
    current_user_rank = None
    current_user_stats = None
    for idx, stats in enumerate(user_stats_by_carbon):
        if stats['user'] == request.user:
            current_user_rank = idx + 1
            current_user_stats = stats
            break
    
    # Get community stats
    total_users = all_users.count()
    average_community_carbon = sum(s['avg_carbon'] for s in user_stats) / len(user_stats) if user_stats else 0
    lowest_carbon_user = user_stats_by_carbon[0] if user_stats_by_carbon else None
    highest_carbon_user = user_stats_by_carbon[-1] if user_stats_by_carbon else None
    
    # Prepare top 10 users (by lowest carbon footprint)
    top_users = user_stats_by_carbon[:10]
    
    context = {
        'current_user_rank': current_user_rank,
        'current_user_stats': current_user_stats,
        'total_users': total_users,
        'average_community_carbon': round(average_community_carbon, 2),
        'lowest_carbon_user': lowest_carbon_user,
        'highest_carbon_user': highest_carbon_user,
        'top_users': top_users,
        'all_user_stats': user_stats_by_registration
    }
    
    return render(request, 'community_comparison.html', context)


def report_issue_view(request):
    """Handle issue reporting from users."""
    if request.method == 'POST':
        from .models import IssueReport
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        issue_type = request.POST.get('issue_type', '').strip()
        page = request.POST.get('page', '').strip()
        subject = request.POST.get('subject', '').strip()
        description = request.POST.get('description', '').strip()
        follow_up = request.POST.get('follow_up') == 'on'
        
        # Validation
        if not all([name, email, issue_type, page, subject, description]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'report_issue.html')
        
        try:
            # Create issue report
            IssueReport.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                issue_type=issue_type,
                page=page,
                subject=subject,
                description=description,
                follow_up=follow_up
            )
            
            messages.success(request, '✅ Thank you for reporting this issue! We\'ll look into it soon. You\'ll receive an email at {} if we need more information.'.format(email))
            return render(request, 'report_issue.html')
        except Exception as e:
            messages.error(request, f'An error occurred while submitting your report: {str(e)}')
            return render(request, 'report_issue.html')
    
    return render(request, 'report_issue.html')


def company_dashboard_view(request):
    """Company member dashboard with backend and user analytics."""
    # Check if user is a company member
    try:
        if request.user.profile.role != 'company_member':
            messages.error(request, 'You do not have access to the company dashboard.')
            return redirect('calculator:index')
    except:
        messages.error(request, 'User profile not found. Access denied.')
        return redirect('calculator:index')
    
    from django.db.models import Avg, Count, Q
    from django.utils import timezone
    from datetime import timedelta
    
    # Get all users with their profiles
    all_users = User.objects.select_related('profile').all()
    
    # User statistics
    total_users = all_users.count()
    
    # Get users with carbon footprints (active users)
    active_users = User.objects.filter(carbon_footprints__isnull=False).distinct().count()
    
    # Get total calculations
    from .models import CarbonFootprint
    total_calculations = CarbonFootprint.objects.count()
    
    # Calculate average carbon footprint
    avg_carbon_obj = CarbonFootprint.objects.aggregate(Avg('total_carbon'))
    average_carbon = avg_carbon_obj['total_carbon__avg'] or 0
    
    # Build user data list
    users_data = []
    for user in all_users:
        try:
            profile = user.profile
        except:
            from .models import UserProfile
            profile = UserProfile.objects.create(user=user)
        
        # Get user's carbon footprints
        footprints = user.carbon_footprints.all()
        calculation_count = footprints.count()
        avg_carbon = footprints.aggregate(Avg('total_carbon'))['total_carbon__avg'] or 0
        
        users_data.append({
            'user': user,
            'profile': profile,
            'phone_number': profile.phone_number,
            'role': profile.role,
            'get_role_display': profile.get_role_display(),
            'calculation_count': calculation_count,
            'avg_carbon': avg_carbon,
            'last_login': user.last_login,
        })
    
    # Analytics - Carbon distribution
    very_low = CarbonFootprint.objects.filter(total_carbon__lt=100).count()
    low = CarbonFootprint.objects.filter(total_carbon__gte=100, total_carbon__lt=200).count()
    medium = CarbonFootprint.objects.filter(total_carbon__gte=200, total_carbon__lt=300).count()
    high = CarbonFootprint.objects.filter(total_carbon__gte=300).count()
    
    total_carbon_records = very_low + low + medium + high
    
    if total_carbon_records > 0:
        very_low_percent = (very_low / total_carbon_records) * 100
        low_percent = (low / total_carbon_records) * 100
        medium_percent = (medium / total_carbon_records) * 100
        high_percent = (high / total_carbon_records) * 100
    else:
        very_low_percent = low_percent = medium_percent = high_percent = 0
    
    # Registration trends
    now = timezone.now()
    this_week_start = now - timedelta(days=now.weekday())
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    this_week_users = User.objects.filter(date_joined__gte=this_week_start).count()
    this_month_users = User.objects.filter(date_joined__gte=this_month_start).count()
    
    # Active users in last 30 days
    last_30_days = now - timedelta(days=30)
    active_last_30_days = User.objects.filter(last_login__gte=last_30_days).count()
    
    # Average calculations per user
    avg_calculations_per_user = total_calculations / total_users if total_users > 0 else 0
    
    # Get issue reports
    from .models import IssueReport
    issue_reports = IssueReport.objects.select_related('user').order_by('-created_at')[:20]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_calculations': total_calculations,
        'average_carbon': average_carbon,
        'users': users_data,
        'very_low_count': very_low,
        'low_count': low,
        'medium_count': medium,
        'high_count': high,
        'very_low_percent': very_low_percent,
        'low_percent': low_percent,
        'medium_percent': medium_percent,
        'high_percent': high_percent,
        'this_week_users': this_week_users,
        'this_month_users': this_month_users,
        'active_last_30_days': active_last_30_days,
        'avg_calculations_per_user': avg_calculations_per_user,
        'issue_reports': issue_reports,
    }
    
    return render(request, 'company_dashboard.html', context)


def is_company_member(user):
    """Check if user is a company member."""
    try:
        return user.profile.role == 'company_member'
    except:
        return False