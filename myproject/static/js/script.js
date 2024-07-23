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
  showHideFields();
}