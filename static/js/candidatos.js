document.addEventListener('DOMContentLoaded', () => {
    async function updateCandidatos() {
        const candidatosList = document.getElementById('candidatos-list');
        const list = []

        await fetch('/api/get_candidatos')
            .then(response => response.json())
            .then((data) => {
                data.forEach(candidato => {
                    const li = document.createElement('li');
                    li.innerHTML = `${candidato.nome} | nº ${candidato.numero} | Votos: ${candidato.votos}`;

                    list.push(li);
                })
            }).catch(error => console.error(error));
        
        candidatosList.replaceChildren(...list);
    };

    updateCandidatos();
});