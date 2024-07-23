
function setEliminazione(numero) {
  document.getElementById('Alert').style.display = 'block';

  const elimButton = document.getElementById('confirmDelete');

  const handleElimination = function () {
    document.getElementById('Alert').style.display = 'none';
    window.location.replace("\elimina_contratto\\" + numero + "\\");
  };

  elimButton.addEventListener('click', handleElimination);
}

function setModifica(numero, dataAttivazione) {
  // Mostra il modale
  document.getElementById('Modify').style.display = 'block';

  // Popola i campi del modale con i dati esistenti
  document.getElementById('modalNumero').value = numero;
  document.getElementById('modalDataAttivazione').value = dataAttivazione;

  const updateButton = document.getElementById('confirmUpdate');

  const handleUpdate = function () {
    // Prepara i dati aggiornati
    const updatedNumero = document.getElementById('modalNumero').value;
    const updatedDataAttivazione = document.getElementById('modalDataAttivazione').value;
    const updatedTipo = document.getElementById('modalTipo').value;
    const updatedCreditoResiduo = document.getElementById('modalCreditoResiduo').value;
    const updatedMinutiResidui = document.getElementById('modalMinutiResidui').value;

    // Nasconde il modale
    document.getElementById('Modify').style.display = 'none';

    // Invia la richiesta di aggiornamento
    fetch('/modifica_contratto/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        Numero: updatedNumero,
        DataAttivazione: updatedDataAttivazione,
        Tipo: updatedTipo,
        CreditoResiduo: updatedCreditoResiduo,
        MinutiResidui: updatedMinutiResidui
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert('Errore durante l\'aggiornamento del contratto');
      }
    });
  };

  updateButton.removeEventListener('click', handleUpdate);
  updateButton.addEventListener('click', handleUpdate);
}

// Funzione per ottenere il CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
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
