document.addEventListener('DOMContentLoaded', function() {
    // Initialize autocomplete functionality for available stocks
    setupAutocomplete();
});

function setupAutocomplete() {
    const inputField = document.getElementById('stockInput'); // The input field for stock search

    inputField.addEventListener('input', function() {
        const searchQuery = inputField.value;
        if (searchQuery.length === 0) {
            clearSuggestions();
            return; // Optionally, adjust the minimum length before search
        }

        fetch(`/api/available-stocks?search=${encodeURIComponent(searchQuery)}`)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.stocks, inputField);
            })
            .catch(error => console.error('Error fetching available stocks:', error));
    });
}

function displaySuggestions(stocks, inputField) {
    const suggestionsBox = document.getElementById('stockSuggestions');
    suggestionsBox.innerHTML = ''; // Clear previous suggestions

    stocks.forEach(stock => {
        const suggestion = document.createElement('div');
        suggestion.textContent = stock;
        suggestion.addEventListener('click', function() {
            inputField.value = stock; // Set input field to the selected stock
            clearSuggestions();
        });
        suggestionsBox.appendChild(suggestion);
    });
}

function clearSuggestions() {
    const suggestionsBox = document.getElementById('stockSuggestions');
    suggestionsBox.innerHTML = ''; // Clear the suggestions
}

function fetchStockPrice() {
    const stockSymbol = document.getElementById('stockInput').value || document.getElementById('customStockInput').value;
    if (!stockSymbol) {
        alert('Please enter a stock symbol.');
        return;
    }

    fetch(`/api/stock-data/${stockSymbol}`)
        .then(response => response.json())
        .then(data => {
            renderStockPriceChart(data);
        })
        .catch(error => {
            console.error('Error fetching stock price:', error);
            alert('Failed to fetch stock price. Please try again later.');
        });
}

function renderStockPriceChart(data) {
    const ctx = document.getElementById('stockPriceChartId').getContext('2d');
    // Clear existing chart if any
    if (window.stockPriceChart) {
        window.stockPriceChart.destroy();
    }
    window.stockPriceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: `${data.symbol} Price Chart`,
                data: data.prices,
                borderColor: 'blue',
                fill: false,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
}
