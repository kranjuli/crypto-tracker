async function fetchCurrentPrices(ids) {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${ids.join(',')}&vs_currencies=eur`;
  const response = await fetch(url);
  return await response.json();
}

async function renderBalance() {
  const response = await fetch("/api/wallet/balance");
  const cryptos = await response.json();
  const alias = cryptos.map(c => c.crypto_alias.toLowerCase());
  const prices = await fetchCurrentPrices(alias);
  const tbody = document.querySelector('#cryptoBalanceTable tbody');
  tbody.innerHTML = '';
  summary = 0;

  cryptos.forEach(crypto => {
    const currentPrice = prices[crypto.crypto_alias]?.eur || 0;
    const currentValue = currentPrice * crypto.remaining_amount;
    summary += currentValue;
    const amount = Math.round(crypto.remaining_amount * 1000) / 1000;
    const row = document.createElement('tr');
    tbody.appendChild(row);
    row.innerHTML = `
      <th scope="row">${crypto.crypto_name}</th>
      <td>${amount.toLocaleString('de-DE', { minimumFractionDigits: 4 })}</td>
      <td>${currentPrice.toLocaleString('de-DE', { minimumFractionDigits: 2 })}</td>
      <td>${currentValue.toLocaleString('de-DE', { minimumFractionDigits: 2 })}</td>
    `;
  });

  const summaryElement = document.getElementById('summary');
  if (summaryElement) {
    summaryElement.innerHTML = `Summary (€):  ${summary.toLocaleString('de-DE', { minimumFractionDigits: 2 })}`;
  }
}

renderBalance();
