// SWOT Analyzer - Complete JavaScript

// ==================== DATA ====================
const swotTemplates = {
    strengths: ['Unique value proposition', 'Skilled team', 'Early mover advantage', 'Strong IP', 'Scalable model', 'Strong brand', 'Data-driven', 'Agile'],
    weaknesses: ['Limited funding', 'Small team', 'No brand recognition', 'No product-market fit', 'Limited channels', 'Technical debt', 'Resource constraints'],
    opportunities: ['Growing demand', 'Emerging trends', 'Strategic partnerships', 'New markets', 'B2B opportunities', 'International expansion'],
    threats: ['Established competitors', 'Regulatory changes', 'Market saturation', 'Price wars', 'Talent challenges', 'Tech disruption']
};

const fields = [
    { name: 'Hospitality', icon: '🏨', ideas: ['AI concierge chatbot', 'Personalized room service', 'VR hotel tours'] },
    { name: 'Education', icon: '🎓', ideas: ['Adaptive learning', 'Gamified courses', 'AI tutors'] },
    { name: 'AI', icon: '🤖', ideas: ['Custom AI assistants', 'Predictive analytics', 'Image generation'] },
    { name: 'Startup', icon: '🚀', ideas: ['No-code MVP builders', 'Investor matching', 'Founder networking'] },
    { name: 'Healthcare', icon: '🏥', ideas: ['Telemedicine apps', 'Wearable monitors', 'Mental health chatbots'] },
    { name: 'Finance', icon: '💰', ideas: ['Crypto trackers', 'Automated advisors', 'Expense splitting'] },
    { name: 'E-commerce', icon: '🛒', ideas: ['Voice shopping', 'Social commerce', 'Try-before-buy'] },
    { name: 'Fitness', icon: '💪', ideas: ['AI workout planners', 'Virtual trainers', 'Nutrition scanners'] }
];

// ==================== STATE ====================
let currentUser = null;
let currentSwot = null;
let currentFeasibility = null;
let currentMarketData = null;

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    generateVariety();
    checkUserStatus();
    setupEventListeners();
});

function setupEventListeners() {
    // document.getElementById('analyzeBtn').addEventListener('click', generateSwot);
    document.getElementById('feasibilityBtn').addEventListener('click', generateFeasibility);
    document.getElementById('saveSwotBtn').addEventListener('click', saveSwot);
    document.getElementById('saveFeasibilityBtn').addEventListener('click', saveFeasibility);
}

// ==================== AUTH ====================
function showAuthModal() { document.getElementById('authModal').classList.add('show'); }
function closeAuthModal() { document.getElementById('authModal').classList.remove('show'); }
function showLogin() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
}
function showRegister() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
}

