import pandas as pd
import scipy.stats
import streamlit as st
import time
import matplotlib.pyplot as plt

# Título de la aplicación
st.title('Simulador de Lanzamiento de Moneda')
st.write('Esta aplicación simula el lanzamiento de una moneda y muestra la media de los resultados en un gráfico.')

# Variables de estado que se conservan entre ejecuciones de Streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# Función para simular el lanzamiento de una moneda
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)  # Simula n lanzamientos de moneda
    mean = None
    outcome_no = 0
    outcome_1_count = 0
    results = []

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no  # Calcula la media actual
        results.append(mean)  # Guarda la media en una lista
        time.sleep(0.05)  # Pequeña pausa para visualizar el progreso

    return results

# Widgets de la interfaz de usuario
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)  # Control deslizante para elegir el número de intentos
start_button = st.button('Ejecutar')  # Botón para iniciar el experimento
reset_button = st.button('Reiniciar')  # Botón para reiniciar los resultados

# Lógica cuando se presiona el botón "Reiniciar"
if reset_button:
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])
    st.write('Resultados reiniciados.')

# Lógica cuando se presiona el botón "Ejecutar"
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1

    # Simula los lanzamientos y obtiene los resultados
    results = toss_coin(number_of_trials)

    # Muestra el gráfico de líneas
    fig, ax = plt.subplots()
    ax.plot(range(len(results)), results, label='Media de los resultados')
    ax.set_xlabel('Número de intentos')
    ax.set_ylabel('Media')
    ax.legend()
    st.pyplot(fig)

    # Guarda los resultados en el DataFrame
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, results[-1]]],
                     columns=['no', 'iteraciones', 'media'])
    ], axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# Muestra la tabla con los resultados de todos los experimentos
st.write('### Resultados de los experimentos')
st.write(st.session_state['df_experiment_results'])

# Pie de página
st.markdown('---')
st.write('Desarrollado por [Elian] - [Enlace a tu GitHub](https://github.com/elianpjl)')
