from flask import render_template, request, jsonify
from flask_socketio import SocketIO, emit
from app import app
from agentes import Morador, Candidato, Apartamento, Urna
import pandas as pd

loaded_auto = False
condominio = Apartamento(numero=101)
urna = Urna()

socketio = SocketIO(app, cors_allowed_origins="*")
u_pendentes = {}

# Rotas para Views #
@app.get('/')
def homepage():
    return render_template('index.html')

@app.get('/moradores')
def moradores():
    return render_template('moradores.html')

@app.get('/candidatos')
def candidatos():
    return render_template('candidatos.html')

@app.get('/apartamentos')
def apartamentos():
    return render_template('apartamentos.html')

@app.get('/urna')
def viewUrna():
    return render_template('urna/urna.html')

@app.get('/urna/registrar')
def urna_registrar():
    return render_template('urna/registrar.html')

@app.get('/urna/votar')
def viewUrna_votar():
    return render_template('urna/votar.html')

@app.get('/urna/controle')
def urna_controle():
    return render_template('urna/controle.html')

@app.get('/resultados')
def resultados():
    return render_template('urna/resultados.html', resultados=urna.resultado())

# Rotas API #
@app.get('/api/add_auto_morador')
def add_auto_morador():
    global loaded_auto
    if loaded_auto:
        return {"loaded_auto": True}
    else:
        df = pd.read_csv('moradores.csv')
        df.reset_index()
        for index, morador in df.iterrows():
            if morador.tipo == 'candidato':
                condominio.add_morador(Candidato(morador.nome, morador.apartamento))
            else:
                condominio.add_morador(Morador(morador.nome, morador.apartamento))
        loaded_auto = True
        return {"loaded_auto": False}

@app.get('/api/get_moradores')
def get_moradores():
    moradores = []
    for ap in condominio.apartamentos:
        for morador in ap.moradores:
            if isinstance(morador, Candidato):
                moradores.append({"candidato": True, "nome": morador.nome, "apartamento": morador.apartamento.numero})
            else:
                moradores.append({"candidato": False, "nome": morador.nome, "apartamento": morador.apartamento.numero})
    return moradores

@app.get('/api/get_candidatos')
def get_candidatos():
    candidatos = []
    for ap in condominio.apartamentos:
        for candidato in ap.moradores:
            if isinstance(candidato, Candidato):
                candidatos.append({"nome": candidato.nome, "numero": candidato.numero, "votos": candidato.votos})
    return candidatos

@app.get('/api/get_apartamentos')
def get_apartamentos():
    apartamentos = []

    for ap in condominio.apartamentos:
        moradores = []

        for morador in ap.moradores:
            moradores.append(morador.nome)

        apartamentos.append({"numero": ap.numero, "moradores": moradores, "votou": ap.votou})

    return apartamentos

@app.post('/api/add_morador')
def add_morador():
    data = request.get_json()

    if not data.get('nome') or not data.get('apartamento'):
        return jsonify({"error": "Campos ausentes"}), 400

    if data.get('candidato') == True:
        condominio.add_morador(Candidato(nome=data.get('nome'), apartamento=data.get('apartamento')))
    else:
        condominio.add_morador(Morador(nome=data.get('nome'), apartamento=data.get('apartamento')))

    return jsonify({"msg": "Morador adicionado com sucesso"})

@app.post('/api/remove_morador')
def remove_morador():
    data = request.get_json()

    condominio.remove_morador(nome=data.get('nome'))
    return jsonify({"msg": f"teste"})

# Rotas API Urna #
@app.get('/api/urna/get_candidatos')
def urna_get_candidatos():
    candidatos = [{"nome": candidato.nome, "numero": candidato.numero, "votos": candidato.votos} for candidato in urna.candidatos]
    return candidatos

@app.get('/api/urna/get_apartamentos')
def urna_get_apartamentos():
    apartamentos = [{"numero": ap.numero, "moradores": [morador.nome for morador in ap.moradores], "votou": ap.votou} for ap in urna.apartamentos]
    return apartamentos

@app.post('/api/urna/add_candidato')
def urna_add_candidato():
    data = request.get_json()

    msg = urna.add_candidato(data.get('nome'))
    return jsonify({"msg": msg})

@app.post('/api/urna/add_apartamento')
def urna_add_apartamento():
    data = request.get_json()

    msg = urna.add_apartamento(int(data.get('numero')))
    return jsonify({"msg": msg})

@app.delete('/api/urna/remove_candidato')
def urna_remove_candidato():
    data = request.get_json()

    msg = urna.remove_candidato(data.get('nome'))
    return jsonify({"msg": msg})

@app.delete('/api/urna/remove_apartamento')
def urna_remove_apartamento():
    data = request.get_json()

    msg = urna.remove_apartamento(int(data.get('numero')))
    return jsonify({"msg": msg})

@app.post('/api/urna/votar')
def urna_votar():
    data = request.get_json()

    msg = urna.votar(int(data.get('numero')), int(data.get('apartamento')))
    return jsonify({"msg": msg})

# WebSocket #
@socketio.on("solicitar_liberacao")
def solicitar_liberacao(data):
    user_id = data["user_id"]
    u_pendentes[user_id] = request.sid

    emit("solicitacao_recebida", {"user_id": user_id}, broadcast=True)

@socketio.on('responder_solicitacao')
def responder_solicitacao(data):
    user_id = data["user_id"]
    liberado = data["liberado"]

    if user_id in u_pendentes:
        user_socket = u_pendentes.pop(user_id)
        emit("resposta_solicitacao", {"liberado": liberado}, room=user_socket)

@app.post('/liberar_voto')
def liberar_voto():
    chave = request.json.get('chave')
    socketio.emit('voto_liberado', {'chave': chave})
    return {"msg": "voto liberado"}