async function doLogin() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const res = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        if (data.success) {
            currentUser = data.user;
            updateUserUI();
            closeAuthModal();
            showToast('Login successful!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch(e) { showToast('Login failed', 'error'); }
}

async function doRegister() {
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    
    try {
        const res = await fetch('/api/auth/register/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        const data = await res.json();
        if (data.success) {
            currentUser = data.user;
            updateUserUI();
            closeAuthModal();
            showToast('Registration successful!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch(e) { showToast('Registration failed', 'error'); }
}

async function doLogout() {
    await fetch('/api/auth/logout/', {method: 'POST'});
    currentUser = null;
    updateUserUI();
    showToast('Logged out', 'success');
}

async function checkUserStatus() {
    try {
        const res = await fetch('/api/auth/status/');
        const data = await res.json();
        if (data.authenticated || true) {
            currentUser = data;
            updateUserUI();
        }
    } catch(e) { console.log('Not logged in'); }
}

function updateUserUI() {
    const loginBtn = document.getElementById('loginBtn');
    const userInfo = document.getElementById('userInfo');
    const usageInfo = document.getElementById('usageInfo');
    const premiumBadge = document.getElementById('premiumBadge');
    const userName = document.getElementById('userName');
    const remainingUses = document.getElementById('remainingUses');
    
    if (currentUser && currentUser.authenticated) {
        loginBtn.classList.add('hidden');
        userInfo.classList.remove('hidden');
        usageInfo.classList.remove('hidden');
        userName.textContent = currentUser.username;
        remainingUses.textContent = `Free uses remaining: ${currentUser.remaining_uses}`;
        
        if (currentUser.is_premium) {
            premiumBadge.classList.remove('hidden');
            remainingUses.textContent = 'Premium - Unlimited uses';
        }
    } else {
        loginBtn.classList.remove('hidden');
        userInfo.classList.add('hidden');
        usageInfo.classList.add('hidden');
    }
}

function showPremiumModal() { document.getElementById('premiumModal').classList.add('show'); }
function closePremiumModal() { document.getElementById('premiumModal').classList.remove('show'); }

async function activatePremium() {
    try {
        const res = await fetch('/api/premium/activate/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({payment_method: 'demo'})
        });
        const data = await res.json();
        if (data.success) {
            currentUser.is_premium = true;
            updateUserUI();
            closePremiumModal();
            showToast('Premium activated!', 'success');
        }
    } catch(e) { showToast('Activation failed', 'error'); }
}

// ==================== SWOT GENERATION ====================
async function generateSwot() {
    const idea = document.getElementById('ideaInput').value.trim();

    if (!isValidIdea(idea)) {
        showInvalidPopup();
        return;
    }

    console.log("idea is valid 122");

    showLoading(true);

    try {
        const res = await fetch('/api/swot/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                idea,
                detailed: true,
                detail: 'garsgwlckdw'
            })
        });

        const data = await res.json();

        console.log("data is coming");
        console.log(data);

        if (data.premium_required) {
            showLoading(false);
            showPremiumModal();
            showToast(data.message, 'error');
            return;
        }

        currentSwot = data.swot;
        currentMarketData = data.market_data;

        displayMarketData(data.market_data);
        displaySwot(data.swot);

        document.getElementById('swotSection').classList.remove('hidden');
        document.getElementById('feasibilitySection').classList.add('hidden');

        checkUserStatus();

    } catch (e) {
        console.error(e);
        showToast('Error generating SWOT', 'error');
    }

    showLoading(false);
}

// ==================== FEASIBILITY REPORT ====================
async function generateFeasibility() {
    const idea = document.getElementById('ideaInput').value.trim();
    if (!isValidIdea(idea)) { showInvalidPopup(); return; }
    
    showLoading(true);
    
    try {
        const res = await fetch('/api/swot/feasibility/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({idea})
        });
        const data = await res.json();
        
        if (data.premium_required) {
            showLoading(false);
            showPremiumModal();
            showToast(data.message, 'error');
            return;
        }
        
        currentFeasibility = data.feasibility;
        currentMarketData = data.market_data;
        
        displayFeasibility(data.feasibility);
        
        document.getElementById('feasibilitySection').classList.remove('hidden');
        document.getElementById('swotSection').classList.add('hidden');
        
        checkUserStatus();
    } catch(e) {
        showToast('Error generating report', 'error');
    }
    
    showLoading(false);
}

function displayFeasibility(feasibility) {
    const container = document.getElementById('feasibilityContent');
    const f = feasibility;
    
    const verdictClass = f.verdict === 'Highly Feasible' ? 'green' : f.verdict === 'Feasible' ? 'yellow' : 'red';
    
    container.innerHTML = `
        <div class="feasibility-summary">
            <div class="viability-score ${verdictClass}">
                <span class="score">${f.overall_viability}</span>
                <span class="label">Viability Score</span>
                <span class="verdict">${f.verdict}</span>
            </div>
        </div>
        
        <div class="feasibility-grid">
            <div class="feasibility-card">
                <h4><i class="fas fa-chart-bar"></i> Market Analysis</h4>
                <p>Score: ${f.market_analysis.score}/10</p>
                <p>Size: ${f.market_analysis.market_size}</p>
                <p>Growth: ${f.market_analysis.growth_rate}</p>
            </div>
            <div class="feasibility-card">
                <h4><i class="fas fa-cogs"></i> Technical</h4>
                <p>Score: ${f.technical_feasibility.score}/10</p>
                <p>Complexity: ${f.technical_feasibility.complexity}</p>
                <p>Time: ${f.technical_feasibility.development_time}</p>
            </div>
            <div class="feasibility-card">
                <h4><i class="fas fa-rupee-sign"></i> Financial</h4>
                <p>Score: ${f.financial_viability.score}/10</p>
                <p>Cost: ${f.financial_viability.estimated_cost}</p>
                <p>Break-even: ${f.financial_viability.break_even}</p>
            </div>
            <div class="feasibility-card">
                <h4><i class="fas fa-users"></i> Operational</h4>
                <p>Score: ${f.operational_feasibility.score}/10</p>
                <p>Team: ${f.operational_feasibility.team_needed}</p>
            </div>
        </div>
        
        <div class="recommendations-box">
            <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
            <ul>
                ${f.recommendations.map(r => `<li>${r}</li>`).join('')}
            </ul>
        </div>
    `;
}

