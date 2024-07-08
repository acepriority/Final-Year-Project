const ctx = document.getElementById('chart');
    
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: {{labels|safe}},
        datasets: [{
        label: 'permits',
        data: {{data|safe}},
        borderWidth: 1
        }]
    },
    options: {
        maintainAspectRatio: false,
    }
    });