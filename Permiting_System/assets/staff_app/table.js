document.getElementById('filterButton').addEventListener('click', filterCards);
document.getElementById('searchInput').addEventListener('keyup', filterCards);

function filterCards() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const cardName = card.getAttribute('data-name').toLowerCase();
        if (cardName.includes(searchInput)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}
