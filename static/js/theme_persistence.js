(function () {
  function applyThemeClass(theme) {
    if (!theme) return;

    const body = document.body;
    const keptClasses = Array.from(body.classList).filter((cls) => !cls.startsWith('theme-'));
    body.className = keptClasses.join(' ').trim();
    body.classList.add(`theme-${theme}`);
  }

  function persistTheme(theme) {
    if (!theme) return;
    localStorage.setItem('selectedTheme', theme);
    applyThemeClass(theme);

    const dropdown = document.getElementById('themeDropdown');
    if (dropdown) {
      dropdown.classList.remove('show');
    }
  }

  window.changeTheme = persistTheme;
  window.selectTheme = persistTheme;

  document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('selectedTheme');
    if (savedTheme) {
      applyThemeClass(savedTheme);
    }
  });
})();
