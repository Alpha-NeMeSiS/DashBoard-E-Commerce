document.addEventListener('DOMContentLoaded', () => {
  const { segLabels, segCounts, segCAMoyen } = window.DASHBOARD_DATA || {};

  // Graph 1 : Nb clients par segment
  const ctx1 = document.getElementById('segCounts');
  if (ctx1) {
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: segLabels,
        datasets: [{ label: 'Nb clients', data: segCounts }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
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
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }

  // Graph 3 : Top client
  const ctx3 = document.getElementById('tableaux_Kpi');
  if (ctx2) {
    new Chart(ctx3, {
      type: 'bar',
      data: {
        labels: topClientsLabels,
        datasets: [{
          label: 'Montant dépensé (€)',
          data: topClientsValues,
          backgroundColor: '#008cffff', // couleurs des batons
          borderColor: '#dedee6ff',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: { color: '#ffffff' },
            title: {
              display: true,
              text: 'Montant (€)',
              color: '#ffffff'
            }
          },
          y: {
            ticks: { color: '#ffffff' },
            title: {
              display: true,
              text: 'Email',
              color: '#ffffff'
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