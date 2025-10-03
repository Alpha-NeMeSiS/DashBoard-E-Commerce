from flask import Flask, render_template
import pandas as pd
import numpy as np
from analyse import analyse_all, graphique_top_clients

app = Flask(__name__, static_folder='Static')

df = pd.read_csv("Ecommerce_Customers.csv")

# 1) Yearly Amount Spent (YAS)
yas = df['Yearly Amount Spent']
yas_mean   = round(float(yas.mean()), 2)
yas_median = round(float(yas.median()), 2)
yas_std    = round(float(yas.std()), 2)

# 2) Valeurs manquantes
missing_counts = df.isna().sum()
missing_any = bool(missing_counts.sum() > 0)

# 3) Chiffre d'affaires (CA)
ca_total  = round(float(yas.sum()), 2)
ca_var    = round(float(yas.var()), 2)
ca_std    = yas_std
ca_moyen  = yas_mean
ca_med    = yas_median

# 4) Sessions estimées & panier moyen
total_time = df['Time on App'] + df['Time on Website']
avg_len = df['Avg. Session Length'].replace(0, np.nan)
n_sessions = (total_time / avg_len).replace([np.inf, -np.inf], np.nan)

panier_moyen_series = yas / n_sessions
panier_moyen_mean   = round(float(panier_moyen_series.mean()), 2)
panier_moyen_median = round(float(panier_moyen_series.median()), 2)
sessions_mean       = round(float(n_sessions.mean()), 2)
sessions_median     = round(float(n_sessions.median()), 2)

# 5) Segmentation par ancienneté
anciennete = df['Length of Membership']
bins = [0, 1, 3, 5, float(anciennete.max()) + 1e-9]
labels = ['Nouveau (<1 an)', 'Récent (1-3 ans)', 'Fidèle (3-5 ans)', 'Très fidèle (>5 ans)']
df['Segment_Anciennete'] = pd.cut(
    anciennete, bins=bins, labels=labels, right=False, include_lowest=True
)

segment_counts = df['Segment_Anciennete'].value_counts().sort_index()
ca_par_segment = (
    df.groupby('Segment_Anciennete', observed=False)['Yearly Amount Spent']
      .agg(['mean', 'median', 'count'])
      .rename(columns={'mean': 'CA moyen', 'median': 'CA médian', 'count': 'Nb clients'})
)

# df['Length of Membership'] = pd.to_datetime(df['Length of Membership'])
 
# ca_actuel = df[df['Length of Membership'].dt.year == 2025]['Yearly Amount Spent'].sum()
# ca_precedent = df[df['Length of Membership'].dt.year == 2024]['Yearly Amount Spent'].sum()
 
# evolution_ca = ((ca_actuel - ca_precedent) / ca_precedent) * 100 if ca_precedent != 0 else 0

ltv_value = float(df['Yearly Amount Spent'].mean() *df['Length of Membership'].mean())

# Structures passées au template
template = {
    # 'evolution_ca':    f"{evolution_ca:,.0f}",
    'ltv_moyenne':     f"{ltv_value:,.0f}",
    'nb_clients':      len(df),
    "ca_total":        f"{ca_total:,.0f} €",
    "ca_moyen":        f"{ca_moyen:.2f} €",
    "ca_median":       f"{ca_med:.2f} €",
    "ca_var":          f"{ca_var:.2f}",
    "ca_std":          f"{ca_std:.2f} €",
    "yas_mean":        f"{yas_mean:.2f} €",
    "yas_median":      f"{yas_median:.2f} €",
    "yas_std":         f"{yas_std:.2f} €",
    "panier_mean":     f"{panier_moyen_mean:.2f} €",
    "panier_median":   f"{panier_moyen_median:.2f} €",
    "sessions_mean":   f"{sessions_mean:.2f}",
    "sessions_median": f"{sessions_median:.2f}",
    "missing_any":     "Oui" if missing_any else "Non"
}

segment_labels   = list(segment_counts.index.astype(str))
segment_values   = [int(v) for v in segment_counts.values]
segment_ca_moyen = [round(float(v), 2) for v in ca_par_segment['CA moyen'].values]

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

