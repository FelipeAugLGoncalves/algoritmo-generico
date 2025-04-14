# Felipe Augusto - Nicolas Povoa
# Algoritmo Genético com Análise de Desempenho

import random
import matplotlib.pyplot as plt
import psutil
import platform
import time

def calcular_y(x):
    if x == 0:
        raise ValueError("x não pode ser zero (divisão por zero).")
    y = (x**2 + 3) / x**2
    print(f"y = ({x}² + 3) / {x}² = {y:.2f}")
    return y

def binario_para_decimal(individuo):
    return sum([bit * (2 ** idx) for idx, bit in enumerate(reversed(individuo))])

def avaliar_individuo(individuo):
    x = binario_para_decimal(individuo)
    print(f"Indivíduo: {individuo} -> x = {x}")
    return calcular_y(x)

def generate_population(size, length):
    return [[random.randint(0, 1) for _ in range(length)] for _ in range(size)]

def crossover(parent1, parent2):
    point = len(parent1) // 2
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def reaper(population, num_to_remove, y_history):
    y_values = []
    for ind in population:
        x = binario_para_decimal(ind)
        y = calcular_y(x)
        y_values.append((ind, y))
        y_history.append(y)

    y_values.sort(key=lambda pair: pair[1])
    weakest_individuals = [pair[0] for pair in y_values[:num_to_remove]]
    for individual in weakest_individuals:
        population.remove(individual)

    return population

def mostrar_info_computador():
    print("\n🔧 CONFIGURAÇÃO DO COMPUTADOR:")
    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Processador: {platform.processor()}")
    print(f"Núcleos (físicos/lógicos): {psutil.cpu_count(logical=False)} / {psutil.cpu_count(logical=True)}")
    print(f"Memória RAM Total: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")

def plotar_grafico_y(y_values):
    plt.figure(figsize=(10, 5))
    plt.plot(y_values, marker='o', linestyle='--', color='blue')
    plt.title('Valores de y dos Indivíduos ao Longo da Execução')
    plt.xlabel('Avaliações')
    plt.ylabel('Valor de y')
    plt.grid(True)
    plt.show()

def plotar_desempenho(cpu_usage, ram_usage):
    plt.figure(figsize=(10, 5))
    plt.plot(cpu_usage, label='Uso da CPU (%)', color='red')
    plt.plot(ram_usage, label='Uso da RAM (%)', color='green')
    plt.title('Desempenho do Computador Durante Execução')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Uso (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    population_size = 4
    chromosome_length = 8
    num_cruzamentos = 3
    y_history = []
    cpu_usage = []
    ram_usage = []

    mostrar_info_computador()

    population = generate_population(population_size, chromosome_length)
    print("\n📌 População Inicial:")
    for individual in population:
        y = avaliar_individuo(individual)
        y_history.append(y)

    for i in range(num_cruzamentos):
        time.sleep(0.5)  # Simula tempo de processamento
        cpu_usage.append(psutil.cpu_percent(interval=0.5))
        ram_usage.append(psutil.virtual_memory().percent)

        print(f"\n🔁 Cruzamento {i+1}:")
        parent1, parent2 = random.sample(population, 2)
        print("Pai:")
        avaliar_individuo(parent1)
        print("Mãe:")
        avaliar_individuo(parent2)
        child1, child2 = crossover(parent1, parent2)
        print("Filho 1:")
        y_history.append(avaliar_individuo(child1))
        print("Filho 2:")
        y_history.append(avaliar_individuo(child2))
        population.extend([child1, child2])

    print("\n☠️ Aplicando Ceifador...")
    population = reaper(population, num_to_remove=2, y_history=y_history)

    print("\n🏁 População Final:")
    for idx, individual in enumerate(population):
        print(f"\nIndivíduo {idx+1}:")
        y_history.append(avaliar_individuo(individual))

    print("\n📊 Estatísticas:")
    print(f"Quantidade de cruzamentos: {num_cruzamentos}")
    print(f"População inicial: {population_size}")
    print(f"População final: {len(population)}")
    print(f"Maior valor de y: {max(y_history):.2f}")
    print(f"Menor valor de y: {min(y_history):.2f}")

    plotar_grafico_y(y_history)
    plotar_desempenho(cpu_usage, ram_usage)

if __name__ == "__main__":
    exemplo = [0, 0, 0, 1, 1, 0, 1, 1]
    print("🧪 Avaliação de Exemplo:")
    avaliar_individuo(exemplo)
    print("\n🚀 Iniciando Algoritmo Genético:\n")
    main()
