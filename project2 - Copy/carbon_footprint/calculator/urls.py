from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home_view, name='home'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('tips/', views.tips_view, name='tips'),
    path('about/', views.about_view, name='about'),
    path('comparison/', views.community_comparison_view, name='comparison'),
    path('report-issue/', views.report_issue_view, name='report_issue'),
    path('api/calculate/', views.calculate_footprint, name='calculate'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('company-dashboard/', views.company_dashboard_view, name='company_dashboard'),
]
