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
function setModifica(numero, dataAttivazione, tipo, minutiResidui, creditoResiduo) {
  const modifyModal = new bootstrap.Modal(document.getElementById("Modify"));
  modifyModal.show();
  document.getElementById("modalNumero").textContent = numero;
  document.getElementById("modalDataAttivazione").textContent = dataAttivazione;
  document.getElementById("Tipo").value = tipo;
  document.getElementById("MinutiResidui").value = minutiResidui || '';
  document.getElementById("CreditoResiduo").value = creditoResiduo || '';
  document.getElementById("hiddenNumero").value = numero;
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


// Funzione per modificare il testo degli elementi <a> solo se la larghezza dello schermo è <= 768px
function modificaTestoMail() {
  var screenWidth = window.innerWidth; // Ottieni la larghezza dello schermo

  if (screenWidth <= 768) {
    var links = document.querySelectorAll(".mail-link"); // Seleziona tutti gli elementi <a> con la classe 'email-link'

    links.forEach(function (link) {
      var testoOriginale = link.textContent; // Salva il testo originale
      var nomeCognome = testoOriginale.split("@")[0]; // Ottieni solo il nome.cognome

      link.textContent = nomeCognome; // Modifica il testo dell'elemento <a> con nome.cognome
    });
  }
}

// Esegui la funzione al caricamento della pagina e al ridimensionamento della finestra
window.onload = modificaTestoMail;
window.onresize = modificaTestoMail;



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//metodi necessari per l'ordinamento di una tabella, data la posizione del campo da considerare(n), il tipo del dato del campo e l'id della tabella su cui si sta lavorando
function sortTable(n, type, tableID) {
  const table = document.getElementById(tableID);
  const rows = Array.from(table.rows).slice(1); // Ottengo tutte le righe tranne l'intestazione
  const dir = table.getAttribute("data-sort-dir") === "asc" ? "desc" : "asc";
  table.setAttribute("data-sort-dir", dir); // Cambio la direzione di ordinamento

  rows.sort((rowA, rowB) => {
    let x = rowA.getElementsByTagName("TD")[n].innerText;
    let y = rowB.getElementsByTagName("TD")[n].innerText;

    // Controllo se x o y contengono un tag <a>; in tal caso bisogna prendere il contenuto dell'elemento <a>
    if (rowA.getElementsByTagName("TD")[n].getElementsByTagName("a").length > 0) {
      x = rowA.getElementsByTagName("TD")[n].getElementsByTagName("a")[0].textContent;
    }
    if (rowB.getElementsByTagName("TD")[n].getElementsByTagName("a").length > 0) {
      y = rowB.getElementsByTagName("TD")[n].getElementsByTagName("a")[0].textContent;
    }

    return compareValues(x, y, type, dir);
  });

  // Rimuovo tutte le righe esistenti
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  // Aggiungo le righe ordinate nell'elemento <tbody>
  rows.forEach((row, index) => {
    table.getElementsByTagName("tbody")[0].appendChild(row);
  });
}

//metodo per passare da gg/mm/aaaa a aaaa/mm/gg
function parseDate(dateString) {
  const parts = dateString.split("/");
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // Mesi da 0 a 11
  const year = parseInt(parts[2], 10);
  return new Date(year, month, day);
}

//metodo che esegue il confronto fra due valori, in base al loro tipo e al criterio di ordinamento (asc/desc)
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
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////