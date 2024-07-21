function setEliminazione(numero) {
    document.getElementById('Err').style.display = 'block';
  
    const elimButton = document.getElementById('eliminazione');
  
    const handleElimination = function () {
      document.getElementById('Err').style.display = 'none';
      window.location.replace("\elimina_contratto\\" + numero + "\\");
    };
  
    elimButton.addEventListener('click', handleElimination);
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("searchForm");
    var resetButton = document.getElementById("reset");
  
    resetButton.addEventListener("click", function () {
  
      var inputs = form.querySelectorAll('input[type="number"], input[type="date"], input[type="text"], input[type="checkbox"]');
      inputs.forEach(function (input) {
        input.value = "";
      });
  
      var checkboxes = form.querySelectorAll('input[type="checkbox"]');
      checkboxes.forEach(function (checkbox) {
        checkbox.checked = false;
      });
    });
  });