from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hotel_secret_key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

clients = []
reservations = []

offres = [
    {"nom": "Hotel Mazagan", "prix": "1800 MAD", "image": "offer1.png"},
    {"nom": "Suite Mazagan", "prix": "2400 MAD", "image": "offer2.png"},
    {"nom": "Chambre Premium", "prix": "2100 MAD", "image": "offer3.png"},
    {"nom": "Resort Family Room", "prix": "2600 MAD", "image": "offer4.png"}
]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        identifiant = request.form.get("identifiant")
        password = request.form.get("password")

        if identifiant == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin"))

        for client in clients:
            if client["email"] == identifiant and client["password"] == password:
                session.clear()
                session["client"] = client["email"]
                session["client_nom"] = client["nom"]
                return redirect(url_for("reservation"))

        return render_template("index.html", message="Email ou mot de passe incorrect")

    return render_template("index.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        password = request.form.get("password")

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
        destination = request.form.get("destination")
        arrivee = request.form.get("arrivee")
        depart = request.form.get("depart")
        personne = request.form.get("personne")

        if not destination or not arrivee or not depart or not personne:
            return render_template(
                "reservation.html",
                offres=offres,
                message="Tous les champs sont obligatoires"
            )

        reservation_data = {
            "nom": session["client_nom"],
            "destination": destination,
            "arrivee": arrivee,
            "depart": depart,
            "personne": personne
        }

        reservations.append(reservation_data)

        return render_template(
            "reservation.html",
            offres=offres,
            confirmation=reservation_data
        )

    return render_template("reservation.html", offres=offres)


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