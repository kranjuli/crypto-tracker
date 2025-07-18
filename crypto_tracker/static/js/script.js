async function fetchCryptoData() {
  const response = await fetch('/api/cryptos');
  return await response.json();
}

async function fetchCurrentPrices(ids) {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${ids.join(',')}&vs_currencies=eur`;
  const response = await fetch(url);
  return await response.json();
}

async function renderTable() {
  const cryptos = await fetchCryptoData();
  const ids = cryptos.map(c => c.cryptoID.toLowerCase());
  const prices = await fetchCurrentPrices(ids);
  const tbody = document.querySelector('#cryptoTable tbody');
  tbody.innerHTML = '';

  cryptos.forEach(crypto => {
    const currentPrice = prices[crypto.cryptoID]?.eur || 0;
    const currentValue = currentPrice * crypto.amount;
    const gainLoss = currentValue - crypto.totalPurchasePrice;

    const row = document.createElement('tr');
    tbody.appendChild(row);
    const gainCss = 'text-success bg-success-subtle border border-success-subtle';
    const lossCss = 'text-danger bg-danger-subtle border border-danger-subtle';
    row.innerHTML = `
       <th scope="row">${crypto.cryptoName}</th>
       <td class="${gainLoss >= 0 ? gainCss : lossCss}">
         ${gainLoss.toFixed(2)}
       </td>
       <td>${crypto.meme ? currentPrice.toFixed(8) : currentPrice.toFixed(2)}</td>
       <td>${crypto.purchasePrice}</td>
       <td>${crypto.amount}</td>
       <td>${crypto.totalPurchasePrice.toFixed(2)}</td>
       <td>${currentValue.toFixed(2)}</td>
       <td>${crypto.purchaseDate}</td>
       <td>${crypto.broker}</td>
    `;
  });
}

renderTable();