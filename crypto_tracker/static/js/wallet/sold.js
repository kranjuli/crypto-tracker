async function renderSoldCryptos() {
  const response = await fetch("/api/wallet/sold");
  const summary = await response.json();
  const tbody = document.querySelector('#cryptoTable tbody');
  tbody.innerHTML = '';

  summary.forEach(crypto => {
    const row = document.createElement('tr');
    tbody.appendChild(row);
    row.innerHTML = `
       <th scope="row">${crypto.crypto_name}</th>
       <td>${crypto.amount}</td>
       <td>${crypto.total_trade_price}</td>
       <td>${crypto.trade_date}</td>
       `;
  });
}

renderSoldCryptos();
