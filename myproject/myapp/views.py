from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# Import our services
from .services import marketplace_service
from .swot_engine import swot_engine
from .models import SWOTAnalysis, UserProfile
import json
import random


def home(request):
    """Main homepage view"""
    user = request.user
    user_data = None
    
    if user.is_authenticated:
        try:
            profile = user.profile
            user_data = {
                'is_premium': profile.is_premium,
                'remaining_uses': profile.remaining_free_uses,
                'usage_count': profile.usage_count,
                'FREE_USAGE_LIMIT': profile.FREE_USAGE_LIMIT
            }
        except UserProfile.DoesNotExist:
            # Create profile for existing users
            profile = UserProfile.objects.create(user=user)
            user_data = {
                'is_premium': False,
                'remaining_uses': profile.FREE_USAGE_LIMIT,
                'usage_count': 0,
                'FREE_USAGE_LIMIT': profile.FREE_USAGE_LIMIT
            }
    
    return render(request, "index.html", {'user_data': user_data, 'user': user})


@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    """User login API"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        # Get user profile data
        try:
            profile = user.profile
            return JsonResponse({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'username': user.username,
                    'is_premium': profile.is_premium,
                    'remaining_uses': profile.remaining_free_uses
                }
            })
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
            return JsonResponse({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'username': user.username,
                    'is_premium': False,
                    'remaining_uses': 5
                }
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def register_api(request):
    """User registration API"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not password:
        return JsonResponse({'success': False, 'message': 'Username and password required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)
    
    if email and User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Email already exists'}, status=400)
    
    user = User.objects.create_user(username=username, email=email or '', password=password)
    UserProfile.objects.create(user=user)
    
    login(request, user)
    return JsonResponse({
        'success': True, 
        'message': 'Registration successful',
        'user': {
            'username': username,
            'is_premium': False,
            'remaining_uses': 5
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def logout_api(request):
    """User logout API"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})


@require_http_methods(["GET"])
def check_user_status(request):
    """Check user status and usage"""
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False})
    
    user = request.user
    try:
        profile = user.profile
        return JsonResponse({
            'authenticated': True,
            'username': user.username,
            'email': user.email,
            'is_premium': profile.is_premium,
            'remaining_uses': profile.remaining_free_uses,
            'usage_count': profile.usage_count,
            'FREE_USAGE_LIMIT': profile.FREE_USAGE_LIMIT
        })
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        return JsonResponse({
            'authenticated': True,
            'username': user.username,
            'email': user.email,
            'is_premium': False,
            'remaining_uses': 5,
            'usage_count': 0,
            'FREE_USAGE_LIMIT': 5
        })


@csrf_exempt
@require_http_methods(["GET"])
def market_research_api(request):
    """API endpoint for market research data"""
    query = request.GET.get('q', request.GET.get('query', ''))
    
    if not query:
        return JsonResponse({'error': 'Query parameter required'}, status=400)
    
    market_data = marketplace_service.get_market_data(query)
    
    return JsonResponse({
        'success': True,
        'data': market_data
    })


@csrf_exempt
@require_http_methods(["POST"])
def generate_swot_api(request):
    """API endpoint for generating SWOT analysis"""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    
    idea = body.get('idea', '').strip()
    is_detailed = body.get('detailed', False)
    
    if not idea:
        return JsonResponse({'error': 'Idea is required'}, status=400)
    
    # Check user limits (if authenticated)
    user = request.user
    if user.is_authenticated:
        try:
            profile = user.profile
            if not profile.can_use_free and not profile.is_premium:
                return JsonResponse({
                    'success': False,
                    'premium_required': True,
                    'message': 'Free usage limit reached. Upgrade to Premium for unlimited access!',
                    'price': UserProfile.PREMIUM_PRICE,
                    'features': [
                        'Unlimited SWOT analyses',
                        'Detailed feasibility reports',
                        'AI-powered insights',
                        'Export PDF reports'
                    ]
                }, status=403)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
    
    # Get market data
    market_data = marketplace_service.get_market_data(idea)
    
    # Generate SWOT
    swot = swot_engine.generate_swot(idea, market_data)
    
    # Generate detailed report if requested
    detailed_report = None
    if is_detailed:
        detailed_report = swot_engine.generate_detailed_report(idea, market_data)
    
    result = {
        'success': True,
        'swot': swot,
        'market_data': market_data,
        'idea': idea,
        'is_detailed': is_detailed
    }
    
    if detailed_report:
        result['detailed_report'] = detailed_report
    
    # Update user usage
    if user.is_authenticated:
        try:
            profile = user.profile
            profile.increment_usage()
        except UserProfile.DoesNotExist:
            pass
    
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def generate_feasibility_api(request):
    """API endpoint for generating feasibility report"""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    
    idea = body.get('idea', '').strip()
    
    if not idea:
        return JsonResponse({'error': 'Idea is required'}, status=400)
    
    # Check premium status
    user = request.user
    is_premium = False
    
    if user.is_authenticated:
        try:
            profile = user.profile
            is_premium = profile.is_premium
            if not profile.can_use_free and not profile.is_premium:
                return JsonResponse({
                    'success': False,
                    'premium_required': True,
                    'message': 'Feasibility reports require Premium subscription',
                    'price': UserProfile.PREMIUM_PRICE
                }, status=403)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
    
    # Get market data
    market_data = marketplace_service.get_market_data(idea)
    
    # Generate feasibility report
    feasibility = swot_engine.generate_feasibility_report(idea, market_data)
    
    # Update usage
    if user.is_authenticated:
        try:
            profile = user.profile
            profile.increment_usage()
        except UserProfile.DoesNotExist:
            pass
    
    return JsonResponse({
        'success': True,
        'feasibility': feasibility,
        'market_data': market_data,
        'is_premium': is_premium
    })


@csrf_exempt
@require_http_methods(["POST"])
def save_swot_api(request):
    """API endpoint for saving SWOT analysis"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    
    idea = body.get('idea', '').strip()
    swot = body.get('swot', {})
    market_data = body.get('market_data')
    feasibility = body.get('feasibility')
    
    if not idea:
        return JsonResponse({'error': 'Idea is required'}, status=400)
    
    # Save to database
    analysis = SWOTAnalysis.objects.create(
        user=request.user,
        idea=idea,
        strength=swot.get('strengths', []),
        weakness=swot.get('weaknesses', []),
        opportunity=swot.get('opportunities', []),
        threat=swot.get('threats', []),
        market_data=market_data,
        feasibility_report=feasibility,
        is_detailed=body.get('is_detailed', False)
    )
    
    return JsonResponse({
        'success': True,
        'id': analysis.id,
        'message': 'SWOT analysis saved successfully'
    })


@require_http_methods(["GET"])
def swot_history_api(request):
    """API endpoint for getting SWOT history"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    limit = int(request.GET.get('limit', 10))
    
    analyses = SWOTAnalysis.objects.filter(user=request.user)[:limit]
    
    history = []
    for a in analyses:
        history.append({
            'id': a.id,
            'idea': a.idea,
            'strengths': a.strength,
            'weaknesses': a.weakness,
            'opportunities': a.opportunity,
            'threats': a.threat,
            'created_at': a.created_at.isoformat(),
            'is_detailed': a.is_detailed
        })
    
    return JsonResponse({
        'success': True,
        'count': len(history),
        'history': history
    })


@require_http_methods(["GET"])
def swot_detail_api(request, analysis_id):
    """API endpoint for getting a specific SWOT analysis"""
    try:
        analysis = SWOTAnalysis.objects.get(id=analysis_id)
    except SWOTAnalysis.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status=404)
    
    return JsonResponse({
        'success': True,
        'analysis': {
            'id': analysis.id,
            'idea': analysis.idea,
            'strengths': analysis.strength,
            'weaknesses': analysis.weakness,
            'opportunities': analysis.opportunity,
            'threats': analysis.threat,
            'market_data': analysis.market_data,
            'feasibility_report': analysis.feasibility_report,
            'created_at': analysis.created_at.isoformat()
        }
    })


@require_http_methods(["GET"])
def premium_info_api(request):
    """Get premium information"""
    return JsonResponse({
        'success': True,
        'price': UserProfile.PREMIUM_PRICE,
        'currency': 'INR',
        'currency_symbol': '₹',
        'billing_cycle': 'monthly',
        'features': [
            {'name': 'Unlimited SWOT Analyses', 'description': 'Generate as many analyses as you need'},
            {'name': 'Detailed Feasibility Reports', 'description': 'Comprehensive business feasibility analysis'},
            {'name': 'AI-Powered Insights', 'description': 'Advanced AI-driven market insights'},
            {'name': 'Export PDF Reports', 'description': 'Download professional PDF reports'},
            {'name': 'Priority Support', 'description': 'Get faster responses to your queries'},
            {'name': 'No Advertisements', 'description': 'Clean, ad-free experience'}
        ],
        'cta': 'Upgrade to Premium',
        'note': '₹350/month - Cancel anytime'
    })


@csrf_exempt
@require_http_methods(["POST"])
def activate_premium_api(request):
    """Activate premium (mock payment for demo)"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
    # In production, integrate with payment gateway
    payment_method = data.get('payment_method', 'demo')
    
    # Activate premium (mock)
    try:
        profile = request.user.profile
        profile.activate_premium(months=1)
        return JsonResponse({
            'success': True,
            'message': 'Premium activated successfully!',
            'premium_details': {
                'is_premium': True,
                'expiry_date': profile.premium_expiry_date.isoformat()
            }
        })
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        profile.activate_premium(months=1)
        return JsonResponse({
            'success': True,
            'message': 'Premium activated successfully!',
            'premium_details': {
                'is_premium': True,
                'expiry_date': profile.premium_expiry_date.isoformat()
            }
        })
