let currentPage = 1;
let pageSize = 25;

document.getElementById("pageSize").addEventListener("change", (e) => {
    pageSize = parseInt(e.target.value);
    currentPage = 1;
    loadTrades();
});

async function loadTrades(page = currentPage) {
    currentPage = page;

    const response = await fetch(
        `/api/wallet/trades?page=${currentPage}&page_size=${pageSize}`
    );

    const data = await response.json();

    renderTable(data.trades);
    renderPagination(data.meta);
}

function renderTable(trades) {
    const tbody = document.getElementById("tradeTableBody");
    tbody.innerHTML = "";

    if (trades.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted">
                    Keine Trades gefunden
                </td>
            </tr>`;
        return;
    }

    trades.forEach(trade => {
        tbody.insertAdjacentHTML("beforeend", `
            <tr>
                <td>${trade.id}</td>
                <td>${trade.crypto_name}</td>
                <td>${trade.crypto_alias}</td>
                <td>
                    <span class="badge ${trade.type === "buy" ? "bg-success" : "bg-danger"}">
                        ${trade.type}
                    </span>
                </td>
                <td>${trade.amount}</td>
                <td>${trade.trade_price}</td>
                <td>${trade.total_trade_price}</td>
                <td>${trade.trade_date}</td>
                <td>${trade.broker}</td>
                <td>${trade.meme}</td>
            </tr>
        `);
    });
}

function renderPagination(meta) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    // Previous
    pagination.insertAdjacentHTML("beforeend", `
        <li class="page-item ${!meta.has_previous ? "disabled" : ""}">
            <a class="page-link" href="#" onclick="loadTrades(${meta.current_page - 1})">
                ←
            </a>
        </li>
    `);

    // Page numbers
    const start = Math.max(1, meta.current_page - 2);
    const end = Math.min(meta.total_pages, meta.current_page + 2);

    for (let p = start; p <= end; p++) {
        pagination.insertAdjacentHTML("beforeend", `
            <li class="page-item ${p === meta.current_page ? "active" : ""}">
                <a class="page-link" href="#" onclick="loadTrades(${p})">
                    ${p}
                </a>
            </li>
        `);
    }

    // Next
    pagination.insertAdjacentHTML("beforeend", `
        <li class="page-item ${!meta.has_next ? "disabled" : ""}">
            <a class="page-link" href="#" onclick="loadTrades(${meta.current_page + 1})">
                →
            </a>
        </li>
    `);
}

// Initial load
loadTrades();
