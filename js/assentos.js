const mapaAssentos = document.getElementById("mapaAssentos");
const confirmarAssentoBtn = document.getElementById("confirmarAssento");

if (mapaAssentos) {
  for (let i = 1; i <= 30; i++) {
    const assento = document.createElement("div");
    assento.classList.add("assento");
    assento.textContent = i;

    assento.addEventListener("click", () => {
      document.querySelectorAll(".assento").forEach(a => a.classList.remove("selecionado"));
      assento.classList.add("selecionado");
      localStorage.setItem("assento", i);
    });

    mapaAssentos.appendChild(assento);
  }
}

if (confirmarAssentoBtn) {
  confirmarAssentoBtn.addEventListener("click", () => {
    if (localStorage.getItem("assento")) {
      alert("Assento confirmado! Vá para a página de confirmação.");
      window.location.href = "confirmacao.html";
    } else {
      alert("Selecione um assento antes de confirmar.");
    }
  });
}
