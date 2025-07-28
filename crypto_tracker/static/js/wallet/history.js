async function renderTradeHistory() {
  const response = await fetch("/api/wallet/history");
  const summary = await response.json();
  const tbody = document.querySelector('#cryptoTable tbody');
  tbody.innerHTML = '';

  summary.forEach(crypto => {
    const row = document.createElement('tr');
    tbody.appendChild(row);
    row.innerHTML = `
      <th class="${crypto.type == 'buy' ? 'text-success' : 'text-danger'}" scope="row">${crypto.crypto_name}</th>
      <td>${crypto.type}</td>
      <td>${crypto.amount}</td>
      <td>${crypto.total_trade_price}</td>
      <td>${crypto.trade_price}</td>
      <td>${crypto.trade_date}</td>
      <td>${crypto.broker}</td>
    `;
  });
}

renderTradeHistory();
