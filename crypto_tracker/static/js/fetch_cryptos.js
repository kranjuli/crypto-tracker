document.addEventListener("DOMContentLoaded", () => {
  const tbody = document.getElementById("crypto-list");

  fetch("/api/cryptos")
    .then((response) => response.json())
    .then((cryptos) => {
      tbody.innerHTML = ""; // Clear loading message

      if (cryptos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4">No purchases found.</td></tr>`;
        return;
      }

      cryptos.forEach(c => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${c.cryptoName}</td>
          <td>${c.purchaseDate}</td>
          <td>${c.pricePerCrypto}</td>
          <td>${c.amount}</td>
          <td>€${c.totalPriceEUR.toFixed(2)}</td>
        `;

        tbody.appendChild(row);
      });
    })
    .catch((err) => {
      tbody.innerHTML = `<tr><td colspan="4">Error loading data.</td></tr>`;
      console.error("Failed to fetch cryptos:", err);
    });
});
