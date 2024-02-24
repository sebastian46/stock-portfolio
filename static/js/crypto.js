document.addEventListener('DOMContentLoaded', function() {
    // Fetch available crypto and populate the dropdown menu
    fetchAvailableCrypto();
});

function fetchAvailableCrypto() {
    fetch('/api/available-crypto')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const cryptoDropdown = document.getElementById('cryptoDropdown');
            // Clear existing options first
            cryptoDropdown.innerHTML = '<option value="">Select a crypto...</option>';
            // Populate dropdown with available crypto
            data.crypto.forEach(crypto => {
                const option = document.createElement('option');
                option.value = crypto;
                option.textContent = `${crypto}`;
                cryptoDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching available crypto:', error));
}

function fetchCryptoPrice() {
    const selectedCrypto = document.getElementById('cryptoDropdown').value;
    const customCrypto = document.getElementById('customCryptoInput').value;
    const cryptoSymbol = customCrypto || selectedCrypto;
    if (!cryptoSymbol) {
        alert('Please select or enter a crypto symbol.');
        return;
    }
    fetch(`/api/crypto-data/${cryptoSymbol}`)
        .then(response => response.json())
        .then(data => {
            renderCryptoPriceChart(data);
        })
        .catch(error => {
            console.error('Error fetching crypto price:', error);
            alert('Failed to fetch crypto price. Please try again later.');
        });
}

function renderCryptoPriceChart(data) {
    const ctx = document.getElementById('cryptoPriceChartId').getContext('2d');
    // Clear existing chart if any
    if (window.cryptoPriceChart) {
        window.cryptoPriceChart.destroy();
    }
    window.cryptoPriceChart = new Chart(ctx, {
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
                    beginAtZero: false,
                }
            }
        }
    });
}
