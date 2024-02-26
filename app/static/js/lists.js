document.addEventListener('DOMContentLoaded', function() {
    fetchStockLists();
    document.getElementById('listSelector').addEventListener('change', handleListSelectionChange);
});

function fetchStockLists() {
    fetch('/api/create-list')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const listSelector = document.getElementById('listSelector');
            // Clear existing options first
            listSelector.innerHTML = '<option value="">Select a list...</option>';
            data.forEach(list => {
                const option = document.createElement('option');
                option.value = list.id; // Assuming you'll identify lists by name
                option.textContent = list.name;
                listSelector.appendChild(option);
            });
        });
}

function handleListSelectionChange() {
    const listId = document.getElementById('listSelector').value;
    if (listId) {
        fetchStockListReturnsAndRenderGraph(listId);
    }
}

function fetchStockListReturnsAndRenderGraph(listId) {
    // Construct the URL with query parameters for start and end dates
    const startDate = '2020-01-06'; // Example start date, adjust as needed
    const endDate = new Date().toISOString().slice(0, 10); // Today's date in YYYY-MM-DD format
    const url = `/api/list-returns/${listId}?start=${startDate}&end=${endDate}`;
    
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        const ctx = document.getElementById('portfolioReturnsChart').getContext('2d');
        // Check if a Chart instance already exists on the canvas
        if (window.chartInstance) {
            window.chartInstance.destroy(); // Destroy the existing Chart instance
        }
        window.chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: [{
                    label: 'Portfolio Cumulative Returns',
                    data: data.returns,  // Already in percentage
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false,
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value, index, values) {
                                return value + '%';  // Add '%' to the Y-axis labels
                            }
                        }
                    }
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem, chart) {
                            var label = chart.datasets[tooltipItem.datasetIndex].label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += tooltipItem.yLabel.toFixed(2) + '%';
                            return label;
                        }
                    }
                }
            }
        });

    });
}
document.getElementById('createListForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from submitting the traditional way
    
    const listName = document.getElementById('listName').value;
    const listTickers = document.getElementById('listTickers').value.split(',');
    const tickerType = document.getElementById('tickerType').value; // Assuming a single type for all tickers for simplicity

    const assets = listTickers.map(ticker => ({
        ticker: ticker.trim(),
        type: tickerType // This assumes all tickers in the input are of the same type; adjust if needed
    }));

    const data = { name: listName, assets: assets };

    // Send the data to the server
    fetch('/api/create-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('List created:', data);
        // Handle success
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors
    });
});