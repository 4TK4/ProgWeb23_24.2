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
  document.getElementById("hiddenContrattoId").value = contrattoId;
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
      form.action = `/modifica_contratto/${contrattoId}/`;
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