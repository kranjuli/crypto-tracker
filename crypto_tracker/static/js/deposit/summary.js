async function renderDeposit() {
  const response = await fetch("/api/deposit/summary");
  const deposit = await response.json();
  const tbody = document.querySelector('#cryptoDepositTable tbody');
  tbody.innerHTML = '';

  for (let i = 0; i < deposit.length && i < 10; i++) {
    const item = deposit[i];
    const row = document.createElement('tr');
    tbody.appendChild(row);
    row.innerHTML = `
      <th scope="row">${item.date}</th>
      <td>${item.amount}</td>
      <td>${item.broker}</td>
      <td>${item.method}</td>
    `;
  }
}

renderDeposit();
