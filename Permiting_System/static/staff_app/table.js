document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.querySelector('table tbody');

    function filterTable() {
        const filterValue = searchInput.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');

        Array.from(rows).forEach(row => {
            const cells = row.getElementsByTagName('td');
            let matchFound = false;

            Array.from(cells).forEach(cell => {
                if (cell.textContent.toLowerCase().includes(filterValue)) {
                    matchFound = true;
                }
            });

            if (matchFound) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('keyup', filterTable);
    document.getElementById('filterButton').addEventListener('click', filterTable);
});
