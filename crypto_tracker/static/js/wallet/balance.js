async function fetchCurrentPrices(ids) {
  if (ids.length === 0) return {};
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${ids.join(',')}&vs_currencies=eur`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Preise konnten nicht geladen werden: ${response.status}`);
  return await response.json();
}

async function renderBalance() {
  try {
    const response = await fetch("/api/wallet/balance");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const cryptos = await response.json();
    const alias = cryptos.map(c => c.crypto_alias.toLowerCase());
    const prices = await fetchCurrentPrices(alias);
    const tbody = document.querySelector('#cryptoBalanceTable tbody');
    tbody.innerHTML = '';
    let summary = 0;

    cryptos.forEach(crypto => {
      const currentPrice = prices[crypto.crypto_alias]?.eur || 0;
      const currentValue = currentPrice * crypto.remaining_amount;
      summary += currentValue;
      const amount = Math.round(crypto.remaining_amount * 1000) / 1000;
      const row = document.createElement('tr');
      row.innerHTML = `
        <th scope="row">${crypto.crypto_name}</th>
        <td>${amount.toLocaleString('de-DE', {minimumFractionDigits: 4, maximumFractionDigits: 4})}</td>
        <td>${currentPrice.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        <td>${currentValue.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
      `;
      tbody.appendChild(row);
    });

    const summaryElement = document.getElementById('summary');
    if (summaryElement) {
      summaryElement.textContent = `Summary (€):  ${summary.toLocaleString('de-DE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })}`;
    }
  } catch (error) {
    console.error('Fehler beim Laden der Balance:', error);
    // Optional: Nutzer informieren, z.B. eine Fehlermeldung anzeigen
  }
}

renderBalance();
