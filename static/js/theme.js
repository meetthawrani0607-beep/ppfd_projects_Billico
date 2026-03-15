/**
 * Theme Switcher
 * Handles dark/light mode toggling
 */

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function () {
    initializeTheme();
    setupThemeToggles();
});

/**
 * Initialize theme from localStorage or system preference
 */
function initializeTheme() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('billico-theme');

    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('billico-theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Set theme and update UI
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('billico-theme', theme);

    // Update all theme toggle buttons
    updateThemeToggles(theme);
}

/**
 * Toggle between light and dark theme
 */
function toggleTheme() {
    const currentTheme = localStorage.getItem('billico-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);

    // Optional: Add animation class
    document.body.classList.add('theme-transitioning');
    setTimeout(() => {
        document.body.classList.remove('theme-transitioning');
    }, 300);
}

/**
 * Setup all theme toggle buttons
 */
function setupThemeToggles() {
    // Setup toggle buttons in settings page
    const themeButtons = document.querySelectorAll('[data-theme-toggle]');
    themeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const requestedTheme = this.dataset.themeToggle;
            setTheme(requestedTheme);
        });
    });

    // Setup main theme toggle button (if exists)
    const mainToggle = document.getElementById('theme-toggle');
    if (mainToggle) {
        mainToggle.addEventListener('click', toggleTheme);
    }
}

/**
 * Update theme toggle button states
 */
function updateThemeToggles(theme) {
    const themeButtons = document.querySelectorAll('[data-theme-toggle]');
    themeButtons.forEach(button => {
        if (button.dataset.themeToggle === theme) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });

    // Update icon if main toggle exists
    const mainToggle = document.getElementById('theme-toggle');
    if (mainToggle) {
        const icon = mainToggle.querySelector('i');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        }
    }
}

/**
 * Get current theme
 */
function getCurrentTheme() {
    return localStorage.getItem('billico-theme') || 'light';
}
