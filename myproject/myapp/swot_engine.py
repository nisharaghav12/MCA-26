"""
SWOT Engine - Generates contextual SWOT analysis based on idea and market data
"""
import random, re
from django.utils import timezone


class SWOTEngine:
    SWOT_TEMPLATES = {
        'strengths': ['Unique value proposition', 'Skilled team', 'Early mover advantage', 'Strong IP', 'Scalable model'],
        'weaknesses': ['Limited funding', 'Small team', 'No brand recognition', 'No product-market fit', 'Limited channels'],
        'opportunities': ['Growing demand', 'Emerging trends', 'Strategic partnerships', 'New markets', 'B2B opportunities'],
        'threats': ['Established competitors', 'Regulatory changes', 'Market saturation', 'Price wars', 'Talent challenges']
    }
    
    INDUSTRY_SWOT_MODIFIERS = {
        'tech': {'strengths': ['Strong tech foundation'], 'weaknesses': ['Technical debt'], 'opportunities': ['API ecosystem'], 'threats': ['Rapid disruption']},
        'healthcare': {'strengths': ['HIPAA compliance'], 'weaknesses': ['Long sales cycles'], 'opportunities': ['Telemedicine'], 'threats': ['FDA regulations']},
        'finance': {'strengths': ['Regulatory compliance'], 'weaknesses': ['Complex compliance'], 'opportunities': ['Unbanked market'], 'threats': ['Regulatory changes']},
        'education': {'strengths': ['Learning science'], 'weaknesses': ['Low retention'], 'opportunities': ['Corporate training'], 'threats': ['Free alternatives']}
    }
    
    def generate_swot(self, idea, market_data=None):
        keywords = self._extract_keywords(idea.lower())
        industry = market_data.get('detected_industry', 'tech') if market_data else 'tech'
        
        return {
            'strengths': self._generate_contextual_items('strengths', keywords, industry, market_data),
            'weaknesses': self._generate_contextual_items('weaknesses', keywords, industry, market_data),
            'opportunities': self._generate_contextual_items('opportunities', keywords, industry, market_data),
            'threats': self._generate_contextual_items('threats', keywords, industry, market_data)
        }
    
    def _extract_keywords(self, idea):
        stop_words = {'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'app', 'solution', 'platform', 'service', 'product', 'business', 'company', 'startup', 'idea', 'new', 'use', 'using'}
        words = re.findall(r'\b[a-z]{3,}\b', idea)
        return [w for w in words if w not in stop_words][:10]
    
    def _generate_contextual_items(self, category, keywords, industry, market_data):
        items = list(self.SWOT_TEMPLATES[category])
        if industry in self.INDUSTRY_SWOT_MODIFIERS:
            items.extend(self.INDUSTRY_SWOT_MODIFIERS[industry].get(category, []))
        
        keyword_items = []
        for kw in keywords[:3]:
            if category == 'strengths' and len(kw) > 4:
                keyword_items.append(f"Strong {kw} capability")
            elif category == 'weaknesses' and len(kw) > 4:
                keyword_items.append(f"Building {kw} expertise")
            elif category == 'opportunities' and len(kw) > 4:
                keyword_items.append(f"{kw.capitalize()} market expansion")
            elif category == 'threats' and len(kw) > 4:
                keyword_items.append(f"{kw.capitalize()} competition")
        
        items.extend(keyword_items)
        random.shuffle(items)
        return items[:5]
    
    def get_swot_templates(self):
        return self.SWOT_TEMPLATES
    
    def generate_feasibility_report(self, idea, market_data=None):
        industry = market_data.get('detected_industry', 'tech') if market_data else 'tech'
        
        m_score = random.randint(6, 9)
        t_score = random.randint(5, 8)
        f_score = random.randint(5, 8)
        o_score = random.randint(6, 9)
        overall = (m_score + t_score + f_score + o_score) / 4
        
        verdict = 'Highly Feasible' if overall >= 7.5 else 'Feasible' if overall >= 6 else 'Moderately Feasible' if overall >= 5 else 'Requires Analysis'
        
        return {
            'executive_summary': f"Feasibility analysis for: {idea}",
            'overall_viability': round(overall * 10, 1),
            'verdict': verdict,
            'market_analysis': {'score': m_score, 'market_size': market_data.get('market_size', 'TBD') if market_data else 'TBD', 'growth_rate': market_data.get('growth', 'N/A') if market_data else 'N/A'},
            'technical_feasibility': {'score': t_score, 'complexity': 'Medium' if t_score >= 6 else 'High', 'development_time': f"{random.randint(3, 6)} months"},
            'financial_viability': {'score': f_score, 'estimated_cost': f"₹{random.randint(5, 50)} Lakhs", 'break_even': f"{random.randint(12, 36)} months"},
            'operational_feasibility': {'score': o_score, 'team_needed': f"{random.randint(3, 10)} full-time"},
            'risks': [{'risk': 'Market Acceptance', 'severity': 'Medium', 'mitigation': 'Iterate based on feedback'}],
            'recommendations': ['Conduct market research', 'Build MVP first']
        }
    
    def generate_detailed_report(self, idea, market_data=None):
        swot = self.generate_swot(idea, market_data)
        industry = market_data.get('detected_industry', 'tech') if market_data else 'tech'
        
        return {
            'title': f'Detailed SWOT: {idea}',
            'generated_at': timezone.now().isoformat(),
            'swot': swot,
            'detailed_insights': {
                'strengths': {'analysis': ['Analyze strengths'], 'action_items': ['Build on core strengths']},
                'weaknesses': {'analysis': ['Address weaknesses'], 'action_items': ['Create mitigation plan']},
                'opportunities': {'analysis': ['Capture opportunities'], 'action_items': ['Build partnerships']},
                'threats': {'analysis': ['Mitigate threats'], 'action_items': ['Monitor continuously']}
            },
            'industry_context': {'sector': industry},
            'strategic_recommendations': ['Build sustainable advantage']
        }


swot_engine = SWOTEngine()
