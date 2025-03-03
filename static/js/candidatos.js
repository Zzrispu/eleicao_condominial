document.addEventListener('DOMContentLoaded', async () => {
    const candidatosList = document.getElementById('candidatos-list');

    await fetch('/api/urna/get_candidatos')
    .then(response => response.json())
    .then(data => {
        if (data.length < 1) {
            candidatosList.innerHTML += `Não há candidados cadastrados`
        } else {
            data.forEach(candidato => {
                const option = document.createElement('option');
                option.innerHTML = `${candidato.nome} nº ${candidato.numero}`;
                candidatosList.appendChild(option);
            });
        };
    });
});