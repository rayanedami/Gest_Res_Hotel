from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hotel_secret_key"

# Compte admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Données
clients = []
reservations = []

chambres = [
    {"numero": 101, "type": "Simple", "prix": 300},
    {"numero": 102, "type": "Double", "prix": 500},
    {"numero": 103, "type": "Suite", "prix": 900},
    {"numero": 104, "type": "Familiale", "prix": 700}
]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        identifiant = request.form["identifiant"]
        password = request.form["password"]

        # Login admin
        if identifiant == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin"))

        # Login client avec email
        for client in clients:
            if client["email"] == identifiant and client["password"] == password:
                session.clear()
                session["client"] = client["email"]
                session["client_nom"] = client["nom"]
                return redirect(url_for("reservation"))

        return render_template("index.html", message="Identifiant ou mot de passe incorrect")

    return render_template("index.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        password = request.form["password"]

        if not nom or not email or not password:
            return render_template("sign_in.html", message="Tous les champs sont obligatoires")

        for client in clients:
            if client["email"] == email:
                return render_template("sign_in.html", message="Cet email existe déjà")

        clients.append({
            "nom": nom,
            "email": email,
            "password": password
        })

        return redirect(url_for("home"))

    return render_template("sign_in.html")


@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if "client" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        nom = session["client_nom"]
        chambre = request.form["chambre"]
        date = request.form["date"]

        if not date:
            return render_template(
                "reservation.html",
                chambres=chambres,
                message="La date est obligatoire"
            )

        for r in reservations:
            if r["chambre"] == chambre and r["date"] == date:
                return render_template(
                    "reservation.html",
                    chambres=chambres,
                    message="Cette chambre est déjà réservée pour cette date"
                )

        reservations.append({
            "nom": nom,
            "chambre": chambre,
            "date": date
        })

        return render_template(
            "reservation.html",
            chambres=chambres,
            message="Réservation enregistrée avec succès"
        )

    return render_template("reservation.html", chambres=chambres)


@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect(url_for("home"))

    return render_template("admin.html", reservations=reservations)


@app.route("/supprimer/<int:index>")
def supprimer(index):
    if "admin" not in session:
        return redirect(url_for("home"))

    if 0 <= index < len(reservations):
        reservations.pop(index)

    return redirect(url_for("admin"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)