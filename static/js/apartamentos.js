document.addEventListener('DOMContentLoaded', () => {
    async function updateList() {
        const list = document.getElementById('apartamentos-list');
        const apartamentos = []

        await fetch('/api/get_apartamentos')
            .then(response => response.json())
            .then((data) => {
                data.forEach(apartamento => {
                    const li = document.createElement('li');
                    li.innerHTML = `Apartamento nº ${apartamento.numero}`;
                    if (data.votou) {
                        li.innerHTML += ` | ✅ Votou`;
                    } else {
                        li.innerHTML += ` | ❌ Votou`;
                    }
                    li.innerHTML += ` | Moradores: ${apartamento.moradores.join(', ')}`;

                    apartamentos.push(li)
                });
            })
            .catch(error => console.error(error));
        
        list.replaceChildren(...apartamentos);
    };

    updateList();
});