
function setEliminazione(numero) {
  document.getElementById('Alert').style.display = 'block';

  const elimButton = document.getElementById('confirmDelete');

  const handleElimination = function () {
    document.getElementById('Alert').style.display = 'none';
    window.location.replace("\elimina_contratto\\" + numero + "\\");
  };

  elimButton.addEventListener('click', handleElimination);
}


// Ordinamento tabella in base al campo su cui si clicca
function sortTable(n, type, tableID) {
  const table = document.getElementById(tableID);
  const rows = Array.from(table.rows).slice(1); // Ottieni tutte le righe tranne l'intestazione
  const dir = table.getAttribute("data-sort-dir") === "asc" ? "desc" : "asc";
  table.setAttribute("data-sort-dir", dir);

  rows.sort((rowA, rowB) => {
      const x = getCellValue(rowA, n);
      const y = getCellValue(rowB, n);
      return compareValues(x, y, type, dir);
  });

  // Rimuovi tutte le righe esistenti (eccetto l'intestazione)
  while (table.rows.length > 1) {
      table.deleteRow(1);
  }

  // Aggiungi le righe ordinate
  rows.forEach(row => {
      table.appendChild(row);
  });
}

function getCellValue(row, index) {
  const cell = row.getElementsByTagName("TD")[index];
  // Se la cella contiene un link, ottieni il testo del link
  const link = cell.querySelector("a");
  return link ? link.innerText || link.textContent : cell.innerText || cell.textContent;
}

function compareValues(x, y, type, dir) {
  if (type === "num") {
      x = parseFloat(x);
      y = parseFloat(y);
  } else if (type === "date") {
      x = parseDate(x);
      y = parseDate(y);
  }
  if (dir === "asc") {
      return x > y ? 1 : x < y ? -1 : 0;
  } else {
      return x < y ? 1 : x > y ? -1 : 0;
  }
}

function parseDate(dateString) {
  // Assumiamo che il formato delle date sia gg/mm/aaaa
  const parts = dateString.split("/");
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // Mesi da 0 a 11
  const year = parseInt(parts[2], 10);
  return new Date(year, month, day);
}
