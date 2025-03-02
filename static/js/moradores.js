document.addEventListener('DOMContentLoaded', () => {
    const addAutoBtn = document.getElementById('add-auto');
    const addMoradorForm = document.getElementById('add-morador-form');

    async function updateMoradores() {
        const moradoresList = document.getElementById('moradores-list');
        const moradores = [];

        await fetch('/api/get_moradores')
            .then(response => response.json())
            .then((data) => {
                data.forEach(morador => {
                    const li = document.createElement('li');
                    li.innerHTML = `${morador.nome} | ${morador.apartamento}`;
                    if (morador.candidato) {
                        li.innerHTML += ` | Candidato`
                    }

                    // Adcicionado botão para remover
                    const dltBtn = document.createElement('button');
                    dltBtn.innerText = 'Remover';
                    dltBtn.addEventListener('click', async () => {
                        await fetch('/api/remove_morador', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(morador)
                        }).catch(error => console.error(error));

                        updateMoradores();
                    });
                    li.appendChild(dltBtn);

                    moradores.push(li);
                });
            })
            .catch(error => console.error(error));
        
        moradoresList.replaceChildren(...moradores);
        
    };

    updateMoradores();

    addAutoBtn.addEventListener('click', async () => {
        await fetch('/api/add_auto_morador')
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));

        updateMoradores();
    });

    addMoradorForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(addMoradorForm).entries());
        if (data.candidato == 'on') {
            data.candidato = true;
        }
        else {
            data.candidato = false;
        }

        console.log(data)

        await fetch('/api/add_morador', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).catch(error => console.error(error));

        updateMoradores();
    });
});