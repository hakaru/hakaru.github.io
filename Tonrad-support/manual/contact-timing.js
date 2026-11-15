// Educational upper-manual illustration. No audio, storage or app connection.
(function () {
    'use strict';
    document.querySelectorAll('[data-contact-demo]').forEach(function (demo) {
        const inputs = Array.from(demo.querySelectorAll('input[data-contact-param]'));
        const rows = Array.from(demo.querySelectorAll('[data-contact-position]'));
        const format = new Intl.NumberFormat(document.documentElement.lang, { maximumFractionDigits: 2 });

        function render() {
            const values = {};
            inputs.forEach(function (input) {
                const fallback = Number(input.defaultValue);
                const parsed = Number(input.value);
                const value = Math.min(Number(input.max), Math.max(Number(input.min), Number.isFinite(parsed) ? parsed : fallback));
                values[input.dataset.contactParam] = value;
                demo.querySelector('output[for="' + input.id + '"]').textContent = format.format(value);
            });
            const velocity = (values.velocity - 1) / 126;
            const spread = values.slow * Math.pow(values.fast / values.slow, Math.pow(velocity, values.curve));
            const limit = Math.max(values.slow, values.fast);
            demo.querySelector('[data-contact-total]').textContent = format.format(spread) + ' ms';
            demo.querySelector('[data-contact-axis-end]').textContent = format.format(limit) + ' ms';
            rows.forEach(function (row) {
                const time = Number(row.dataset.contactPosition) * spread;
                row.querySelector('.contact-marker').style.left = (100 * time / limit) + '%';
                row.querySelector('.contact-time-value').textContent = format.format(time) + ' ms';
            });
        }

        inputs.forEach(function (input) { input.addEventListener('input', render); });
        demo.querySelector('[data-contact-reset]').addEventListener('click', function () {
            inputs.forEach(function (input) { input.value = input.defaultValue; });
            render();
        });
        render();
        demo.hidden = false;
    });
})();