// ==================== SAVE FUNCTIONS ====================
async function saveSwot() {
    if (!currentUser || !currentUser.authenticated) {
        showAuthModal();
        showToast('Please login to save', 'error');
        return;
    }
    
    try {
        const res = await fetch('/api/swot/save/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                idea: document.getElementById('ideaInput').value,
                swot: currentSwot,
                market_data: currentMarketData,
                is_detailed: true
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast('SWOT saved!', 'success');
            loadHistory();
        }
    } catch(e) { showToast('Error saving', 'error'); }
}

async function saveFeasibility() {
    if (!currentUser || !currentUser.authenticated) {
        showAuthModal();
        showToast('Please login to save', 'error');
        return;
    }
    
    try {
        const res = await fetch('/api/swot/save/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                idea: document.getElementById('ideaInput').value,
                swot: currentSwot,
                feasibility: currentFeasibility,
                market_data: currentMarketData,
                is_detailed: true
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast('Report saved!', 'success');
        }
    } catch(e) { showToast('Error saving', 'error'); }
}

async function loadHistory() {
    if (!currentUser || !currentUser.authenticated) return;
    
    try {
        const res = await fetch('/api/swot/history/');
        const data = await res.json();
        if (data.success && data.history.length > 0) {
            document.getElementById('historySection').classList.remove('hidden');
            const list = document.getElementById('historyList');
            list.innerHTML = data.history.map(h => `
                <div class="history-card">
                    <h4>${h.idea}</h4>
                    <p>${new Date(h.created_at).toLocaleDateString()}</p>
                </div>
            `).join('');
        }
    } catch(e) {}
}

// ==================== DISPLAY FUNCTIONS ====================
function displayMarketData(data) {
    document.getElementById('marketSection').classList.remove('hidden');
    document.getElementById('industryName').textContent = data.name || '-';
    document.getElementById('marketSize').textContent = data.market_size || '-';
    document.getElementById('marketGrowth').textContent = data.growth || '-';
    document.getElementById('keyPlayers').textContent = data.key_players ? data.key_players.join(', ') : '-';
}

function displaySwot(swot) {
    const lists = {
        strengths: document.getElementById('strengthsList'),
        weaknesses: document.getElementById('weaknessesList'),
        opportunities: document.getElementById('opportunitiesList'),
        threats: document.getElementById('threatsList')
    };
    
    Object.keys(lists).forEach(key => {
        const list = lists[key];
        list.innerHTML = '';
        swot[key].forEach((item, i) => {
            const li = document.createElement('li');
            li.textContent = item;
            li.style.animationDelay = `${i * 0.1}s`;
            list.appendChild(li);
        });
    });
}

// ==================== VARIETY GRID ====================
function generateVariety() {
    const grid = document.getElementById('varietyGrid');
    if (!grid) return;
    
    fields.forEach((field, i) => {
        const card = document.createElement('div');
        card.className = 'variety-card';
        card.innerHTML = `
            <div class="icon">${field.icon}</div>
            <h4>${field.name}</h4>
            <p>${field.ideas[0]}</p>
        `;
        card.onclick = () => {
            document.getElementById('ideaInput').value = field.ideas[0];
            generateSwot();
        };
        grid.appendChild(card);
    });
}

// ==================== UTILITIES ====================
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) overlay.classList.remove('hidden');
    else overlay.classList.add('hidden');
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function showInvalidPopup() {
    const existing = document.querySelector('.invalid-popup-overlay');
    if (existing) existing.remove();
    
    const overlay = document.createElement('div');
    overlay.className = 'invalid-popup-overlay show';
    overlay.innerHTML = `
        <div class="invalid-popup">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Invalid Input!</h3>
            <p>Please enter a meaningful idea!</p>
            <button onclick="this.closest('.invalid-popup-overlay').remove()">Got it!</button>
        </div>
    `;
    document.body.appendChild(overlay);
    setTimeout(() => overlay.remove(), 4000);
}

function isValidIdea(idea) {
    if (!idea || idea.length < 10) return false;
    if (!/[a-zA-Z]/.test(idea)) return false;
    const words = idea.split(/\s+/).filter(w => w.length > 0);
    if (words.length < 2) return false;
    const vowels = /[aeiouAEIOU]/;
    const gibberishWords = words.filter(w => !vowels.test(w) && w.length > 3);
    if (gibberishWords.length > words.length * 0.6) return false;
    return true;
}
