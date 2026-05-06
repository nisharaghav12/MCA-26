from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication APIs
    path('api/auth/login/', views.login_api, name='login'),
    path('api/auth/register/', views.register_api, name='register'),
    path('api/auth/logout/', views.logout_api, name='logout'),
    path('api/auth/status/', views.check_user_status, name='user-status'),
    
    # Main APIs
    path('api/market-research/', views.market_research_api, name='market-research'),
    path('api/swot/generate/', views.generate_swot_api, name='generate-swot'),
    path('api/swot/feasibility/', views.generate_feasibility_api, name='feasibility'),
    path('api/swot/save/', views.save_swot_api, name='save-swot'),
    path('api/swot/history/', views.swot_history_api, name='swot-history'),
    path('api/swot/detail/<int:analysis_id>/', views.swot_detail_api, name='swot-detail'),
    
    # Premium APIs
    path('api/premium/info/', views.premium_info_api, name='premium-info'),
    path('api/premium/activate/', views.activate_premium_api, name='activate-premium'),
]
