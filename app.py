from flask import Flask, render_template, request, session, redirect, url_for
import qrcode
import io
import random

app = Flask(__name__)
app.secret_key = "chave-secreta"

# Lista de aeroportos fictícios
AEROPORTOS = ["Rua D.Abataiguara - 663 - Dirthmouth"]

# Banco de dados simulado de usuários
usuarios = {}

# Assentos ocupados na sessão
def get_assentos_ocupados():
    if "ocupados" not in session:
        session["ocupados"] = []
    return session["ocupados"]

# ===== ROTAS DE LOGIN/CADASTRO =====

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        if email in usuarios:
            return "Usuário já existe!"
        usuarios[email] = {"nome": nome, "email": email, "senha": senha, "otp": None}
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = usuarios.get(email)
        if usuario and usuario["senha"] == senha:
            otp = str(random.randint(100000, 999999))
            usuario["otp"] = otp
            session["email"] = email
            print(f"OTP para {email}: {otp}")  # Para testes
            return redirect(url_for("verificar_otp"))
        return "Email ou senha incorretos"
    return render_template("login.html")

@app.route("/verificar-otp", methods=["GET", "POST"])
def verificar_otp():
    if "email" not in session:
        return redirect(url_for("login"))
    email = session["email"]
    usuario = usuarios[email]

    if request.method == "POST":
        otp_digitado = request.form["otp"]
        if otp_digitado == usuario["otp"]:
            # Salva o nome do usuário logado na sessão
            session["nome"] = usuario["nome"]
            return redirect(url_for("perfil"))
        else:
            return "OTP incorreto!"
    return """
    <form method='post'>
        <label>Digite o OTP enviado:</label><br>
        <input type='text' name='otp'><br>
        <button type='submit'>Verificar</button>
    </form>
    """

@app.route("/perfil")
def perfil():
    if "email" not in session:
        return redirect(url_for("login"))
    email = session["email"]
    usuario = usuarios[email]
    return render_template("perfil.html", usuario=usuario)

# ===== ROTAS DO SITE DE CHECK-IN =====

@app.route("/")
def index():
    nome = session.get("nome", "")
    return render_template("index.html", nome=nome)

@app.route("/checkin")
def checkin():
    nome = session.get("nome", "")
    return render_template("checkin.html", nome=nome)

@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    if "nome" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        session["codigo"] = request.form.get("codigo")
        session["origem"] = request.form.get("origem")

    return render_template(
        "reserva.html",
        nome=session.get("nome"),  # Nome do login
        codigo=session.get("codigo"),
        origem=session.get("origem"),
        aeroportos=AEROPORTOS
    )


@app.route("/assentos", methods=["GET", "POST"])
def assentos():
    if "nome" not in session:
        return redirect(url_for("login"))
    ocupados = get_assentos_ocupados()
    return render_template("assentos.html", ocupados=ocupados, nome=session.get("nome"))

@app.route("/cartao", methods=["GET", "POST"])
def cartao():
    if "nome" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        assento_escolhido = request.form.get("assento")
        ocupados = get_assentos_ocupados()
        if assento_escolhido and assento_escolhido not in ocupados:
            ocupados.append(assento_escolhido)
            session["ocupados"] = ocupados
            session["assento"] = assento_escolhido

    nome = session.get("nome")
    codigo = session.get("codigo")
    assento = session.get("assento")
    origem = session.get("origem")

    if nome and codigo and assento and origem:
        dados_qr = (
            f"Passageiro: {nome}\n"
            f"Reserva: {codigo}\n"
            f"Assento: {assento}\n"
            f"Origem: {origem}\n"
        )
        qr = qrcode.make(dados_qr)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        buf.seek(0)
        qr_filename = "static/qrcode.png"
        with open(qr_filename, "wb") as f:
            f.write(buf.getbuffer())

        return render_template(
            "cartao.html",
            nome=nome,
            codigo=codigo,
            assento=assento,
            origem=origem,
            qr=qr_filename
        )
    else:
        return redirect(url_for('reserva'))
    
@app.route("/logout")
def logout():
    # Remove os dados do usuário da sessão
    session.pop("email", None)
    session.pop("nome", None)
    # Opcional: limpar assentos e código se quiser
    # session.pop("assento", None)
    # session.pop("codigo", None)
    return redirect(url_for("login"))


# ===== RODAR APP =====
if __name__ == "__main__":
    app.run(debug=True)
