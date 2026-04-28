# ============================================================
#  MGPEB - Módulo de Gerenciamento de Pouso e Estabilização
#          de Base | Missão Aurora Siger
# ============================================================
# Conteúdos articulados:
#   - Estruturas lineares (listas, pilhas, filas)
#   - Algoritmos de busca e ordenação
#   - Portas lógicas / funções booleanas (IF/ELIF/ELSE)
#   - Modelagem de funções matemáticas aplicadas
# ============================================================

from collections import deque   # fila (queue)

# ─────────────────────────────────────────────────────────────
# 1. DEFINIÇÃO DOS MÓDULOS DE POUSO
# ─────────────────────────────────────────────────────────────
# Cada módulo é representado como um dicionário com os
# atributos exigidos: nome, tipo, prioridade (1=mais alta),
# combustivel (%), massa (kg), criticidade ("ALTA"/"MEDIA"/"BAIXA")
# e horario_chegada (minutos a partir do tempo zero).

modulos_iniciais = [
    {
        "id": 1,
        "nome": "Aurora-HAB-01",
        "tipo": "Habitação",
        "prioridade": 1,
        "combustivel": 42,   # %
        "massa": 8500,        # kg
        "criticidade": "ALTA",
        "horario_chegada": 0  # min
    },
    {
        "id": 2,
        "nome": "Aurora-ENE-01",
        "tipo": "Energia",
        "prioridade": 2,
        "combustivel": 68,
        "massa": 5200,
        "criticidade": "ALTA",
        "horario_chegada": 15
    },
    {
        "id": 3,
        "nome": "Aurora-LAB-01",
        "tipo": "Laboratório Científico",
        "prioridade": 3,
        "combustivel": 75,
        "massa": 4100,
        "criticidade": "MEDIA",
        "horario_chegada": 30
    },
    {
        "id": 4,
        "nome": "Aurora-LOG-01",
        "tipo": "Logística",
        "prioridade": 4,
        "combustivel": 55,
        "massa": 9800,
        "criticidade": "MEDIA",
        "horario_chegada": 45
    },
    {
        "id": 5,
        "nome": "Aurora-MED-01",
        "tipo": "Suporte Médico",
        "prioridade": 2,
        "combustivel": 30,   # combustível baixo → alerta
        "massa": 3700,
        "criticidade": "ALTA",
        "horario_chegada": 20
    },
]

# ─────────────────────────────────────────────────────────────
# 2. ESTRUTURAS DE DADOS LINEARES
# ─────────────────────────────────────────────────────────────

fila_pouso     = deque()   # FILA  – módulos aguardando autorização
lista_pousados = []        # LISTA – módulos que já pousaram
lista_espera   = []        # LISTA – módulos adiados temporariamente
pilha_alertas  = []        # PILHA (LIFO) – módulos em situação crítica

# Popula a fila com todos os módulos iniciais
for m in modulos_iniciais:
    fila_pouso.append(m)

print("=" * 60)
print("   MGPEB — Missão Aurora Siger")
print("=" * 60)
print(f"\n[INIT] {len(fila_pouso)} módulos adicionados à fila de pouso.\n")


# ─────────────────────────────────────────────────────────────
# 3. FUNÇÕES DE BUSCA
# ─────────────────────────────────────────────────────────────

def busca_linear(estrutura, chave, valor):
    """Busca linear: percorre a estrutura procurando chave==valor.
    Retorna o primeiro módulo encontrado ou None."""
    for modulo in estrutura:
        if modulo.get(chave) == valor:
            return modulo
    return None

def busca_menor_combustivel(estrutura):
    """Retorna o módulo com o menor nível de combustível."""
    if not estrutura:
        return None
    return min(estrutura, key=lambda m: m["combustivel"])

def busca_maior_prioridade(estrutura):
    """Retorna o módulo com a maior prioridade (menor número = mais urgente)."""
    if not estrutura:
        return None
    return min(estrutura, key=lambda m: m["prioridade"])


# ─────────────────────────────────────────────────────────────
# 4. ALGORITMO DE ORDENAÇÃO — Bubble Sort por prioridade
# ─────────────────────────────────────────────────────────────

