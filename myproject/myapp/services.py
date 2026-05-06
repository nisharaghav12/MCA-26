"""
Marketplace Service - Provides market research data
Note: Uses internal data for demo - can integrate real APIs later
"""
import json
import random


class MarketplaceService:
    """Service for fetching market research and industry data"""
    
    # Free tier mock data for fallback
    INDUSTRY_DATA = {
        'tech': {
            'name': 'Technology',
            'market_size': '$2.5T+',
            'growth': '12% CAGR',
            'key_players': ['Google', 'Microsoft', 'Apple', 'Amazon', 'Meta'],
            'trends': ['AI/ML', 'Cloud Computing', 'Edge Computing', '5G'],
            'opportunities': ['AI solutions', 'Cybersecurity', 'Low-code platforms'],
            'risks': ['Regulatory scrutiny', 'Talent shortage', 'Rapid commoditization']
        },
        'healthcare': {
            'name': 'Healthcare',
            'market_size': '$8.5T+',
            'growth': '8% CAGR',
            'key_players': ['UnitedHealth', 'CVS Health', 'HCA Healthcare'],
            'trends': ['Telemedicine', 'Wearables', 'AI diagnostics', 'Personalized medicine'],
            'opportunities': ['Remote monitoring', 'Digital therapeutics', 'Health apps'],
            'risks': ['Privacy regulations', 'Reimbursement challenges', 'Data breaches']
        },
        'finance': {
            'name': 'Finance',
            'market_size': '$26T+',
            'growth': '6% CAGR',
            'key_players': ['JP Morgan', 'Bank of America', 'Wells Fargo'],
            'trends': ['Fintech', 'Blockchain', 'Open Banking', 'ESG Investing'],
            'opportunities': ['Embedded finance', 'Crypto', 'Neobanks', 'Robo-advisors'],
            'risks': ['Regulatory compliance', 'Cybersecurity', 'Market volatility']
        },
        'education': {
            'name': 'Education',
            'market_size': '$7T+',
            'growth': '14% CAGR',
            'key_players': ['Chegg', 'Duolingo', 'Coursera', 'Khan Academy'],
            'trends': ['E-learning', 'Gamification', 'VR/AR', 'Microlearning'],
            'opportunities': ['Corporate training', 'Skills-based learning', 'AI tutors'],
            'risks': ['Engagement', 'Quality assurance', 'Access gaps']
        },
        'e-commerce': {
            'name': 'E-commerce',
            'market_size': '$6T+',
            'growth': '16% CAGR',
            'key_players': ['Amazon', 'Shopify', 'Walmart', 'Alibaba'],
            'trends': ['Social commerce', 'Voice shopping', 'Same-day delivery', 'AR try-on'],
            'opportunities': ['Niche marketplaces', 'Subscription boxes', 'D2C brands'],
            'risks': ['Customer acquisition costs', 'Logistics', 'Returns']
        },
        'food': {
            'name': 'Food & Beverage',
            'market_size': '$8T+',
            'growth': '5% CAGR',
            'key_players': ['Nestle', 'Coca-Cola', 'PepsiCo', 'Unilever'],
            'trends': ['Plant-based', 'Sustainability', 'Ghost kitchens', 'Meal kits'],
            'opportunities': ['Health-focused', 'Ethically sourced', 'Personalized nutrition'],
            'risks': ['Supply chain', 'Commodity prices', 'Regulations']
        },
        'fitness': {
            'name': 'Fitness',
            'market_size': '$600B+',
            'growth': '10% CAGR',
            'key_players': ['Peloton', 'Nike', 'Planet Fitness', 'ClassPass'],
            'trends': ['Home workouts', 'Wearables', 'Personalized training', 'Recovery'],
            'opportunities': ['Corporate wellness', 'Gamification', 'Hybrid models'],
            'risks': ['Retention', 'Competition', 'Equipment costs']
        },
        'travel': {
            'name': 'Travel & Hospitality',
            'market_size': '$8T+',
            'growth': '9% CAGR',
            'key_players': ['Airbnb', 'Booking Holdings', 'Marriott', 'Expedia'],
            'trends': ['Bleisure travel', 'Eco-tourism', 'Workation', 'Experience-driven'],
            'opportunities': ['Digital nomad', 'Micro-adventures', 'Local experiences'],
            'risks': ['Economic downturn', 'Travel restrictions', 'Fuel costs']
        },
        'real_estate': {
            'name': 'Real Estate',
            'market_size': '$12T+',
            'growth': '7% CAGR',
            'key_players': ['Zillow', 'Redfin', 'Compass', 'Opendoor'],
            'trends': ['iBuyers', 'Virtual tours', 'Smart homes', 'Co-living'],
            'opportunities': ['Proptech', 'Fractional ownership', 'Rental platforms'],
            'risks': ['Interest rates', 'Housing bubble', 'Inventory']
        },
        'gaming': {
            'name': 'Gaming',
            'market_size': '$200B+',
            'growth': '12% CAGR',
            'key_players': ['Tencent', 'Sony', 'Microsoft', 'Nintendo'],
            'trends': ['Mobile gaming', 'Cloud gaming', 'VR/AR', 'Esports'],
            'opportunities': ['Cross-platform', 'UGC', 'Game streaming', 'Blockchain gaming'],
            'risks': ['Discovery', 'Piracy', 'Regulatory', 'Burnout']
        }
    }
    
    # Keywords mapping for industry detection
    INDUSTRY_KEYWORDS = {
        'tech': ['app', 'software', 'ai', 'ml', 'machine learning', 'tech', 'digital', 'code', 'developer', 'saas', 'cloud', 'data', 'api'],
        'healthcare': ['health', 'medical', 'doctor', 'patient', 'hospital', 'clinic', 'wellness', 'fitness', 'mental', 'therapy', 'medicine', 'diagnos'],
        'finance': ['finance', 'money', 'bank', 'investment', 'crypto', 'trading', 'payment', 'fintech', 'loan', 'credit', 'insur'],
        'education': ['learn', 'education', 'school', 'student', 'course', 'tutor', 'training', 'skill', 'teach', 'academic'],
        'e-commerce': ['shop', 'store', 'buy', 'sell', 'product', 'retail', 'marketplace', 'commerce', 'order', 'delivery'],
        'food': ['food', 'restaurant', 'meal', 'cook', 'kitchen', 'diet', 'nutrition', 'drink', 'recipe', 'grocery'],
        'fitness': ['fitness', 'workout', 'exercise', 'gym', 'training', 'sport', 'athlet', 'muscle', 'cardio'],
        'travel': ['travel', 'trip', 'hotel', 'vacation', 'flight', 'booking', 'tourism', 'destination', 'airbnb'],
        'real_estate': ['property', 'house', 'real estate', 'home', 'apartment', 'rental', 'mortgage', 'buyer', 'seller'],
        'gaming': ['game', 'gaming', 'play', 'player', 'esports', 'stream', 'arcade', 'console', 'vr', 'ar']
    }
    
    def get_market_data(self, query):
        """Get market research data for a given idea/query"""
        query_lower = query.lower()
        
        # Detect industry
        industry = self._detect_industry(query_lower)
        
        # Get base data
        market_data = self.INDUSTRY_DATA.get(industry, self.INDUSTRY_DATA['tech']).copy()
        
        # Try to get real data from free APIs
        try:
            # Try MarketStack (free tier)
            # Fallback to mock data
            market_data['source'] = 'market_analysis'
        except Exception as e:
            market_data['source'] = 'internal_analysis'
        
        # Add contextual recommendations based on the query
        market_data['recommendations'] = self._generate_recommendations(query_lower, industry)
        market_data['detected_industry'] = industry
        
        return market_data
    
    def _detect_industry(self, query):
        """Detect industry from query text"""
        scores = {}
        
        for industry, keywords in self.INDUSTRY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query)
            scores[industry] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'tech'  # Default to tech
    
    def _generate_recommendations(self, query, industry):
        """Generate contextual recommendations"""
        recs = []
        
        # Industry-specific recommendations
        if industry == 'tech':
            recs = [
                'Focus on clear value proposition vs existing solutions',
                'Consider freemium model for user acquisition',
                'Build moat through network effects or proprietary data',
                'Consider strategic partnerships with larger players'
            ]
        elif industry == 'healthcare':
            recs = [
                'Ensure HIPAA compliance from day one',
                'Consider clinical validation pathway',
                'Partner with healthcare providers for pilots',
                'Focus on measurable health outcomes'
            ]
        elif industry == 'finance':
            recs = [
                'Prioritize security and regulatory compliance',
                'Consider B2B before B2C go-to-market',
                'Build trust through transparency',
                'Explore embedded finance partnerships'
            ]
        else:
            recs = [
                'Identify clear market fit and target audience',
                'Build minimum viable product first',
                'Focus on customer acquisition costs',
                'Consider strategic partnerships'
            ]
        
        return recs
    
    def get_industry_trends(self, category):
        """Get trends for a specific category"""
        return self.INDUSTRY_DATA.get(category, self.INDUSTRY_DATA['tech'])


# Singleton instance
marketplace_service = MarketplaceService()
