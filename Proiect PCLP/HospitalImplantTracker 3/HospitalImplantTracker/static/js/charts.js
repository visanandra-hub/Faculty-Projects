/**
 * Hospital Implant Tracker - Chart Utilities
 * 
 * This file contains utility functions for rendering charts in the application.
 */

/**
 * Create a pie chart
 * @param {string} elementId - The ID of the canvas element
 * @param {Array} labels - The chart labels
 * @param {Array} data - The chart data
 * @param {Array} colors - The chart colors
 */
function createPieChart(elementId, labels, data, colors) {
    const ctx = document.getElementById(elementId).getContext('2d');
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
}

/**
 * Create a doughnut chart
 * @param {string} elementId - The ID of the canvas element
 * @param {Array} labels - The chart labels
 * @param {Array} data - The chart data
 * @param {Array} colors - The chart colors
 */
function createDoughnutChart(elementId, labels, data, colors) {
    const ctx = document.getElementById(elementId).getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
}

/**
 * Create a bar chart
 * @param {string} elementId - The ID of the canvas element
 * @param {Array} labels - The chart labels
 * @param {Array} data - The chart data
 * @param {string} label - The dataset label
 * @param {string} color - The bar color
 */
function createBarChart(elementId, labels, data, label, color) {
    const ctx = document.getElementById(elementId).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

/**
 * Create a line chart
 * @param {string} elementId - The ID of the canvas element
 * @param {Array} labels - The chart labels
 * @param {Array} data - The chart data
 * @param {string} label - The dataset label
 * @param {string} borderColor - The line color
 * @param {string} backgroundColor - The line area color
 */
function createLineChart(elementId, labels, data, label, borderColor, backgroundColor) {
    const ctx = document.getElementById(elementId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: borderColor,
                backgroundColor: backgroundColor,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

/**
 * Get a color palette for charts
 * @param {number} count - Number of colors needed
 * @returns {Array} Array of colors
 */
function getColorPalette(count) {
    const basePalette = [
        'rgba(52, 152, 219, 0.8)',  // Blue
        'rgba(155, 89, 182, 0.8)',   // Purple
        'rgba(52, 73, 94, 0.8)',    // Dark Blue
        'rgba(26, 188, 156, 0.8)',  // Green
        'rgba(241, 196, 15, 0.8)',  // Yellow
        'rgba(230, 126, 34, 0.8)',  // Orange
        'rgba(231, 76, 60, 0.8)',   // Red
        'rgba(149, 165, 166, 0.8)'  // Gray
    ];
    
    if (count <= basePalette.length) {
        return basePalette.slice(0, count);
    }
    
    // If we need more colors, repeat the palette
    const result = [];
    for (let i = 0; i < count; i++) {
        result.push(basePalette[i % basePalette.length]);
    }
    
    return result;
}

/**
 * Get status-specific colors
 * @returns {Object} Object with status colors
 */
function getStatusColors() {
    return {
        'Active': 'rgba(26, 188, 156, 0.8)',    // Green
        'Removed': 'rgba(231, 76, 60, 0.8)',    // Red
        'Replaced': 'rgba(241, 196, 15, 0.8)'   // Yellow
    };
}

/**
 * Refresh all charts with new data
 * @param {string} url - The API URL to fetch data from
 */
function refreshCharts(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Update charts with new data
            if (window.typeChart) {
                window.typeChart.data.labels = data.type_labels;
                window.typeChart.data.datasets[0].data = data.type_counts;
                window.typeChart.update();
            }
            
            if (window.statusChart) {
                window.statusChart.data.labels = data.status_labels;
                window.statusChart.data.datasets[0].data = data.status_counts;
                window.statusChart.update();
            }
            
            if (window.trendChart) {
                window.trendChart.data.labels = data.month_labels;
                window.trendChart.data.datasets[0].data = data.monthly_trend;
                window.trendChart.update();
            }
        })
        .catch(error => console.error('Error fetching chart data:', error));
}
