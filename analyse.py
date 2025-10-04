import pandas as pd
import numpy as np

data = pd.read_csv("Ecommerce_Customers.csv")
# Calculs des KPIs

def calcul_Kpi():
    kpis = {
        'ca_total': float(data['Yearly Amount Spent'].sum()),
        'ca_moyen': float(data['Yearly Amount Spent'].mean()),
        'ca_median': float(data['Yearly Amount Spent'].median()),
        'nb_clients': len(data),
        'anciennete_moyenne': float(data['Length of Membership'].mean()),
        'panier_moyen': float((data['Yearly Amount Spent'] /((data['Time on App'] + data['Time on Website']) /data['Avg. Session Length'])).mean()),
        'ltv_moyenne': float(data['Yearly Amount Spent'].mean() * data['Length of Membership'].mean()),
        'taux_retention_1an': float((data['Length of Membership'] > 1).sum() / len(data) * 100),
        'taux_retention_3ans': float((data['Length of Membership'] > 3).sum() / len(data) * 100),
    }
    return kpis


def tableaux_Kpi():
    top_clients_df = (data.groupby('Email')['Yearly Amount Spent'].sum().sort_values(ascending=False).head(10).reset_index().to_dict(orient='records'))
    clients_recents = (data.sort_values(by='Length of Membership', ascending=True).head(5)[['Email', 'Length of Membership']].to_dict(orient='records'))
    return {'top_clients' : top_clients_df, 'achat_recent' : clients_recents}

def graphique_top_clients(tableaux):
    top_clients = tableaux.get('top_clients', [])
    labels = [client['Email'] for client in top_clients]
    values = [round(client['Yearly Amount Spent'], 2) for client in top_clients]
    return labels, values   

def analyse_all():
    data = pd.read_csv("Ecommerce_Customers.csv")

    kpis = calcul_Kpi()

    tableaux = tableaux_Kpi()

    return {'Kpis' : kpis, 'tableaux' : tableaux}
