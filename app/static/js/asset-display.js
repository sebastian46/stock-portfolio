document.addEventListener('DOMContentLoaded', function() {
    // Initialize autocomplete functionality for all asset types
    document.querySelectorAll('.asset-input').forEach(inputField => {
        setupAutocomplete(inputField);
    });

    // Setup event listeners for all "Get Price Chart" buttons
    document.querySelectorAll('.fetch-price-btn').forEach(button => {
        button.addEventListener('click', function() {
            const assetType = this.closest('.asset-input-group').getAttribute('data-asset-type');
            fetchAssetPrice(assetType);
        });
    });
});

function setupAutocomplete(inputField) {
    const assetType = inputField.closest('.asset-input-group').getAttribute('data-asset-type');
    const suggestionsBoxId = `${assetType}Suggestions`;

    inputField.addEventListener('input', function() {
        const searchQuery = inputField.value;
        if (searchQuery.length === 0) {
            clearSuggestions(suggestionsBoxId);
            return;
        }

        fetch(`/api/available-${assetType}?search=${encodeURIComponent(searchQuery)}`)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data[assetType], inputField, suggestionsBoxId);
            })
            .catch(error => console.error(`Error fetching available ${assetType}:`, error));
    });
}

function displaySuggestions(assets, inputField, suggestionsBoxId) {
    const suggestionsBox = document.getElementById(suggestionsBoxId);
    suggestionsBox.innerHTML = '';

    assets.forEach(assets => {
        const suggestion = document.createElement('div');
        suggestion.textContent = assets;
        suggestion.addEventListener('click', function() {
            inputField.value = assets;
            clearSuggestions(suggestionsBoxId);
        });
        suggestionsBox.appendChild(suggestion);
    });
}

function clearSuggestions(suggestionsBoxId) {
    const suggestionsBox = document.getElementById(suggestionsBoxId);
    suggestionsBox.innerHTML = '';
}

function fetchAssetPrice(assetType) {
    const assetGroup = document.querySelector(`.asset-input-group[data-asset-type="${assetType}"]`);
    const assetInput = assetGroup.querySelector('.asset-input').value;
    const customInput = assetGroup.querySelector('.form-control').value;
    const assetSymbol = assetInput || customInput;
    const url = `api/asset-data/${assetType}/${assetSymbol}`;

    if (!assetSymbol) {
        alert(`Please enter a ${assetType} symbol.`);
        return;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const chartId = `${assetType}PriceChartId`;
            renderPriceChart(data, chartId, `${data.symbol} Price Chart`);
        })
        .catch(error => {
            console.error(`Error fetching ${assetType} price:`, error);
            alert(`Failed to fetch ${assetType} price. Please try again later.`);
        });
}

function renderPriceChart(data, chartId, label) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    // Construct the variable name based on chartId
    const chartVarName = chartId + 'PriceChart';

    // Check if a chart instance already exists and destroy it if so
    if (window[chartVarName]) {
        window[chartVarName].destroy();
    }

    // Create a new chart instance and assign it to the dynamically named window variable
    window[chartVarName] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: label,
                data: data.prices,
                borderColor: 'blue',
                fill: false,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                }
            }
        }
    });
}