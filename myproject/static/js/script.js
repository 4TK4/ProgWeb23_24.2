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