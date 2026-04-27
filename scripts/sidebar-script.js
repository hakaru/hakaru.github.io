(function() {
    var savedLang = localStorage.getItem('hakaru-lang');
    var activeLangButton = document.querySelector('.sidebar-lang-btn.active');
    var pageLang = activeLangButton ? activeLangButton.dataset.lang : 'en';

    function detectLang() {
        if (savedLang) return savedLang;
        var navLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
        if (navLang.startsWith('ja')) return 'ja';
        if (navLang.startsWith('fr')) return 'fr';
        if (navLang.startsWith('de')) return 'de';
        if (navLang.startsWith('es')) return 'es';
        if (navLang.startsWith('it')) return 'it';
        if (navLang.startsWith('ko')) return 'ko';
        if (navLang.startsWith('nl')) return 'nl';
        if (navLang === 'pt-br' || navLang.startsWith('pt')) return 'pt-BR';
        if (navLang.startsWith('sv')) return 'sv';
        if (navLang === 'zh-tw' || navLang === 'zh-hk' || navLang.startsWith('zh-hant')) {
            return 'zh-Hant';
        }
        if (navLang.startsWith('th')) return 'th';
        return 'en';
    }

    var userLang = detectLang();
    if (!savedLang && (!document.referrer || !document.referrer.includes('hakaru.net')) && pageLang !== userLang) {
        var langAlt = document.querySelector('.sidebar-lang-btn[data-lang="' + userLang + '"]');
        if (langAlt && langAlt.href) {
            window.location.href = langAlt.href;
            return;
        }
    }

    // Accordion
    document.querySelectorAll('.sidebar-app-header').forEach(function(header) {
        header.addEventListener('click', function() {
            var links = this.nextElementSibling;
            var wasExpanded = this.classList.contains('expanded');
            // Collapse all
            document.querySelectorAll('.sidebar-app-header').forEach(function(h) {
                h.classList.remove('expanded');
                if (h.nextElementSibling) h.nextElementSibling.classList.remove('show');
            });
            // Toggle clicked
            if (!wasExpanded) {
                this.classList.add('expanded');
                if (links) links.classList.add('show');
            }
        });
    });

    // Auto-expand current app
    var currentApp = document.querySelector('.sidebar-app-header.active');
    if (currentApp) {
        currentApp.classList.add('expanded');
        if (currentApp.nextElementSibling) {
            currentApp.nextElementSibling.classList.add('show');
        }
    }

    // Mobile toggle
    var toggle = document.querySelector('.sidebar-toggle');
    var sidebar = document.querySelector('.sidebar');
    var overlay = document.querySelector('.sidebar-overlay');
    if (toggle) {
        toggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('show');
        });
    }
    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
        });
    }

    // Language switch saves preference
    document.querySelectorAll('.sidebar-lang-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            localStorage.setItem('hakaru-lang', this.dataset.lang);
        });
    });
})();
