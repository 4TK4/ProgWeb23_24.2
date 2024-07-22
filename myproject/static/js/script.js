function setEliminazione(numero) {
    document.getElementById('Alert').style.display = 'block';
  
    const elimButton = document.getElementById('confirmDelete');
  
    const handleElimination = function () {
      document.getElementById('Alert').style.display = 'none';
      window.location.replace("\elimina_contratto\\" + numero + "\\");
    };
  
    elimButton.addEventListener('click', handleElimination);
  }