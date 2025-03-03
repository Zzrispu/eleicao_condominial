const socket = io("http://localhost:8080");

document.addEventListener("DOMContentLoaded", () => {
    socket.on("solicitacao_recebida", (data) => {
        const userId = data.user_id;
        const requestsBox = document.getElementById('requests-box');

        const li = document.createElement('li');
        li.innerHTML = `<span><b>${userId}</b> quer usar a Urna</span>`;

        const liberarBtn = document.createElement('button');
        liberarBtn.innerHTML = 'Liberar'
        liberarBtn.addEventListener('click', () => {
            socket.emit("responder_solicitacao", { user_id: userId, liberado: true });
            li.remove();
        });
        li.appendChild(liberarBtn);

        const negarBtn = document.createElement('button');
        negarBtn.innerHTML = 'Negar'
        negarBtn.addEventListener('click', () => {
            socket.emit("responder_solicitacao", { user_id: userId, liberado: false });
            li.remove();
        });
        li.appendChild(negarBtn);

        requestsBox.appendChild(li);
    });

    const autoVotarBtn = document.getElementById('auto-votar-btn');
    autoVotarBtn.addEventListener('click', async () => {
        let candidatos = []
        await fetch('/api/urna/get_candidatos')
            .then(response => response.json())
            .then(data => {
                data.forEach(candidato => {
                    candidatos.push(candidato.numero)
                })
            });

        await fetch('/api/urna/get_apartamentos')
            .then(response => response.json())
            .then(data => {
                if (data.length < 1) {
                    alert('Não há apartamentos cadastrados.')
                } else {
                    let allApVoted = true;
                    data.forEach(async (apartamento) => {
                        if (!apartamento.votou) {
                            allApVoted = false;
                            await fetch('/api/urna/votar', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ "numero": candidatos[Math.floor(Math.random() * candidatos.length)], "apartamento": apartamento.numero })
                            }).then(response => response.json()).then(data => console.log(data.msg)).catch(error => console.error(error));
                        };
                    });
                    if (allApVoted) {
                        alert('Todos os apartamentos já votaram');
                    }
                };
            }).catch(error => console.error(error));
    });
});