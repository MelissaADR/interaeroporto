const validarReservaBtn = document.getElementById("validarReserva");
const reservaMsg = document.getElementById("reservaMsg");

if (validarReservaBtn) {
  validarReservaBtn.addEventListener("click", () => {
    const codigo = document.getElementById("codigoReserva").value;

    if (codigo === "ABC123") {
      reservaMsg.textContent = "Reserva válida! Vá para a escolha de assento.";
      reservaMsg.style.color = "green";
    } else {
      reservaMsg.textContent = "Código de reserva inválido.";
      reservaMsg.style.color = "red";
    }
  });
}
