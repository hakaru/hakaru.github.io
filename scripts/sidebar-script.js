(function() {
    // Language auto-detection
    var savedLang = localStorage.getItem('hakaru-lang');
    var currentPath = window.location.pathname;

    function detectLang() {
        if (savedLang) return savedLang;
        var navLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
        return navLang.startsWith('ja') ? 'ja' : 'en';
    }

    function isJaPage() {
        return currentPath.includes('/index-ja') ||
               currentPath.includes('/privacy-ja') ||
               currentPath.includes('/changelog-ja') ||
               currentPath.includes('/manual/ja/') ||
               currentPath.includes('/blog/ja/') ||
               (currentPath.includes('/ChatArchive-support/') &&
                !currentPath.includes('/en/') &&
                !currentPath.includes('/th/') &&
                !currentPath.includes('/zh-Hant/'));
    }

    function getCurrentPageLang() {
        if (currentPath.includes('/th/')) return 'th';
        if (currentPath.includes('/zh-Hant/')) return 'zh-Hant';
        if (currentPath.includes('/en/') && currentPath.includes('/ChatArchive-support/')) return 'en';
        return isJaPage() ? 'ja' : 'en';
    }

    // Auto-redirect on first visit (no saved preference, not coming from same site)
    var pageLang = getCurrentPageLang();
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
