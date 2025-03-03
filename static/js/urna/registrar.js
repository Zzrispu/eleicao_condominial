document.addEventListener('DOMContentLoaded', () => {
    const cUnregistered = document.getElementById('c-unregistered');
    const cRegistered = document.getElementById('c-registered');

    const aUnregistered = document.getElementById('a-unregistered');
    const aRegistered = document.getElementById('a-registered');

    const cSwapBtn = document.getElementById('c-swap-btn');
    const aSwapBtn = document.getElementById('a-swap-btn');

    // const cSaveBtn = document.getElementById('c-save-btn');
    // const aSaveBtn = document.getElementById('a-save-btn');

    async function updateCadidatos() {
        const unrList = []
        const rList = []

        await fetch('/api/get_candidatos')
            .then(response => response.json())
            .then((data) => {
                data.forEach(candidato => {
                    const option = document.createElement('option');
                    option.innerHTML = candidato.nome;

                    if (candidato.numero == 0) unrList.push(option);
                    else rList.push(option);
                })
            }).catch(error => console.error(error));
        
        cUnregistered.replaceChildren(...unrList);
        cRegistered.replaceChildren(...rList);
    };

    async function updateApartamentos() {
        const unrList = []
        const rList = []

        await fetch('/api/urna/get_apartamentos')
            .then(response => response.json())
            .then((data) => {
                data.forEach(apartamento => {
                    rList.push(apartamento.numero);
                });
            }).catch(error => console.error(error));
        await fetch('/api/get_apartamentos')
            .then(response => response.json())
            .then((data) => {
                data.forEach(apartamento => {
                    if (!rList.includes(apartamento.numero)) unrList.push(apartamento.numero);
                });
            }).catch(error => console.error(error));
        
        aUnregistered.replaceChildren(...unrList.map(numero => {            
            const option = document.createElement('option');
            option.innerHTML = `Apartamento nº ${numero}`;
            return option;
        }));
        aRegistered.replaceChildren(...rList.map(numero => {            
            const option = document.createElement('option');
            option.innerHTML = `Apartamento nº ${numero}`;
            return option;
        }));
    };

    cSwapBtn.addEventListener('click', () => {
        const selectedUnregistered = document.querySelectorAll('#c-unregistered option:checked');
        const selectedRegistered = document.querySelectorAll('#c-registered option:checked');

        selectedUnregistered.forEach(async (option) => {
            cRegistered.appendChild(option);
            await fetch('/api/urna/add_candidato', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'nome': `${option.innerHTML}`})
            }).then(response => response.json()).then(data => console.log(data)).catch(error => console.error(error));
        });
        selectedRegistered.forEach(async (option) => {
            cUnregistered.appendChild(option);
            await fetch('/api/urna/remove_candidato', {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'nome': `${option.innerHTML}`})
            }).then(response => response.json()).then(data => console.log(data)).catch(error => console.error(error));
        });
    });

    aSwapBtn.addEventListener('click', () => {
        const selectedUnregistered = document.querySelectorAll('#a-unregistered option:checked');
        const selectedRegistered = document.querySelectorAll('#a-registered option:checked');

        selectedUnregistered.forEach(async (option) => {
            aRegistered.appendChild(option);
            await fetch('/api/urna/add_apartamento', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'numero': option.innerHTML.split(' ')[2]})
            }).then(response => response.json()).then(data => console.log(data)).catch(error => console.error(error));
        });
        selectedRegistered.forEach(async (option) => {
            aUnregistered.appendChild(option);
            await fetch('/api/urna/remove_apartamento', {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'numero': option.innerHTML.split(' ')[2]})
            }).then(response => response.json()).then(data => console.log(data)).catch(error => console.error(error));
        });
    });

    // cSaveBtn.addEventListener('click', async () => {
        
    // });

    updateCadidatos();
    updateApartamentos();
});