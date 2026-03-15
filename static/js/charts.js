/**
 * Dashboard Charts
 * Chart.js configurations for analytics
 */

// Chart.js Default Configuration
Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
Chart.defaults.color = '#6B7280';

/**
 * Stock Trend Line Chart
 */
async function initStockTrendChart() {
    const canvas = document.getElementById('stockTrendChart');
    if (!canvas) return;

    try {
        const data = await Billico.fetchAPI('/api/analytics/trends');

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.data.map(d => new Date(d.date).toLocaleDateString()),
                datasets: [{
                    label: 'Stock Changes',
                    data: data.data.map(d => d.total_change),
                    borderColor: '#4F46E5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#4F46E5',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#F3F4F6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Stock trend chart error:', error);
    }
}

/**
 * Category Distribution Bar Chart
 */
async function initCategoryChart() {
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return;

    try {
        const data = await Billico.fetchAPI('/api/analytics/category-distribution');

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.data.map(d => d.category),
                datasets: [{
                    label: 'Items',
                    data: data.data.map(d => d.count),
                    backgroundColor: [
                        '#4F46E5',
                        '#10B981',
                        '#F59E0B',
                        '#EF4444',
                        '#3B82F6',
                        '#8B5CF6',
                        '#EC4899'
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        padding: 12,
                        callbacks: {
                            afterLabel: function (context) {
                                const item = data.data[context.dataIndex];
                                return [
                                    `Quantity: ${item.total_quantity}`,
                                    `Value: ${Billico.formatCurrency(item.total_value)}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#F3F4F6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Category chart error:', error);
    }
}

/**
 * Stock Health Pie Chart
 */
async function initStockHealthChart() {
    const canvas = document.getElementById('stockHealthChart');
    if (!canvas) return;

    try {
        const data = await Billico.fetchAPI('/api/analytics/stock-health');

        const statusColors = {
            'healthy': '#10B981',
            'medium': '#F59E0B',
            'low': '#EF4444',
            'out_of_stock': '#6B7280'
        };

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.data.map(d => d.status.replace('_', ' ').toUpperCase()),
                datasets: [{
                    data: data.data.map(d => d.count),
                    backgroundColor: data.data.map(d => statusColors[d.status]),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        padding: 12
                    }
                }
            }
        });
    } catch (error) {
        console.error('Stock health chart error:', error);
    }
}

/**
 * Initialize All Charts
 */
function initCharts() {
    initStockTrendChart();
    initCategoryChart();
    initStockHealthChart();
}

// Initialize charts on page load
document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.analytics-page') || document.querySelector('.dashboard-page')) {
        initCharts();
    }
});
