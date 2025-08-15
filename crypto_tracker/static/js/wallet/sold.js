async function renderSoldCryptos() {
  try {
    const response = await fetch("/api/wallet/sold");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const summary = await response.json();
    const tbody = document.querySelector('#cryptoTable tbody');
    if (!tbody) {
      console.error('Kein tbody mit id #cryptoTable gefunden.');
      return;
    }
    tbody.innerHTML = '';
    if (summary.length === 0) {
      const row = document.createElement('tr');
      row.innerHTML = `<td colspan="4" class="text-center">No sold crypto found!</td>`;
      tbody.appendChild(row);
      return;
    }
    summary.forEach(crypto => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <th scope="row">${crypto.crypto_name}</th>
        <td>${Number(crypto.amount).toLocaleString('de-DE', { minimumFractionDigits: 4, maximumFractionDigits: 4 })}</td>
        <td>${Number(crypto.total_trade_price).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €</td>
        <td>${new Date(crypto.trade_date).toLocaleDateString('de-DE')}</td>
      `;
      tbody.appendChild(row);
    });
  } catch (error) {
    console.error('Fehler beim Laden der verkauften Kryptos:', error);
    // Optional: Fehlermeldung im UI anzeigen
  }
}

renderSoldCryptos();
