from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with usage tracking and premium status"""
    
    PREMIUM_PRICE = 350  # Monthly price in INR
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    usage_count = models.IntegerField(default=0, help_text="Number of SWOT analyses used")
    is_premium = models.BooleanField(default=False, help_text="Premium subscription status")
    premium_start_date = models.DateTimeField(null=True, blank=True, help_text="Premium start date")
    premium_expiry_date = models.DateTimeField(null=True, blank=True, help_text="Premium expiry date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Free usage limit
    FREE_USAGE_LIMIT = 5
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {'Premium' if self.is_premium else 'Free'}"
    
    @property
    def can_use_free(self):
        """Check if user can use free features"""
        return self.usage_count < self.FREE_USAGE_LIMIT or self.is_premium
    
    @property
    def remaining_free_uses(self):
        """Calculate remaining free uses"""
        if self.is_premium:
            return "Unlimited"
        return max(0, self.FREE_USAGE_LIMIT - self.usage_count)
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count', 'updated_at'])
    
    def activate_premium(self, months=1):
        """Activate premium subscription"""
        from django.utils import timezone
        from datetime import timedelta
        
        self.is_premium = True
        self.premium_start_date = timezone.now()
        self.premium_expiry_date = timezone.now() + timedelta(days=30 * months)
        self.save(update_fields=['is_premium', 'premium_start_date', 'premium_expiry_date', 'updated_at'])


class SWOTAnalysis(models.Model):
    """Model to store SWOT analysis results with market data"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swot_analyses', null=True, blank=True)
    idea = models.TextField(help_text="The startup idea or concept being analyzed")
    strength = models.JSONField(default=list, help_text="List of strengths")
    weakness = models.JSONField(default=list, help_text="List of weaknesses")
    opportunity = models.JSONField(default=list, help_text="List of opportunities")
    threat = models.JSONField(default=list, help_text="List of threats")
    market_data = models.JSONField(null=True, blank=True, help_text="Market research data")
    feasibility_report = models.JSONField(null=True, blank=True, help_text="Feasibility analysis data")
    is_detailed = models.BooleanField(default=False, help_text="Detailed report flag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'SWOT Analysis'
        verbose_name_plural = 'SWOT Analyses'
    
    def __str__(self):
        return f"SWOT: {self.idea[:50]}..."
