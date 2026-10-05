document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const payload = {
        rank: parseFloat(document.getElementById('rank').value),
        ranker_score: parseFloat(document.getElementById('rank_score').value),
        pool_row: parseFloat(document.getElementById('pool_row').value),
        popularity: parseFloat(document.getElementById('popularity').value),
        pool_source: parseFloat(document.getElementById('pool_source').value),
        lib_max: parseFloat(document.getElementById('lib_max').value)
    };

    console.log("Sending payload to backend:", payload);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("422 Validation Error Detail:", errorData);
            throw new Error(JSON.stringify(errorData.detail || 'API Request Failed'));
        }

        const data = await response.json();

        document.getElementById('is-truth-value').innerText = data.is_truth === 1 ? 'True (1)' : 'False (0)';
        document.getElementById('confidence-value').innerText = data.confidence !== null ? (data.confidence * 100).toFixed(2) + '%' : 'N/A';
        
        document.getElementById('result-box').classList.remove('hidden');

    } catch (error) {
        alert('Validation or Server Error: ' + error.message);
        console.error('Prediction Error:', error);
    }
});