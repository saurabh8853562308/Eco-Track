/* ============================================
   CARBON FOOTPRINT CALCULATOR - JAVASCRIPT
   ============================================ */

// Carbon emission factors (kg CO2e per unit)
const CARBON_FACTORS = {
    food: {
        beef: 27.0,        // kg CO2e per kg
        chicken: 6.9,      // kg CO2e per kg
        fish: 5.0,         // kg CO2e per kg
        vegetable: 2.0,    // kg CO2e per kg
    },
    energy: {
        electricity: 0.92,  // kg CO2e per kWh
        natural_gas: 2.04,  // kg CO2e per cubic meter
    },
    transport: {
        car: 0.411,        // kg CO2e per mile
        public_transport: 0.089, // kg CO2e per mile
    }
};

// Chart instance (global variable)
let footprintChart = null;

/**
 * Calculate carbon footprint and display results
 */
function calculateFootprint() {
    // Get input values
    const inputs = {
        beef: parseFloat(document.getElementById('beef').value) || 0,
        chicken: parseFloat(document.getElementById('chicken').value) || 0,
        fish: parseFloat(document.getElementById('fish').value) || 0,
        vegetable: parseFloat(document.getElementById('vegetable').value) || 0,
        electricity: parseFloat(document.getElementById('electricity').value) || 0,
        natural_gas: parseFloat(document.getElementById('natural_gas').value) || 0,
        car_miles: parseFloat(document.getElementById('car_miles').value) || 0,
        public_transport_miles: parseFloat(document.getElementById('public_transport_miles').value) || 0,
    };

    // Validate inputs
    if (!isValidInput(inputs)) {
        alert('Please enter valid numbers for all fields.');
        return;
    }

    // Send data to server for calculation
    const csrfToken = getCsrfToken();
    
    fetch('/api/calculate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(inputs),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayResults(data);
            showResultsSection();
            updateChart(data);
        } else {
            alert('Error calculating footprint: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while calculating your footprint. Please try again.');
    });
}

/**
 * Validate input values
 */
function isValidInput(inputs) {
    for (let key in inputs) {
        if (isNaN(inputs[key]) || inputs[key] < 0) {
            return false;
        }
    }
    return true;
}

/**
 * Get CSRF token from cookie
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue || '';
}

/**
 * Display results in the results section
 */
function displayResults(data) {
    // Update monthly and annual carbon
    document.getElementById('monthly-carbon').textContent = data.monthly_carbon.toLocaleString();
    document.getElementById('annual-carbon').textContent = data.annual_carbon.toLocaleString();

    // Update breakdown
    document.getElementById('food-carbon').textContent = data.food_carbon.toLocaleString();
    document.getElementById('energy-carbon').textContent = data.energy_carbon.toLocaleString();
    document.getElementById('transport-carbon').textContent = data.transport_carbon.toLocaleString();

    // Show motivational message based on carbon amount
    displayMotivationalMessage(data.monthly_carbon);
}

/**
 * Show motivational message based on carbon footprint
 */
function displayMotivationalMessage(carbonAmount) {
    let message = '';
    let emoji = '';

    if (carbonAmount < 50) {
        emoji = '🌟';
        message = 'Excellent! You have a very low carbon footprint. Keep up the sustainable lifestyle!';
    } else if (carbonAmount < 100) {
        emoji = '✨';
        message = 'Great! Your carbon footprint is below average. Continue making sustainable choices!';
    } else if (carbonAmount < 200) {
        emoji = '💪';
        message = 'Good start! You\'re on the right track. Consider implementing some of our tips to reduce further.';
    } else if (carbonAmount < 300) {
        emoji = '🎯';
        message = 'Time to take action! Implement the recommended tips to significantly reduce your carbon footprint.';
    } else {
        emoji = '🌍';
        message = 'This is a good opportunity to make meaningful changes. Start with the highest impact areas.';
    }

    // Create and display notification
    const notification = document.createElement('div');
    notification.className = 'motivational-message';
    notification.style.cssText = `
        background: linear-gradient(135deg, #2ecc71, #3498db);
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
        text-align: center;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    `;
    notification.innerHTML = `${emoji} ${message}`;

    const resultsSection = document.getElementById('results-section');
    const existingNotification = resultsSection.querySelector('.motivational-message');
    if (existingNotification) {
        existingNotification.remove();
    }
    resultsSection.querySelector('.container').insertBefore(notification, resultsSection.querySelector('h2').nextElementSibling);
}

/**
 * Show the results section
 */
function showResultsSection() {
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update the chart with current data
 */
function updateChart(data) {
    const ctx = document.getElementById('footprintChart');
    
    if (!ctx) {
        console.error('Canvas element not found');
        return;
    }

    // Destroy existing chart if it exists
    if (footprintChart) {
        footprintChart.destroy();
    }

    // Create new chart
    footprintChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Food', 'Energy', 'Transport'],
            datasets: [{
                data: [
                    data.food_carbon,
                    data.energy_carbon,
                    data.transport_carbon
                ],
                backgroundColor: [
                    '#e74c3c',  // Food - red
                    '#3498db',  // Energy - blue
                    '#f39c12',  // Transport - orange
                ],
                borderColor: [
                    '#c0392b',
                    '#2980b9',
                    '#d68910',
                ],
                borderWidth: 2,
                hoverOffset: 10,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold',
                        },
                        padding: 20,
                        color: '#34495e',
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold',
                    },
                    bodyFont: {
                        size: 12,
                    },
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return context.label + ': ' + value.toFixed(2) + ' kg CO₂e (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Reset the calculator form
 */
function resetForm() {
    // Get all input fields
    const inputs = document.querySelectorAll('.input-field');
    
    // Clear all inputs
    inputs.forEach(input => {
        input.value = '';
    });

    // Hide results section
    document.getElementById('results-section').style.display = 'none';

    // Destroy chart
    if (footprintChart) {
        footprintChart.destroy();
        footprintChart = null;
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Add event listeners for real-time calculation feedback
 */
function addEventListeners() {
    const inputs = document.querySelectorAll('.input-field');
    
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            // Optional: Add visual feedback on change
            this.style.borderColor = '#2ecc71';
            setTimeout(() => {
                this.style.borderColor = '#ddd';
            }, 500);
        });

        // Enter key to calculate
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                calculateFootprint();
            }
        });
    });
}

/**
 * Initialize the calculator on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    addEventListeners();

    // Add smooth scrolling for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Log initialization
    console.log('Carbon Footprint Calculator initialized successfully!');
});

/**
 * Format number with thousand separators
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
