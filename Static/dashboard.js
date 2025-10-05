document.addEventListener('DOMContentLoaded', () => {
  const { segLabels = [], segCounts = [], segCAMoyen = [] } = window.DASHBOARD_DATA || {};

  // Graph 1 : Nb clients par segment
  const ctx1 = document.getElementById('segCounts');
  if (ctx1) {
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: segLabels,
        datasets: [{ label: 'Nb clients', data: segCounts }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        layout: { padding: 8 }
      }
    });
  }

  // Graph 2 : CA moyen par segment
  const ctx2 = document.getElementById('segCA');
  if (ctx2) {
    new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: segLabels,
        datasets: [{ label: 'CA moyen (€)', data: segCAMoyen }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        layout: { padding: 8 }
      }
    });
  }

  // Graph 3 : Top clients
  const ctx3 = document.getElementById('tableaux_Kpi');
  if (ctx3) {
    new Chart(ctx3, {
      type: 'bar',
      data: {
        labels: topClientsLabels,
        datasets: [{
          label: 'Montant dépensé (€)',
          data: topClientsValues,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,      // <-- ajouté
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        layout: { padding: 8 },          // <-- cohérence
        scales: {
          x: {
            beginAtZero: true,
            title: { display: true, text: 'Montant (€)' }
          },
          y: {
            title: { display: true, text: 'Email' }
          }
        }
      }
    });
  }

  // Graph 4 : Camembert CA par segment
  const ctxPie = document.getElementById('segmentPieChart');
  if (ctxPie) {
    new Chart(ctxPie, {
      type: 'pie',
      data: {
        labels: segmentLabels,
        datasets: [{
          label: 'CA total (€)',
          data: segmentCA,
          backgroundColor: ['#3D1FE6', '#1A0D99', '#6C5CE7', '#A29BFE'],
          borderColor: '#ffffff',
          borderWidth: 0.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,      // <-- ajouté
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#ffffff',          // <-- corrigé
              font: { size: 14 }
            }
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.label || '';
                const value = context.parsed || 0;
                return `${label}: ${value.toFixed(2)} €`;
              }
            }
          }
        }
      }
    });
  }
});

function refreshData() {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) overlay.classList.add("active");
  setTimeout(() => location.reload(), 500);
}

function exportData() {
  alert("Fonctionnalité d'export en cours de développement");
}
