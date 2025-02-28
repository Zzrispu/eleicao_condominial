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

        self.apartamento.add_morador(self)

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
        self.moradores.append(morador)

    def reset_voto(self):
        self.votou = False

    def __str__(self):
        return f"Apartamento [ {self.numero} ] | Moradores: {', '.join([morador.nome for morador in self.moradores])}"

class Urna():
    def __init__(self):
        self.apartamentos = []
        self.candidatos = []

    def add_apartamento(self, apartamento: Apartamento):
        if apartamento in self.apartamentos:
            return "Apartamento já cadastrado"

        self.apartamentos.append(apartamento)

    def add_candidato(self, candidato: Candidato):
        if candidato in self.candidatos:
            return "Candidato já cadastrado"

        setted = False

        for i in range(5):
            rn = randint(10, 99)
            numeros = [c.numero for c in self.candidatos]
            if rn not in numeros:
                candidato.set_numero(rn)
                setted = True
                break
        if not setted:
            return "Não foi possível gerar um número para o candidato"

        self.candidatos.append(candidato)

    def votar(self, numero: int, apartamento: Apartamento):
        candidato = None

        for c in self.candidatos:
            if c.numero == numero:
                candidato = c
                break
        if candidato is None:
            return "Candidato não cadastrado"

        if apartamento not in self.apartamentos:
            return "Apartamento não cadastrado"

        if apartamento.votou:
            return "Apartamento já votou"

        candidato.set_votos(candidato.votos + 1)
        apartamento.votou = True

        print(f"Voto computado para o candidato {candidato.numero}")

        if all([ap.votou for ap in self.apartamentos]):
            self.resultado()

    def resultado(self):
        ganhador = None
        for c in self.candidatos:
            if c.votos > (ganhador.votos if ganhador else 0):
                ganhador = c
            print(f"{c.nome} ({c.numero}): {c.votos} votos")
        print(f"Ganhador: {ganhador.nome} ({ganhador.numero}): {ganhador.votos} votos")