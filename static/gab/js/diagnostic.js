document.addEventListener("DOMContentLoaded", () => {

    const componentCards = Array.from(
        document.querySelectorAll(".component-card")
    );

    function updatePanel(componentData) {

        const support = componentData.support_contact || {};

        // --------------------------
        // SUPPORT
        // --------------------------

        document.getElementById("dyn-sla").innerText =
            support.sla || "—";

        document.getElementById("dyn-vendor-logo").innerText =
            (support.support || "—").slice(0, 3).toUpperCase();

        document.getElementById("dyn-vendor").innerText =
            support.support || "—";

        document.getElementById("dyn-contact").innerText =
            support.responsable || "—";

        document.getElementById("dyn-resp").innerText =
            support.responsable || "—";

        document.getElementById("dyn-phone").innerText =
            support.telephone || "—";

        const email = document.getElementById("dyn-email");

        email.innerText = support.email || "—";
        email.href = support.email
            ? `mailto:${support.email}`
            : "#";

        document.getElementById("dyn-hours").innerText =
            support.heure_debut && support.heure_fin
                ? `${support.heure_debut} - ${support.heure_fin}`
                : "—";

        // --------------------------
        // DIAGNOSTIC
        // --------------------------

        document.getElementById("diag-comp-name").innerText =
            componentData.action ||
            componentData.component ||
            "—";

        document.getElementById("dyn-cause").innerText =
            componentData.cause || "—";

        document.getElementById("dyn-reco").innerText =
            componentData.recommendation || "—";

        // --------------------------
        // STYLE
        // --------------------------

        const wrapper = document.getElementById("diag-card-wrapper");
        const cause = document.getElementById("dyn-cause");
        const reco = document.getElementById("dyn-reco");
        const button = document.getElementById("diag-btn-container");

        wrapper.classList.remove("border-red-200", "bg-red-50", "border-orange-200", "bg-orange-50");
        cause.classList.remove("bg-red-50", "border-red-200", "text-red-700", "bg-orange-50", "border-orange-200", "text-orange-700", "bg-gray-50", "border-gray-200", "text-gray-700");
        reco.classList.remove("bg-red-50", "border-red-200", "text-red-700", "bg-green-50", "border-green-200", "text-green-700", "bg-orange-50", "border-orange-200", "text-orange-700", "bg-gray-50", "border-gray-200", "text-gray-700");
        button.classList.add("hidden");

        if (componentData.severity === "Critique") {

            wrapper.classList.add("border-red-200", "bg-red-50");

            cause.classList.add("bg-red-50", "border-red-200", "text-red-700");

            reco.classList.add("bg-green-50", "border-green-200", "text-green-700");

            if (componentData.status !== "Résolu") {
                button.classList.remove("hidden");
            }

        } else if (componentData.severity === "Moyenne") {

            wrapper.classList.add("border-orange-200", "bg-orange-50");

            cause.classList.add("bg-orange-50", "border-orange-200", "text-orange-700");

            reco.classList.add("bg-green-50", "border-green-200", "text-green-700");

        } else {

            wrapper.classList.add("border-gray-200");

            cause.classList.add("bg-gray-50", "border-gray-200", "text-gray-700");

            reco.classList.add("bg-gray-50", "border-gray-200", "text-gray-700");
        }
    }

    function selectComponent(componentKey) {

        componentCards.forEach(card => {
            card.classList.remove("active");
        });

        const selected = document.querySelector(
            `[data-component-key="${componentKey}"]`
        );

        if (selected) {
            selected.classList.add("active");
        }

        if (!diagnosticData || !diagnosticData.components) {
            return;
        }

        const component = diagnosticData.components.find(
            c => c.component === componentKey
        );

        if (component) {
            updatePanel(component);
        }
    }

    componentCards.forEach(card => {

        card.addEventListener("click", () => {

            selectComponent(
                card.dataset.componentKey
            );

        });

    });

    if (
        diagnosticData &&
        diagnosticData.components &&
        diagnosticData.components.length > 0
    ) {

        const initial =
            diagnosticData.selected_component ||
            diagnosticData.components[0].component;

        selectComponent(initial);

    }

    window.selectComponent = selectComponent;

});
