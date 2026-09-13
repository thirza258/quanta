try {
  document.documentElement.dataset.theme = localStorage.getItem('quanta-theme') || 'light';
} catch {
  document.documentElement.dataset.theme = 'light';
}
