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
});
function refreshData() {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) overlay.classList.add("active");
  setTimeout(() => location.reload(), 500);
}

function exportData() {
  alert("Fonctionnalité d'export en cours de développement");
}