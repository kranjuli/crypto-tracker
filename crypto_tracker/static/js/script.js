async function fetchCryptoData() {
  const response = await fetch('/api/wallet/dashboard');
  return await response.json();
}

async function fetchCurrentPrices(ids) {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${ids.join(',')}&vs_currencies=eur`;
  const response = await fetch(url);
  return await response.json();
}

async function renderTable() {
  const cryptos = await fetchCryptoData();
  const alias = cryptos.map(c => c.crypto_alias.toLowerCase());
  const prices = await fetchCurrentPrices(alias);
  const tbody = document.querySelector('#cryptoDashBoardTable tbody');
  tbody.innerHTML = '';
  cryptos.forEach(crypto => {
    const currentPrice = prices[crypto.crypto_alias]?.eur || 0;
    const currentValue = currentPrice * crypto.amount;
    const gainLoss = currentValue - crypto.total_trade_price;
    const row = document.createElement('tr');
    tbody.appendChild(row);
    const gainCss = 'text-success bg-success-subtle border border-success-subtle';
    const lossCss = 'text-danger bg-danger-subtle border border-danger-subtle';
    row.innerHTML = `
      <th scope="row">${crypto.crypto_name}</th>
      <td>${crypto.type}</th>
      <td class="${gainLoss >= 0 ? gainCss : lossCss}">
        ${gainLoss.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
      </td>
      <td>${crypto.trade_price}</td>
      <td>${currentPrice.toFixed(4)}</td>
      <td>${crypto.amount.toLocaleString('de-DE', { minimumFractionDigits: 2 })}</td>
      <td>${crypto.total_trade_price.toLocaleString('de-DE', { minimumFractionDigits: 2 })}</td>
      <td>${currentValue.toLocaleString('de-DE', { minimumFractionDigits: 2 })}</td>
      <td>${crypto.trade_date}</td>
      <td>${crypto.broker}</td>
    `;
  });
}

renderTable();
