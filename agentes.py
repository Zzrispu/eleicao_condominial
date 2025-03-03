from random import randint

class Morador():
    def __init__(self, nome='', apartamento=''):
        self.nome = nome
        self.apartamento = apartamento

        while len(self.nome) < 3:
            self.nome = input("Digite um nome com mais de 3 caracteres: ")
        
        while not isinstance(self.apartamento, Apartamento):
            try:
                apartamento = int(apartamento)
                found = False

                for ap in Apartamento.apartamentos:
                    if ap.numero == apartamento:
                        self.apartamento = ap
                        found = True
                        break

                if not found:
                    self.apartamento = Apartamento(apartamento)

            except ValueError:
                print("Digite um número válido")
                apartamento = input(f"Digite um número de apartamento para criá-lo ou alocá-lo: ")
                continue

    def __str__(self):
        return f"{self.nome} mora no apartamento {self.apartamento.numero}"

    def votar(self, candidato: int, urna):
        urna.votar(numero=candidato, apartamento=self.apartamento)
        return f"{self.nome} votou no candidato de número {candidato}"


class Candidato(Morador):
    candidatos = []

    def __init__(self, nome='', apartamento=''):
        super().__init__(nome, apartamento)
        self.numero = 0
        self.votos = 0
        self.candidatos.append(self)

    def __str__(self):
        return f"{self.nome} é o candidato {self.numero} e tem {self.votos} votos"

    def set_numero(self, numero: int):
        self.numero = numero

    def set_votos(self, votos):
        self.votos = votos


class Apartamento():
    apartamentos = []

    def __init__(self, numero: int):
        self.numero = numero
        self.moradores = []
        self.votou = False
        self.apartamentos.append(self)

    def add_morador(self, morador: Morador):
        morador.apartamento.moradores.append(morador)

    def remove_morador(self, nome: str):
        for ap in self.apartamentos:
            for morador in ap.moradores:
                if morador.nome == nome:
                    ap.moradores.remove(morador)
                    return f"{morador.nome} do apartamento {morador.apartamento} foi removido"
        return f"Morador {nome} não foi encontrado"

    def remove_apartamento(self, apartamento: int):
        for ap in self.apartamentos:
            if ap.numero == apartamento:
                self.apartamentos.remove(ap)
                return f"O apartamento nº{ap.numero} foi removido"
        return f"Apartamento {apartamento} não foi encontrado"

    def reset_voto(self):
        self.votou = False

    def __str__(self):
        return f"Apartamento [ {self.numero} ] | Moradores: {', '.join([morador.nome for morador in self.moradores])}"

class Urna():
    def __init__(self):
        self.apartamentos = []
        self.candidatos = []

    def add_apartamento(self, apartamento: int):
        for ap in Apartamento.apartamentos:
            if ap.numero == apartamento:
                apartamento = ap
                break
        if not isinstance(apartamento, Apartamento): return "Apartamento Inexistente"
        if apartamento in self.apartamentos: return "Apartamento já cadastrado"

        self.apartamentos.append(apartamento)
        return f"Apartamento nº {apartamento.numero} foi cadastrado com sucesso"

    def add_candidato(self, candidato: str):
        for c in Candidato.candidatos:
            if c.nome == candidato:
                candidato = c
                break
        if not isinstance(candidato, Candidato): return "Candidato Inexistente"
        if candidato in self.candidatos: return "Candidato já cadastrado"

        setted = False

        for i in range(5):
            rn = randint(10, 99)
            numeros = [c.numero for c in self.candidatos]
            if rn not in numeros:
                candidato.set_numero(rn)
                setted = True
                break
        if not setted: return "Não foi possível gerar um número para o candidato"

        self.candidatos.append(candidato)
        return f"Candidato {candidato.nome} foi registrado com o número {candidato.numero}"

    def remove_candidato(self, candidato: str):
        for c in self.candidatos:
            if c.nome == candidato:
                candidato = c
                break
        if not isinstance(candidato, Candidato): return "Candidato não está cadastrado"

        candidato.numero = 0
        self.candidatos.remove(candidato)
        return f"Candidato {candidato.nome} número {candidato.numero} foi removido com sucesso"
    
    def remove_apartamento(self, apartamento: int):
        for ap in self.apartamentos:
            if ap.numero == apartamento:
                apartamento = ap
                break
        if not isinstance(apartamento, Apartamento): return "Apartamento não está cadastrado"

        self.apartamentos.remove(apartamento)
        return f"Apartamento nº {apartamento.numero} foi removido com sucesso"

    def votar(self, numero: int, apartamento: int):
        candidato = None

        for c in self.candidatos:
            if c.numero == numero:
                candidato = c
                break
        if candidato is None:
            return "Não há um cadidato com esse número"

        for ap in self.apartamentos:
            if ap.numero == apartamento:
                apartamento = ap
                break
        if not isinstance(apartamento, Apartamento): return "Apartamento não está cadastrado"

        if apartamento.votou:
            return "Apartamento já votou"

        candidato.set_votos(candidato.votos + 1)
        apartamento.votou = True

        return f"Voto computado para o candidato {candidato.numero}"

    def resultado(self):
        if not all([ap.votou for ap in self.apartamentos]) or len(self.apartamentos) < 1: return "Ainda falta todos os Apartamentos votarem"
        resultados = [{"candidato": f"{c.nome} nº {c.numero}", "votos": c.votos} for c in self.candidatos]
        return resultados