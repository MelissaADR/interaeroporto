const nomePassageiro = document.getElementById("nomePassageiro");
const assentoSelecionado = document.getElementById("assentoSelecionado");

if (nomePassageiro && assentoSelecionado) {
  nomePassageiro.textContent = localStorage.getItem("user") || "Passageiro";
  assentoSelecionado.textContent = localStorage.getItem("assento") || "Não selecionado";
}
