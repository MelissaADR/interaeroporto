from flask import Flask, render_template, request, session, redirect, url_for
import qrcode
import io

app = Flask(__name__)
app.secret_key = "chave-secreta"  # Necessário para usar sessão

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
    return render_template("reserva.html", nome=session.get("nome"), codigo=session.get("codigo"))

@app.route("/assentos", methods=["GET", "POST"])
def assentos():
    return render_template("assentos.html")

@app.route("/cartao", methods=["GET", "POST"])
def cartao():
    if request.method == "POST":
        session["assento"] = request.form.get("assento")

    # Obtendo os dados da sessão
    nome = session.get("nome")
    codigo = session.get("codigo")
    assento = session.get("assento")

    # --- NOVO: Colocando o código do QR Code AQUI DENTRO ---
    if nome and codigo and assento:
        # Dados do QR Code
        dados_qr = f"Passageiro: {nome}\nReserva: {codigo}\nAssento: {assento}"

        # Gerar QR Code em memória
        qr = qrcode.make(dados_qr)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        buf.seek(0)

        # Salvar imagem temporária
        qr_filename = "static/qrcode.png"
        with open(qr_filename, "wb") as f:
            f.write(buf.getbuffer())

        return render_template(
            "cartao.html",
            nome=nome,
            codigo=codigo,
            assento=assento,
            qr=qr_filename
        )
    else:
        # Redireciona de volta se os dados não estiverem na sessão
        return redirect(url_for('reserva'))

if __name__ == "__main__":
    app.run(debug=True)