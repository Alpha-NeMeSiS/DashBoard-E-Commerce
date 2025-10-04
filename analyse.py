import pandas as pd
import numpy as np

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


def tableaux_Kpi():
    top_clients_df = (df.groupby('Email')['Yearly Amount Spent'].sum().sort_values(ascending=False).head(10).reset_index().to_dict(orient='records'))
    clients_recents = (df.sort_values(by='Length of Membership', ascending=True).head(5)[['Email', 'Length of Membership']].to_dict(orient='records'))
    return {'top_clients' : top_clients_df, 'achat_recent' : clients_recents}

def graphique_top_clients(tableaux):
    top_clients = tableaux.get('top_clients', [])
    labels = [client['Email'] for client in top_clients]
    values = [round(client['Yearly Amount Spent'], 2) for client in top_clients]
    return labels, values

def analyse_all():

    kpis = template

    tableaux = tableaux_Kpi()

    return {'Kpis' : kpis, 'tableaux' : tableaux}