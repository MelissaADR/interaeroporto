const loginBtn = document.getElementById("loginBtn");
const loginModal = document.getElementById("loginModal");
const doLogin = document.getElementById("doLogin");

if (loginBtn) {
  loginBtn.addEventListener("click", () => {
    loginModal.style.display = "flex";
  });
}

if (doLogin) {
  doLogin.addEventListener("click", () => {
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;

    if (user && pass) {
      localStorage.setItem("user", user);
      alert("Login realizado com sucesso!");
      loginModal.style.display = "none";
    } else {
      alert("Preencha usuário e senha.");
    }
  });
}
