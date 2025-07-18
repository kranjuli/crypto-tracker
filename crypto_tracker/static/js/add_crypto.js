document.getElementById('addCryptoForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const newEntry = Object.fromEntries(formData.entries());

  // Felder richtig konvertieren
  newEntry.amount = parseFloat(newEntry.amount);
  newEntry.totalPriceEUR = parseFloat(newEntry.totalPriceEUR);
  newEntry.cryptoName = newEntry.cryptoName.toLowerCase(); // für CoinGecko kompatibel

  const response = await fetch('/api/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newEntry)
  });

  if (response.ok) {
    alert('Kauf hinzugefügt!');
    form.reset();
    renderTable(); // neu laden
  } else {
    alert('Fehler beim Hinzufügen.');
  }
});
