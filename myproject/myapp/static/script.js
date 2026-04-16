const fields = [
    { name: 'Hospitality', icon: '🏨', ideas: ['AI concierge chatbot for hotels', 'Personalized room service via app', 'VR hotel tours'] },
    { name: 'Education', icon: '🎓', ideas: ['Adaptive learning platforms', 'Gamified skill courses', 'AI tutors for homework'] },
    { name: 'AI', icon: '🤖', ideas: ['Custom AI assistants', 'Predictive analytics tools', 'Image generation services'] },
    { name: 'Business Strategy', icon: '📈', ideas: ['SWOT automation tools', 'Market trend predictors', 'Competitor analysis dashboards'] },
    { name: 'Startup', icon: '🚀', ideas: ['No-code MVP builders', 'Investor matching platforms', 'Founder networking apps'] },
    { name: 'Furniture', icon: '🛋️', ideas: ['AR furniture visualizers', 'Custom modular designs', 'Sustainable material marketplaces'] },
    { name: 'Home Decor', icon: '🏠', ideas: ['AI interior designers', 'Smart lighting systems', 'Personalized wall art generators'] },
    { name: 'Gifts', icon: '🎁', ideas: ['Personalized gift recommenders', 'Subscription surprise boxes', 'Engraved tech gadgets'] },
    { name: 'Healthcare', icon: '🏥', ideas: ['Telemedicine apps', 'Wearable health monitors', 'Mental health chatbots'] },
    { name: 'Finance', icon: '💰', ideas: ['Crypto portfolio trackers', 'Automated investment advisors', 'Expense splitting apps'] },
    { name: 'E-commerce', icon: '🛒', ideas: ['Voice shopping assistants', 'Social commerce platforms', 'Try-before-buy services'] },
    { name: 'Fitness', icon: '💪', ideas: ['AI workout planners', 'Virtual trainers', 'Nutrition scanners'] },
    { name: 'Travel', icon: '✈️', ideas: ['Itinerary optimizers', 'Budget travel planners', 'Local experience marketplaces'] },
    { name: 'Gaming', icon: '🎮', ideas: ['AI opponents', 'Cloud streaming services', 'Esports training tools'] },
    { name: 'Food', icon: '🍔', ideas: ['Recipe generators', 'Meal kit customizers', 'Diet-specific delivery'] },
    { name: 'Fashion', icon: '👗', ideas: ['Virtual fitting rooms', 'Style advisors', 'Sustainable clothing swaps'] },
    { name: 'Real Estate', icon: '🏘️', ideas: ['Property valuation AI', 'Virtual tours', 'Neighborhood insight tools'] },
    { name: 'Agriculture', icon: '🌾', ideas: ['Crop yield predictors', 'Drone monitoring', 'Smart irrigation'] },
    { name: 'Environment', icon: '🌍', ideas: ['Carbon footprint trackers', 'Recycling apps', 'Eco-product recommenders'] },
    { name: 'Music', icon: '🎵', ideas: ['AI composers', 'Personalized playlists', 'Collaborative song makers'] },
    { name: 'Automotive', icon: '🚗', ideas: ['EV charging optimizers', 'Car sharing platforms', 'Maintenance predictors'] },
    { name: 'Books', icon: '📚', ideas: ['AI book summarizers', 'Reading habit trackers', 'Personalized recommendations'] }
];



document.getElementById('analyzeBtn').addEventListener('click', function() {
    const idea = document.getElementById('ideaInput').value.trim();
    
    // Enhanced validation for invalid/nonsense input
    if (!isValidIdea(idea)) {
        showInvalidPopup();
        return;
    }

    // Generate SWOT
    generateSWOT();
    
    // Show sections
    document.getElementById('swotSection').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('swotSection').scrollIntoView({ behavior: 'smooth' });
});

