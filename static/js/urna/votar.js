const socket = io("http://localhost:8080");

document.addEventListener('DOMContentLoaded', async () => {
    const moradoresSlc = document.getElementById('morador-slc');
    const selecionarBtn = document.getElementById('selecionar-btn');
    const sectionConteiner = document.getElementById('section-conteiner');

    await fetch('/api/urna/get_apartamentos')
        .then(response => response.json())
        .then(data => {
            if (data.length < 1) {
                document.querySelectorAll('.pre-liberation').forEach(element => element.remove());
                sectionConteiner.innerHTML += `<h4>Não há Apartamentos cadastrados</h4>`;
            } else {
                let allApVoted = true;
                data.forEach(apartamento => {
                    if (!apartamento.votou) {
                        allApVoted = false;
                        apartamento.moradores.forEach(morador => {
                            const option = document.createElement('option');
                            option.innerHTML = `${morador} | Apartamento nº ${apartamento.numero}`;
                            moradoresSlc.appendChild(option);
                        });
                    };
                });
                if (allApVoted) {
                    document.querySelectorAll('.pre-liberation').forEach(element => element.remove());
                    sectionConteiner.innerHTML += `<h4>Todos os apartamentos já votaram</h4>`;
                }
            };
        }).catch(error => console.error(error));

    selecionarBtn.addEventListener('click', () => {
        const userId = moradoresSlc.selectedOptions[0].innerHTML;

        socket.emit("solicitar_liberacao", { user_id: userId });

        document.querySelectorAll('.pre-liberation').forEach(element => element.remove());
        sectionConteiner.innerHTML += `<span class="pre-liberation">Aguardando liberação...</span>`;

        socket.on("resposta_solicitacao", async (data) => {
            if (data.liberado) {
                alert("acesso liberado");

                document.querySelectorAll('.pre-liberation').forEach(element => element.remove());

                sectionConteiner.innerHTML += `<h4>Votando como ${userId}</h4>
                    <label for="candidato-slc">Selecione uma cadidato para votar</label>`;

                const select = document.createElement('select');
                select.id = 'candidato-slc';
                await fetch('/api/urna/get_candidatos')
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(candidato => {
                            const option = document.createElement('option');
                            option.innerHTML = `${candidato.nome} nº ${candidato.numero}`;
                            select.appendChild(option);
                        })
                    });
                sectionConteiner.appendChild(select);

                const button = document.createElement('button');
                button.innerHTML = 'Selecionar';
                button.addEventListener('click', async () => {
                    const body = { "numero": select.selectedOptions[0].innerHTML.split(' nº ')[1], "apartamento": userId.split(' nº ')[1] };
                    console.log(body)
                    await fetch('/api/urna/votar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(body)
                    }).then(response => response.json()).then(data => {
                        alert(`${data.msg}\nVocê será redirecionado.`);
                        window.location.href = '/';
                    }).catch(error => console.error(error));
                });
                sectionConteiner.appendChild(button);
            } else {
                alert("Acesso negado!\nVocê será redirecionado.");
                window.location.href = '/';
            }
        });
    });

});