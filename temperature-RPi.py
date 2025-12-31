import psutil
import time

def obtener_temperatura_procesador():
    # Obtener la temperatura del procesador en grados Celsius
    temperatura = psutil.sensors_temperatures().get('cpu_thermal')
    if temperatura:
        return temperatura[0].current
    else:
        return None

if __name__ == "__main__":
    try:
        while True:
            temperatura = obtener_temperatura_procesador()
            if temperatura is not None:
                print(f"CPU Temperature: {temperatura}°C", end = "\r")
            else:
                print("No se pudo obtener la temperatura del procesador.")
            time.sleep(5)  # Espera 5 segundos antes de volver a obtener la temperatura
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