// Enhanced validation: checks for empty, too short, no letters, or gibberish
function isValidIdea(idea) {
    if (!idea) return false;
    if (idea.length < 10) return false;
    
    // Check if contains alphabetic characters (letters)
    if (!/[a-zA-Z]/.test(idea)) return false;
    
    // Check for gibberish: too many repeated chars or no spaces/vowels after first few words
    const words = idea.split(/\s+/).filter(w => w.length > 0);
    if (words.length < 2) return false;
    
    // Simple gibberish check: no vowels in most words
    const vowels = /[aeiouAEIOU]/;
    const gibberishWords = words.filter(word => !vowels.test(word) && word.length > 3);
    if (gibberishWords.length > words.length * 0.6) return false; // More than 60% gibberish
    
    return true;
}

// Show custom styled invalid input popup
function showInvalidPopup() {
    // Remove existing popup if any
    const existing = document.querySelector('.invalid-popup-overlay');
    if (existing) existing.remove();
    
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'invalid-popup-overlay show';
    
    // Create popup content
    overlay.innerHTML = `
        <div class="invalid-popup">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Invalid Input!</h3>
            <p>Please enter a meaningful idea or description. Try again with more details!</p>
            <button onclick="this.closest('.invalid-popup-overlay').remove()">Got it!</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        if (overlay.parentNode) {
            overlay.classList.remove('show');
            setTimeout(() => overlay.remove(), 300);
        }
    }, 4000);
    
    // Click overlay to dismiss
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            overlay.classList.remove('show');
            setTimeout(() => overlay.remove(), 300);
        }
    });
}

function generateSWOT() {
    const lists = {
        strengths: document.getElementById('strengthsList'),
        weaknesses: document.getElementById('weaknessesList'),
        opportunities: document.getElementById('opportunitiesList'),
        threats: document.getElementById('threatsList')
    };

    Object.keys(lists).forEach(key => {
        const list = lists[key];
        list.innerHTML = '';
        const items = swotTemplates[key];
        const shuffled = items.sort(() => Math.random() - 0.5).slice(0, 4);
        
        shuffled.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = `• ${item}`;
            li.style.animationDelay = `${index * 0.1}s`;
            list.appendChild(li);
        });
    });
}

// Variety Section Functionality
function generateVariety() {
    const grid = document.getElementById('varietyGrid');
    if (!grid) return;

fields.forEach((field, index) => {
        const card = document.createElement('div');
        card.className = 'variety-card';
        card.dataset.fieldIndex = index; // For unique color
        card.innerHTML = `
            <div class="icon">${field.icon}</div>
            <h4>${field.name}</h4>
            <p class="preview">${field.ideas[0]}</p>
            <ul class="full-ideas">
                <li>${field.ideas[1]}</li>
                <li>${field.ideas[2]}</li>
            </ul>
            <button class="toggle-btn">Show More <i class="fas fa-plus"></i></button>
        `;
        card.style.animationDelay = `${index * 0.05}s`;
        grid.appendChild(card);
    });

    // Add click handlers after population
    grid.addEventListener('click', function(e) {
        const card = e.target.closest('.variety-card');
        if (!card) return;

        if (e.target.classList.contains('toggle-btn') || e.target.tagName === 'I') {
            card.classList.toggle('expanded');
            const btn = card.querySelector('.toggle-btn');
            if (card.classList.contains('expanded')) {
                btn.innerHTML = 'Show Less <i class="fas fa-minus"></i>';
            } else {
                btn.innerHTML = 'Show More <i class="fas fa-plus"></i>';
            }
        } else {
            // Click anywhere else on card to toggle
            card.classList.toggle('expanded');
            const btn = card.querySelector('.toggle-btn');
            if (card.classList.contains('expanded')) {
                btn.innerHTML = 'Show Less <i class="fas fa-minus"></i>';
            } else {
                btn.innerHTML = 'Show More <i class="fas fa-plus"></i>';
            }
        }
    });
}

// Init on DOM load
document.addEventListener('DOMContentLoaded', function() {
    generateVariety();
    
    // Existing input focus handler
    document.getElementById('ideaInput').addEventListener('focus', function() {
        this.placeholder = 'Type your brilliant idea... Watch the magic happen!';
    });
});
