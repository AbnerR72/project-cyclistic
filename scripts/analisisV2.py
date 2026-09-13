"""

Este código procesa y consolida varios archivos de Excel con datos de viajes de Cyclistic.
Calcula la duración de cada viaje, elimina registros duplicados o con tiempos no válidos y clasifica los viajes por día de la semana.
Posteriormente, compara el comportamiento de los usuarios ocasionales y los miembros anuales mediante métricas como el número de viajes, la duración, los días de mayor uso y el tipo de bicicleta preferido.
Finalmente, genera una gráfica para visualizar la evolución mensual de los viajes de ambos grupos.

"""



import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Directorio donde se encuentran los archivos de Excel procesados por el sript de limpieza
ruta_archivos = r'C:\Users\abner\Documents\DataAnalyst\Cyclistic\DATOS\AnalisisPy\archivos_procesados'
todos_los_archivos = glob.glob(os.path.join(ruta_archivos, "*.xlsx"))

lista_dataframes = []

for archivo in todos_los_archivos:
    df = pd.read_excel(archivo)
    
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    
    df['ride_length'] = df['ended_at'] - df['started_at']
    df = df[df['ride_length'].dt.total_seconds() > 0]
    
    df['day_of_week'] = (df['started_at'].dt.dayofweek + 1) % 7 + 1
    df = df.drop_duplicates(subset=['ride_id'])
    
    lista_dataframes.append(df)
    print(f"Procesado: {os.path.basename(archivo)} - Filas válidas: {len(df)}")

df_anual = pd.concat(lista_dataframes, ignore_index=True)
print(f"\nConsolidación exitosa. Total de registros anuales: {len(df_anual)}")

# ============================================================================
# ANÁLISIS MACRO: LA FOTOGRAFÍA GENERAL
# ============================================================================
print("\n" + "="*50)
print("ANÁLISIS MACRO: MÉTRICAS CLAVE")
print("="*50)

# 1. Volumen total y porcentaje de viajes
print("\n--- 1. Volumen de Viajes por Segmento ---")
conteo_usuarios = df_anual['member_casual'].value_counts()
porcentaje_usuarios = df_anual['member_casual'].value_counts(normalize=True) * 100

for tipo, total in conteo_usuarios.items():
    print(f"{tipo.capitalize()}: {total:,.0f} viajes ({porcentaje_usuarios[tipo]:.2f}%)")

# 2. Estadísticas de tiempo (en minutos)
print("\n--- 2. Estadísticas de Tiempo de Uso (en minutos) ---")
df_anual['ride_length_mins'] = df_anual['ride_length'].dt.total_seconds() / 60
stats_duracion = df_anual.groupby('member_casual')['ride_length_mins'].agg(['mean', 'min', 'max', 'median'])
print(stats_duracion.round(2))

# 3. Viajes por día de la semana
print("\n--- 3. Viajes por día de la semana ---")
uso_dias = df_anual.groupby(['member_casual', 'day_of_week']).size().unstack()
print(uso_dias)

# 4. Preferencia de tipo de bicicleta por usuario
print("\n--- 4. Uso de Tipo de Bicicleta por Usuario ---")
conteo_bicis = df_anual.groupby(['member_casual', 'rideable_type']).size()

for (usuario, bici), conteo in conteo_bicis.items():
    total_usuario = conteo_usuarios[usuario]
    porcentaje = (conteo / total_usuario) * 100
    print(f"{usuario.capitalize()} - {bici}: {porcentaje:.2f}%")

# ==========================================
# VISUALIZACIÓN: SERIE DE TIEMPO POR MES
# ==========================================
# Extraer el mes y año (formato YYYY-MM) de la fecha de inicio
df_anual['year_month'] = df_anual['started_at'].dt.to_period('M')

# Agrupar los datos para contar los viajes mensuales por tipo de usuario
viajes_por_mes = df_anual.groupby(['year_month', 'member_casual']).size().reset_index(name='total_viajes')
viajes_por_mes['year_month'] = viajes_por_mes['year_month'].astype(str)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 7))

sns.lineplot(
    data=viajes_por_mes, 
    x='year_month', 
    y='total_viajes', 
    hue='member_casual', 
    marker='o',       
    linewidth=2.5,
    palette={'casual': '#FF8C00', 'member': '#1E90FF'} 
)

plt.title('Estacionalidad: Uso Mensual de Bicicletas (Miembros vs. Ocasionales)', fontsize=16, fontweight='bold')
plt.xlabel('Mes del Año', fontsize=12)
plt.ylabel('Cantidad Total de Viajes', fontsize=12)
plt.xticks(rotation=45) 
plt.legend(title='Tipo de Usuario', fontsize=11)
plt.tight_layout()

plt.show()