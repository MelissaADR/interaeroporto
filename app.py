from flask import Flask, render_template, request, session, redirect, url_for
import qrcode
import io

app = Flask(__name__)
app.secret_key = "chave-secreta"  # Necessário para usar sessão

# Lista de aeroportos fictícios
AEROPORTOS = ["Rua D.Abataiguara - 663 - Dirthmouth"]

# Assentos ocupados na sessão
def get_assentos_ocupados():
    if "ocupados" not in session:
        session["ocupados"] = []
    return session["ocupados"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkin")
def checkin():
    return render_template("checkin.html")

@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    if request.method == "POST":
        session["nome"] = request.form.get("nome")
        session["codigo"] = request.form.get("codigo")
        session["origem"] = request.form.get("origem")
        
    return render_template(
        "reserva.html",
        nome=session.get("nome"),
        codigo=session.get("codigo"),
        origem=session.get("origem"),
        aeroportos=AEROPORTOS
    )

@app.route("/assentos", methods=["GET", "POST"])
def assentos():
    ocupados = get_assentos_ocupados()
    return render_template("assentos.html", ocupados=ocupados)

@app.route("/cartao", methods=["GET", "POST"])
def cartao():
    if request.method == "POST":
        assento_escolhido = request.form.get("assento")
        ocupados = get_assentos_ocupados()

        # Marca o assento como ocupado
        if assento_escolhido and assento_escolhido not in ocupados:
            ocupados.append(assento_escolhido)
            session["ocupados"] = ocupados
            session["assento"] = assento_escolhido

    # Dados do passageiro
    nome = session.get("nome")
    codigo = session.get("codigo")
    assento = session.get("assento")
    origem = session.get("origem")
   

    if nome and codigo and assento and origem:
        # Conteúdo do QR Code
        dados_qr = (
            f"Passageiro: {nome}\n"
            f"Reserva: {codigo}\n"
            f"Assento: {assento}\n"
            f"Origem: {origem}\n"
        )

        # Gera QR Code em memória
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

if __name__ == "__main__":
    app.run(debug=True)
