from flask import render_template, request, redirect, jsonify
from app import app
from agentes import Morador, Candidato, Apartamento
import pandas as pd

loaded_auto = False
condominio = Apartamento(numero=000)

@app.get('/')
def homepage():
    return render_template('index.html')

@app.get('/moradores')
def moradores():
    return render_template('moradores.html')
    
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

    msg = condominio.remove_morador(nome=data.get('nome'))
    return jsonify({"msg": f"{msg}"})
    