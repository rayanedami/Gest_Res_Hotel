from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

reservations = []

chambres = [
    {"numero": 101, "type": "Simple", "prix": 300},
    {"numero": 102, "type": "Double", "prix": 500},
    {"numero": 103, "type": "Suite", "prix": 900},
    {"numero": 104, "type": "Familiale", "prix": 700}
]

@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if request.method == "POST":
        nom = request.form["nom"]
        chambre = request.form["chambre"]
        date = request.form["date"]

        for r in reservations:
            if r["chambre"] == chambre:
                return render_template(
                    "reservation.html",
                    chambres=chambres,
                    message="cette chambre est deja reserve"
                )

        reservations.append({
            "nom": nom,
            "chambre": chambre,
            "date": date
        })

        return render_template(
            "reservation.html",
            chambres=chambres,
            message="Reservation enregistre avec succes"
        )

    return render_template("reservation.html", chambres=chambres)

@app.route("/liste")
def liste():
    return render_template("liste_reservations.html", reservations=reservations)

if __name__ == "__main__":
    app.run(debug=True)