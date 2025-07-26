// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Crop recommendation form
    const cropForm = document.getElementById('cropForm');
    if (cropForm) {
        cropForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get all form values
            const formData = {
                nitrogen: document.getElementById('nitrogen').value,
                phosphorus: document.getElementById('phosphorus').value,
                potassium: document.getElementById('potassium').value,
                temperature: document.getElementById('temperature').value,
                humidity: document.getElementById('humidity').value,
                ph: document.getElementById('ph').value,
                rainfall: document.getElementById('rainfall').value
            };
            
            // Here you would normally send to a server
            // For now we'll simulate a response
            simulateRecommendation(formData);
        });
    }
});

function simulateRecommendation(data) {
    // This is mock logic - replace with actual API call
    const crops = [
        { name: "Rice", suitability: 85 },
        { name: "Wheat", suitability: 72 },
        { name: "Maize", suitability: 68 }
    ];
    
    // Sort by suitability
    crops.sort((a, b) => b.suitability - a.suitability);
    
    // Display results
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <h3><i class="fas fa-check-circle"></i> Recommended Crops</h3>
        <div class="result-item">
            <span class="crop-name">1. ${crops[0].name}</span>
            <span class="suitability">${crops[0].suitability}% match</span>
        </div>
        <div class="result-item">
            <span class="crop-name">2. ${crops[1].name}</span>
            <span class="suitability">${crops[1].suitability}% match</span>
        </div>
        <p class="advice-note">Based on your soil and weather conditions</p>
    `;
    
    // Scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}