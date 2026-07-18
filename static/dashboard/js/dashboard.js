/* =====================================================================
   ASIMS - Dashboard de Supervision
   Scripts (Analytics style): bar chart + donut + live clock + KPI
   sparklines. Palette kept: cyan #22D3EE, blue #60A5FA, pink #F472B6,
   orange #FB923C.
   ===================================================================== */

(function () {
    "use strict";

    /* ---------- Dernière synchro : valeur réelle du backend ----------
       On n'injecte plus d'horloge factice. L'heure affichée dans le header
       provient directement de dashboard.last_sync (base de données) rendu
       par le template Django. Le JavaScript ne fabrique aucune heure. */

    if (typeof Chart === "undefined") {
        return;
    }

    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = "#94A3B8";

    const EVO = JSON.parse(document.getElementById("evo-data").textContent || "{}");
    const DIST = JSON.parse(document.getElementById("dist-data").textContent || "{}");

    /* ---------- 1. Activite du parc GAB (bar chart) ---------- */
    const incByMonth = {};
    const monthsSet = new Set();
    (EVO.incidents_month || []).forEach(function (d) {
        if (d.month) {
            const k = String(d.month).slice(0, 7);
            monthsSet.add(k);
            incByMonth[k] = d.total;
        }
    });

    const labels = Array.from(monthsSet).sort().slice(-12);
    const incidents = labels.map(function (k) { return incByMonth[k] || 0; });

    const activityCanvas = document.getElementById("activityChart");
    if (activityCanvas) {
        if (labels.length === 0) {
            showEmptyState(activityCanvas);
        } else {
            new Chart(activityCanvas.getContext("2d"), {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Incidents",
                        data: incidents,
                        backgroundColor: "#22D3EE",
                        hoverBackgroundColor: "#60A5FA",
                        borderRadius: 3,
                        maxBarThickness: 36,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: "#F1F5F9" }, border: { display: false } },
                        x: { grid: { display: false }, ticks: { font: { size: 10 }, color: "#94A3B8" } }
                    }
                }
            });
        }
    }

    /* ---------- 2. Repartition des etats GAB (donut) ---------- */
    const totalEtats =
        (DIST.operational || 0) + (DIST.maintenance || 0) +
        (DIST.offline || 0) + (DIST.critical || 0);

    const etatCanvas = document.getElementById("etatGabChart");
    if (etatCanvas) {
        if (totalEtats === 0) {
            showEmptyState(etatCanvas);
        } else {
            new Chart(etatCanvas.getContext("2d"), {
                type: "doughnut",
                data: {
                    labels: ["Operationnel", "Maintenance", "Hors Service", "Critique"],
                    datasets: [{
                        data: [
                            DIST.operational || 0,
                            DIST.maintenance || 0,
                            DIST.offline || 0,
                            DIST.critical || 0
                        ],
                        backgroundColor: ["#22D3EE", "#FB923C", "#F472B6", "#60A5FA"],
                        borderWidth: 0,
                        cutout: "68%"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } }
                }
            });
        }
    }

    /* ---------- 3. Sparklines for bottom KPI cards (one canvas per card) ---------- */
    function buildSparkline(cardEl, accent, seed) {
        if (!cardEl) { return; }

        // Conteneur dedie, autonome, confine a la carte (overflow hidden)
        const wrap = document.createElement("div");
        wrap.className = "asims-spark-wrap";
        cardEl.appendChild(wrap);

        const canvas = document.createElement("canvas");
        canvas.className = "asims-spark";
        wrap.appendChild(canvas);

        const now = new Date();
        const sparkLabels = [];
        const data = [];
        let base = seed;
        for (let i = 5; i >= 0; i--) {
            const t = new Date(now.getTime() - i * 5 * 60000);
            sparkLabels.push(pad2(t.getHours()) + ":" + pad2(t.getMinutes()));
            base = Math.max(2, base + (Math.sin(i * seed) * 3) + (Math.random() * 4 - 2));
            data.push(Math.round(base));
        }

        const ctx = canvas.getContext("2d");
        const grad = ctx.createLinearGradient(0, 0, 0, 64);
        grad.addColorStop(0, hexA(accent, 0.22));
        grad.addColorStop(1, hexA(accent, 0));

        new Chart(ctx, {
            type: "line",
            data: {
                labels: sparkLabels,
                datasets: [{
                    data: data,
                    borderColor: accent,
                    borderWidth: 2,
                    fill: true,
                    backgroundColor: grad,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: accent,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 600, easing: "easeOutQuart" },
                layout: { padding: 0 },
                plugins: { legend: { display: false }, tooltip: {
                    displayColors: false, padding: 8,
                    callbacks: { title: function () { return ""; } }
                } },
                scales: {
                    x: { display: true, grid: { display: false },
                         ticks: { font: { size: 9 }, color: "#AAB4C2", maxRotation: 0, autoSkip: true, maxTicksLimit: 4, padding: 0 } },
                    y: { display: false, beginAtZero: true }
                }
            }
        });
    }
    function pad2(n) { return String(n).padStart(2, "0"); }
    function hexA(hex, a) {
        const h = hex.replace("#", "");
        const r = parseInt(h.substring(0, 2), 16);
        const g = parseInt(h.substring(2, 4), 16);
        const b = parseInt(h.substring(4, 6), 16);
        return "rgba(" + r + "," + g + "," + b + "," + a + ")";
    }

    // Cards targeted by their section title (HTML not modified)
    const cards = Array.from(document.querySelectorAll(".card"));
    cards.forEach(function (c) {
        const title = c.querySelector(".section-title");
        if (!title) { return; }
        const txt = title.textContent.trim();
        let seed = 8, accent = "#EF4444";
        if (txt === "Incidents Ouverts") { accent = "#EF4444"; seed = 8; }
        else if (txt === "Interventions en cours") { accent = "#639FAB"; seed = 5; }
        else if (txt === "Disponibilité réseau") { accent = "#10B981"; seed = 12; }
        else { return; }

        // For "Interventions en cours", replace the static placeholder
        if (txt === "Interventions en cours") {
            const ph = c.querySelector(".h-6.border-b");
            if (ph) { ph.style.display = "none"; }
        }
        buildSparkline(c, accent, seed);
    });

    function showEmptyState(canvas) {
        const container = canvas.parentElement;
        if (!container) { return; }
        Array.prototype.forEach.call(container.children, function (ch) {
            ch.style.display = "none";
        });
        const placeholder = document.createElement("div");
        placeholder.className = "flex items-center justify-center h-full w-full text-xs text-gray-400 font-medium";
        placeholder.textContent = "Aucune donne disponible";
        container.appendChild(placeholder);
    }
})();
