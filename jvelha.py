import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

class Agente():
    def __init__(self, aprendizado=0.5):
        self.estado_jogo = None
        self.estado_anterior = None
        self.recompensa = None
        self.aprendizado = aprendizado
        self.modelo = self.criar_modelo()
        
    def criar_modelo(self):
        modelo = Sequential()
        modelo.add(Flatten(input_shape=(3, 3)))
        modelo.add(Dense(128, activation='relu'))
        modelo.add(Dense(64, activation='relu'))
        modelo.add(Dense(9, activation='softmax'))
        modelo.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))
        return modelo
    
    def escolher_jogada(self, estado_jogo):
        self.estado_jogo = estado_jogo
        print(self.aprendizado)
        if np.random.rand() <= self.aprendizado:
            return np.random.choice(9)
        else:
            estado_jogo = np.array(estado_jogo).reshape(1, 3, 3)
            valores_q = self.modelo.predict(estado_jogo)[0]
            return np.argmax(valores_q)
        
    def atualizar(self, recompensa):
        self.recompensa = recompensa
        estado_jogo = np.array(self.estado_jogo).reshape(1, 3, 3)
        valores_q = self.modelo.predict(estado_jogo)[0]
        valores_q[np.argmax(self.estado_anterior)] = self.recompensa
        self.modelo.fit(estado_jogo, valores_q.reshape(1, -1), epochs=1, verbose=0)
        
def jogar_jogo(agente):
    tabuleiro = np.zeros((3, 3))
    vitoria = 0
    empate = 0
    derrota = 0
    for i in range(10000):
        if i % 2 == 0:
            jogador = 1
        else:
            jogador = -1
        while True:
            if jogador == 1:
                acao = agente.escolher_jogada(tabuleiro)
                linha = acao // 3
                coluna = acao % 3
                if tabuleiro[linha][coluna] == 0:
                    tabuleiro[linha][coluna] = 1
                    break
            else:
                acao = int(input("Digite sua jogada (0-8): "))
                linha = acao // 3
                coluna = acao % 3
                if tabuleiro[linha][coluna] == 0:
                    tabuleiro[linha][coluna] = -1
                    break
        estado_atual = np.copy(tabuleiro)
        if verificar_vitoria(tabuleiro, jogador):
            vitoria += 1
            agente.atualizar(1)
            break
        elif verificar_empate(tabuleiro):
            empate += 1
            agente.atualizar(0)
            break
        else:
            agente.estado_anterior = np.copy(estado_atual)
            jogador *= -1
    return vitoria, empate, derrota

def verificar_vitoria(tabuleiro, jogador):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] == jogador:
            return True
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] == jogador:
            return True
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == jogador:
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == jogador:
        return True
    return False

def verificar_empate(tabuleiro):
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                return False
    return True

agente = Agente()
for i in range(10000):
    vitoria, empate, derrota = jogar_jogo(agente)
    if i % 1000 == 0:
        print(f"Vitórias: {vitoria} Empates: {empate} Derrotas: {derrota}")
    if i % 100 == 0:
        agente.aprendizado = max(agente.aprendizado - 0.01, 0.1)
        