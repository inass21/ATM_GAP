document.addEventListener('DOMContentLoaded', () => {
    const componentCards = Array.from(document.querySelectorAll('.component-card'));
    const initialComponent = componentCards[0];

    const updatePanel = (componentData) => {
        document.getElementById('dyn-sla').innerText = componentData.support.sla || '—';
        document.getElementById('dyn-vendor-logo').innerText = (componentData.support.vendor || '—').slice(0, 3).toUpperCase();
        document.getElementById('dyn-vendor').innerText = componentData.support.vendor || '—';
        document.getElementById('dyn-contact').innerText = componentData.support.responsable || '—';
        document.getElementById('dyn-resp').innerText = componentData.support.responsable || '—';
        document.getElementById('dyn-phone').innerText = componentData.support.telephone || '—';
        document.getElementById('dyn-email').innerText = componentData.support.email || '—';
        document.getElementById('dyn-email').href = componentData.support.email ? `mailto:${componentData.support.email}` : 'mailto:';
        document.getElementById('dyn-hours').innerText = componentData.support.hours || '—';

        document.getElementById('diag-comp-name').innerText = componentData.name || '—';
        document.getElementById('dyn-cause').innerText = componentData.cause || '—';
        document.getElementById('dyn-reco').innerText = componentData.recommendation || '—';

        const wrapper = document.getElementById('diag-card-wrapper');
        const causeEl = document.getElementById('dyn-cause');
        const recoEl = document.getElementById('dyn-reco');
        const buttonContainer = document.getElementById('diag-btn-container');

        if (componentData.severity === 'Critique' || componentData.status === 'En panne' || componentData.status === 'À traiter') {
            wrapper.className = 'bg-red-50/20 border border-red-100 rounded-xl p-5 shadow-sm flex-1 flex flex-col justify-between transition-colors duration-300';
            causeEl.className = 'text-sm font-medium text-red-800 leading-snug bg-red-50 p-3 rounded-lg border border-red-100 shadow-inner transition-colors';
            recoEl.className = 'text-sm font-medium text-green-800 leading-snug bg-green-50 p-3 rounded-lg border border-green-100 shadow-inner transition-colors';
            buttonContainer.classList.remove('hidden');
        } else if (componentData.severity === 'Moyenne' || componentData.status === 'Attention') {
            wrapper.className = 'bg-orange-50/20 border border-orange-100 rounded-xl p-5 shadow-sm flex-1 flex flex-col justify-between transition-colors duration-300';
            causeEl.className = 'text-sm font-medium text-orange-800 leading-snug bg-orange-50 p-3 rounded-lg border border-orange-100 shadow-inner transition-colors';
            recoEl.className = 'text-sm font-medium text-green-800 leading-snug bg-green-50 p-3 rounded-lg border border-green-100 shadow-inner transition-colors';
            buttonContainer.classList.add('hidden');
        } else {
            wrapper.className = 'bg-white border border-borderGray rounded-xl p-5 shadow-sm flex-1 flex flex-col justify-between transition-colors duration-300';
            causeEl.className = 'text-sm font-medium text-gray-700 leading-snug bg-gray-50 p-3 rounded-lg border border-gray-200 shadow-inner transition-colors';
            recoEl.className = 'text-sm font-medium text-gray-700 leading-snug bg-gray-50 p-3 rounded-lg border border-gray-200 shadow-inner transition-colors';
            buttonContainer.classList.add('hidden');
        }
    };

    const selectComponent = (componentKey) => {
        componentCards.forEach((card) => card.classList.remove('active'));
        const selectedCard = document.querySelector(`[data-component-key="${componentKey}"]`);
        if (selectedCard) {
            selectedCard.classList.add('active');
        }

        const data = diagnosticData.components.find((item) => item.component === componentKey);
        if (data) {
            updatePanel(data);
        }
    };

    componentCards.forEach((card) => {
        card.addEventListener('click', () => selectComponent(card.dataset.componentKey));
    });

    if (diagnosticData.components && diagnosticData.components.length) {
        const firstKey = diagnosticData.components[0].component;
        selectComponent(firstKey);
    } else if (initialComponent) {
        selectComponent(initialComponent.dataset.componentKey);
    }

    window.selectComponent = selectComponent;
});
