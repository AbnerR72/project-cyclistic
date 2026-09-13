# Este código está destinado a rellenar las celdas vacías de las siguientes columnas::
#- star_station_name = las celdas que este vacias se rellenaran con "unknown"
#- star_station_id = las celdas que este vacias se rellenaran con "NULL"
#- end_station_name = las celdas que este vacias se rellenaran con "unknown"
#- end_station_id = las celdas que este vacias se rellenaran con "NULL"

# r"C:\Users\abner\Documents\DataAnalyst\Cyclistic\DATOS\Datos_12Meses_Extraidos\Conversiones\*.xlsx"

import pandas as pd
import glob
import os

# Ruta donde se encuentran los archivos de Excel a procesar
ruta_archivos = r"C:\Users\abner\Documents\DataAnalyst\Cyclistic\DATOS\Datos_12Meses_Extraidos\Conversiones\*.xlsx"
archivos = glob.glob(ruta_archivos)

if len(archivos) == 0:
    print("Error: Python no encontró ningún archivo.")
else:
    print(f"¡Éxito! Python encontró {len(archivos)} archivos. Iniciando limpieza...\n")
    
    # Crear la carpeta de salida
    carpeta_salida = "archivos_procesados"
    os.makedirs(carpeta_salida, exist_ok=True)

    for archivo in archivos:
        nombre_original = os.path.basename(archivo)
        print(f"Procesando: {nombre_original}...")
        
        # Leer el archivo
        df = pd.read_excel(archivo)
        
        # Aplicar tus reglas de limpieza
        if 'star_station_name' in df.columns:
            df['star_station_name'] = df['star_station_name'].fillna('unknown')
            df['star_station_id'] = df['star_station_id'].fillna('NULL')
        elif 'start_station_name' in df.columns:
            df['start_station_name'] = df['start_station_name'].fillna('unknown')
            df['start_station_id'] = df['start_station_id'].fillna('NULL')
            
        df['end_station_name'] = df['end_station_name'].fillna('unknown')
        df['end_station_id'] = df['end_station_id'].fillna('NULL')
        
        # EL CAMBIO ESTÁ AQUÍ: Se conserva exactamente el mismo nombre del archivo original
        ruta_guardado = os.path.join(carpeta_salida, nombre_original)
        df.to_excel(ruta_guardado, index=False)
        
    print("\n¡Proceso finalizado con éxito! Los archivos están en la carpeta 'archivos_procesados'.")