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

document.addEventListener("DOMContentLoaded", function() {
    const setDisplayButton = document.getElementById("set-display");
    const numPermitsInput = document.getElementById("num-permits");
    const historyTbody = document.getElementById("history-tbody");

    setDisplayButton.addEventListener("click", function() {
        const numPermits = parseInt(numPermitsInput.value, 10);
        const allRows = Array.from(historyTbody.querySelectorAll("tr"));
        
        allRows.forEach(row => row.style.display = "none");

        for (let i = 0; i < numPermits && i < allRows.length; i++) {
            allRows[i].style.display = "";
        }
    });

    setDisplayButton.click();
});