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