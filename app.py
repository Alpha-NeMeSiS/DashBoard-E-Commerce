from flask import Flask, render_template
import pandas as pd
import numpy as np
from analyse import analyse_all, graphique_top_clients,template,segment_labels,segment_values,segment_ca_moyen

app = Flask(__name__, static_folder='Static')

@app.route("/")
def index():
    analysis = analyse_all()
    tableaux = analysis["tableaux"]

    top_clients_labels = [client['Email'] for client in tableaux['top_clients']]
    top_clients_values = [round(client['Yearly Amount Spent'], 2) for client in tableaux['top_clients']]

    top_clients_labels, top_clients_values = graphique_top_clients(tableaux)
    
    return render_template(
        "dashboard.html",
        template=template,
        segment_labels=segment_labels,
        segment_values=segment_values,
        segment_ca_moyen=segment_ca_moyen,
        tableaux = analysis["tableaux"],
        top_clients_labels = top_clients_labels,
        top_clients_values = top_clients_values,
        other_labels=[],
        other_values=[]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