def ordenar_fila_por_prioridade(fila):
    """Converte a fila em lista, aplica Bubble Sort pela coluna
    'prioridade' (crescente) e reconstrói a fila."""
    lista = list(fila)
    n = len(lista)
    # Bubble Sort
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["prioridade"] > lista[j + 1]["prioridade"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    fila.clear()
    for item in lista:
        fila.append(item)
    print("[SORT] Fila reordenada por prioridade (Bubble Sort).")


# ─────────────────────────────────────────────────────────────
# 5. REGRAS BOOLEANAS DE AUTORIZAÇÃO DE POUSO
# ─────────────────────────────────────────────────────────────
# Expressões lógicas derivadas do diagrama de portas:
#
#  AUTORIZADO = (combustivel >= 35)
#               AND (condicao_atm == "ESTAVEL")
#               AND (area_disponivel == True)
#               AND (sensores_ok == True)
#
#  ALERTA     = (combustivel < 35) OR (criticidade == "ALTA")
#
#  BLOQUEADO  = NOT AUTORIZADO

COMBUSTIVEL_MINIMO = 35   # %

def avaliar_condicoes_ambiente():
    """Simula leitura de sensores externos.
    Retorna (condicao_atm, area_disponivel, sensores_ok)."""
    condicao_atm    = "ESTAVEL"  # poderia vir de sensor real
    area_disponivel = True
    sensores_ok     = True
    return condicao_atm, area_disponivel, sensores_ok

def autorizar_pouso(modulo):
    """Aplica as regras booleanas e decide: AUTORIZADO, ALERTA ou BLOQUEADO.
    Retorna uma string com o status."""
    comb_ok   = modulo["combustivel"] >= COMBUSTIVEL_MINIMO
    atm, area, sens = avaliar_condicoes_ambiente()

    # Porta AND principal
    autorizado = (comb_ok and (atm == "ESTAVEL") and area and sens)

    # Condição de alerta: combustível baixo OU carga crítica
    alerta = (not comb_ok) or (modulo["criticidade"] == "ALTA")

    if autorizado and not alerta:
        return "AUTORIZADO"
    elif autorizado and alerta:
        return "AUTORIZADO_COM_ALERTA"
    else:
        return "BLOQUEADO"


# ─────────────────────────────────────────────────────────────
# 6. FUNÇÃO MATEMÁTICA — Altura em função do tempo de descida
# ─────────────────────────────────────────────────────────────
# Modelo simplificado de descida com retrofoguetes:
#   h(t) = h0 - v0*t - (1/2)*a*t^2
# onde:
#   h0 = altitude inicial (m)
#   v0 = velocidade inicial de descida (m/s)  — positiva para baixo
#   a  = desaceleração aplicada pelos retrofoguetes (m/s^2)
#
# O sistema usa esta função para estimar o tempo até toque.

def altura_descida(t, h0=10000, v0=200, a=8.0):
    """Calcula a altitude h(t) em metros durante a descida.
    Retorna 0 quando atinge o solo."""
    h = h0 - v0 * t - 0.5 * a * t**2
    return max(h, 0)

def tempo_toque(h0=10000, v0=200, a=8.0, passo=0.5):
    """Estima o tempo (s) até h(t) = 0 por simulação discreta."""
    t = 0
    while altura_descida(t, h0, v0, a) > 0:
        t += passo
    return t

print("[MATH] Simulação de descida do módulo Aurora-HAB-01:")
for t_s in [0, 5, 10, 20, 30, 40]:
    print(f"       t = {t_s:>3}s  →  h = {altura_descida(t_s):>8.1f} m")
t_toque = tempo_toque()
print(f"       Toque estimado: t ≈ {t_toque:.1f} s\n")


# ─────────────────────────────────────────────────────────────
# 7. LOOP PRINCIPAL DE PROCESSAMENTO DA FILA
# ─────────────────────────────────────────────────────────────

# Primeiro, ordena a fila por prioridade
ordenar_fila_por_prioridade(fila_pouso)

print("\n[PROC] Iniciando processamento da fila de pouso...\n")
print("-" * 60)

while fila_pouso:
    modulo = fila_pouso.popleft()   # Desenfileira (FIFO)
    status = autorizar_pouso(modulo)

    print(f"Módulo : {modulo['nome']}  ({modulo['tipo']})")
    print(f"  Combustível: {modulo['combustivel']}%  |  "
          f"Massa: {modulo['massa']} kg  |  "
          f"Criticidade: {modulo['criticidade']}")
    print(f"  Status de Pouso: [{status}]")

    if status == "AUTORIZADO":
        lista_pousados.append(modulo)
        print("  → Pouso realizado com sucesso.")

    elif status == "AUTORIZADO_COM_ALERTA":
        lista_pousados.append(modulo)
        pilha_alertas.append(modulo)   # Empilha (LIFO) para revisão
        print("  → Pouso realizado, mas módulo entra em ALERTA.")

    else:  # BLOQUEADO
        lista_espera.append(modulo)
        print("  → Pouso BLOQUEADO. Módulo movido para lista de espera.")

    print()

print("-" * 60)


# ─────────────────────────────────────────────────────────────
# 8. RELATÓRIO RESUMIDO
# ─────────────────────────────────────────────────────────────

print("\n[RESUMO] Estado final das estruturas de dados")
print(f"  Pousados    : {len(lista_pousados)} módulo(s)")
for m in lista_pousados:
    print(f"    • {m['nome']}")

print(f"\n  Em espera   : {len(lista_espera)} módulo(s)")
for m in lista_espera:
    print(f"    • {m['nome']}")

print(f"\n  Pilha alertas (topo → base): {len(pilha_alertas)} módulo(s)")
while pilha_alertas:
    m = pilha_alertas.pop()    # Desempilha (LIFO)
    print(f"    ↑ {m['nome']}  — revisão necessária")


# ─────────────────────────────────────────────────────────────
# 9. DEMONSTRAÇÃO DAS FUNÇÕES DE BUSCA
# ─────────────────────────────────────────────────────────────

print("\n[BUSCA] Módulo com menor combustível na lista de pousados:")
resultado = busca_menor_combustivel(lista_pousados)
if resultado:
    print(f"  → {resultado['nome']}  ({resultado['combustivel']}%)")

print("\n[BUSCA] Módulo de maior prioridade na lista de pousados:")
resultado = busca_maior_prioridade(lista_pousados)
if resultado:
    print(f"  → {resultado['nome']}  (prioridade {resultado['prioridade']})")

print("\n[BUSCA] Busca linear por tipo 'Energia' em pousados:")
resultado = busca_linear(lista_pousados, "tipo", "Energia")
if resultado:
    print(f"  → Encontrado: {resultado['nome']}")
else:
    print("  → Não encontrado na lista de pousados.")

print("\n[FIM] MGPEB encerrado.\n")
