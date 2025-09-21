from flask import Flask, render_template

app = Flask(__name__)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página de check-in
@app.route("/checkin")
def checkin():
    return render_template("checkin.html")

# Validação de reserva
@app.route("/reserva")
def reserva():
    return render_template("reserva.html")

# Escolha de assentos
@app.route("/assentos")
def assentos():
    return render_template("assentos.html")

# Confirmação e cartão de embarque
@app.route("/cartao")
def cartao():
    return render_template("cartao.html")


if __name__ == "__main__":
    app.run(debug=True)
