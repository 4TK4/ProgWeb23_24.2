function setEliminazione(numero) {
  const alertModal = new bootstrap.Modal(document.getElementById('Alert'));
  alertModal.show();

  const elimButton = document.getElementById('confirmDelete');

  const handleElimination = function () {
    alertModal.hide();
    window.location.replace(`/elimina_contratto/${numero}/`);
  };

  elimButton.addEventListener('click', handleElimination, { once: true });
}

function showHideFields() {
  const tipoContratto = document.getElementById("Tipo").value;
  const minutiResiduiGroup = document.getElementById("minutiResiduiGroup");
  const creditoResiduoGroup = document.getElementById("creditoResiduoGroup");
  if (tipoContratto === "a ricarica") {
    creditoResiduoGroup.style.display = "block"; 
    minutiResiduiGroup.style.display = "none"; 
  } else if (tipoContratto === "a consumo") {
    minutiResiduiGroup.style.display = "block"; 
    creditoResiduoGroup.style.display = "none"; 
  } else {
    minutiResiduiGroup.style.display = "none";
    creditoResiduoGroup.style.display = "none";
  }
}
function setModifica(numero, dataAttivazione, tipo, minutiResidui, creditoResiduo, contrattoId) {
  const modifyModal = new bootstrap.Modal(document.getElementById("Modify"));
  modifyModal.show();
  document.getElementById("modalNumero").textContent = numero;
  document.getElementById("modalDataAttivazione").textContent = dataAttivazione;
  document.getElementById("Tipo").value = tipo;
  document.getElementById("MinutiResidui").value = minutiResidui || '';
  document.getElementById("CreditoResiduo").value = creditoResiduo || '';
  showHideFields();
}

function controlloModifica() {
  const tipo = document.getElementById("Tipo").value;
  const minutiResidui = document.getElementById("MinutiResidui").value;
  const creditoResiduo = document.getElementById("CreditoResiduo").value;
  const contrattoId = document.getElementById("hiddenContrattoId").value;

  const tipoWarning = document.getElementById("tipoWarning");
  const minutiResiduiWarning = document.getElementById("minutiResiduiWarning");
  const creditoResiduoWarning = document.getElementById("creditoResiduoWarning");

  tipoWarning.style.display = "none";
  minutiResiduiWarning.style.display = "none";
  creditoResiduoWarning.style.display = "none";

  let isValid = true;
  if (!tipo) {
      tipoWarning.style.display = "block";
      isValid = false;
  }
  if (tipo === "a consumo" && !minutiResidui) {
      minutiResiduiWarning.style.display = "block";
      isValid = false;
  }
  if (tipo === "a ricarica" && !creditoResiduo) {
      creditoResiduoWarning.style.display = "block";
      isValid = false;
  }
  if (isValid) {
      const form = document.getElementById("updateForm");
      form.submit();
  }
}


function showHideFieldsInsert() {
  const tipoContratto = document.getElementById("Tipo2").value;
  const minutiResiduiGroup = document.getElementById("minutiResiduiGroup2");
  const creditoResiduoGroup = document.getElementById("creditoResiduoGroup2");
  if (tipoContratto === "a ricarica") {
    creditoResiduoGroup.style.display = "block"; 
    minutiResiduiGroup.style.display = "none"; 
  } else if (tipoContratto === "a consumo") {
    minutiResiduiGroup.style.display = "block";
    creditoResiduoGroup.style.display = "none"; 
  } else {
    minutiResiduiGroup.style.display = "none";
    creditoResiduoGroup.style.display = "none";
  }
}

function setInsert() {
  const insertModal = new bootstrap.Modal(document.getElementById("Insert"));
  insertModal.show();
}

function controlloInserimento() {
  const numero = document.getElementById("Numero2").value;
  const dataAttivazione = document.getElementById("DataAttivazione2").value;
  const tipo = document.getElementById("Tipo2").value;
  const minutiResidui = document.getElementById("MinutiResidui2").value;
  const creditoResiduo = document.getElementById("CreditoResiduo2").value;

  const numeroWarning = document.getElementById("numeroWarning");
  const dataAttivazioneWarning = document.getElementById("dataAttivazioneWarning2");
  const tipoWarning = document.getElementById("tipoWarning2");
  const minutiResiduiWarning = document.getElementById("minutiResiduiWarning2");
  const creditoResiduoWarning = document.getElementById("creditoResiduoWarning2");

  numeroWarning.style.display = "none";
  dataAttivazioneWarning.style.display = "none";
  tipoWarning.style.display = "none";
  minutiResiduiWarning.style.display = "none";
  creditoResiduoWarning.style.display = "none";

  let isValid = true;
  if (!numero) {
    numeroWarning.style.display = "block";
    isValid = false;
  }
  if (!dataAttivazione) {
    dataAttivazioneWarning.style.display = "block";
    isValid = false;
  }
  if (!tipo) {
    tipoWarning.style.display = "block";
    isValid = false;
  }
  if (tipo === "a consumo" && !minutiResidui) {
    minutiResiduiWarning.style.display = "block";
    isValid = false;
  }
  if (tipo === "a ricarica" && !creditoResiduo) {
    creditoResiduoWarning.style.display = "block";
    isValid = false;
  }
  if (isValid) {
    document.getElementById("createForm").submit();
  }
}

function sortTable(n, type, tableID) {
  const table = document.getElementById(tableID);
  const rows = Array.from(table.rows).slice(1); // Ottieni tutte le righe tranne l'intestazione
  const dir = table.getAttribute("data-sort-dir") === "asc" ? "desc" : "asc";
  table.setAttribute("data-sort-dir", dir); // Aggiorna la direzione di ordinamento

  rows.sort((rowA, rowB) => {
    let x = rowA.getElementsByTagName("TD")[n].innerText;
    let y = rowB.getElementsByTagName("TD")[n].innerText;

    // Controlla se x o y contengono un tag <a>
    if (rowA.getElementsByTagName("TD")[n].getElementsByTagName("a").length > 0) {
      x = rowA.getElementsByTagName("TD")[n].getElementsByTagName("a")[0].textContent;
    }
    if (rowB.getElementsByTagName("TD")[n].getElementsByTagName("a").length > 0) {
      y = rowB.getElementsByTagName("TD")[n].getElementsByTagName("a")[0].textContent;
    }

    return compareValues(x, y, type, dir);
  });

  // Rimuovi tutte le righe esistenti
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  // Aggiungi le righe ordinate
  rows.forEach((row, index) => {
    table.getElementsByTagName("tbody")[0].appendChild(row);
    // Assegna la classe in base all'indice
   /* if (index % 2 === 0) {
      row.className = "rowOdd";
    } else {
      row.className = "rowEven";
    }*/
  });
  refreshTable(tableID)
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

function refreshTable(tableID) {
  var table = document.getElementById(tableID);
  table.style.display = 'none'; // Nascondi la tabella
  table.offsetHeight; // Trigger reflow
  table.style.display = ''; // Mostra di nuovo la tabella
}
