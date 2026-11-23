import logging
from datetime import datetime

# 1. Archivo de logs
logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
#definicion de excepciones personalizadas
# 2. Excepciones Personalizadas
class ErrorParqueadero(Exception):
    """Excepción base para errores del sistema de parqueadero."""
    pass

class HoraInvalidaError(ErrorParqueadero):
    """Se lanza cuando las horas están fuera de rango o la salida es menor al ingreso."""
    pass

class DatoVacioError(ErrorParqueadero):
    """Se lanza cuando un campo de texto queda vacío."""
    pass

class RegistroCarroError(ErrorParqueadero):
    """Excepción para demostrar encadenamiento de excepciones."""
    pass

#aqui definimos la clase carro con sus datos basicos y revisamos que no haya errores al ingresar
class Carro:
    _valor_hora = 2000
    
    # Corrección 1: Doble guion bajo en __init__
    def __init__(self, color, marca, placa, hora_ingreso, hora_salida):
        if not color.strip() or not marca.strip() or not placa.strip():
            raise DatoVacioError("El color, la marca y la placa no pueden estar vacíos.")
        if not (0 <= hora_ingreso <= 23) or not (0 <= hora_salida <= 23):
            raise HoraInvalidaError("Las horas deben estar entre 0 y 23.")
        if hora_salida < hora_ingreso:
            raise HoraInvalidaError("La hora de salida no puede ser menor a la de ingreso.")
            
        self._color = color.strip()
        self._marca = marca.strip()
        self._placa = placa.strip().upper()
        self._hora_ingreso = hora_ingreso
        self._hora_salida = hora_salida
        
    def horas_a_pagar(self):
        horas = self._hora_salida - self._hora_ingreso
        return horas * self._valor_hora
        
    def mostrar_informacion(self):
        return (
            f"Carro: {self._color} | Marca: {self._marca} | Placa: {self._placa} | "
            f"Ingreso: {self._hora_ingreso}:00 | Salió: {self._hora_salida}:00"
        )


def registrar_carro():
    """Captura datos y aplica encadenamiento de excepciones."""
    try:
        color = input("Color del carro: ")
        marca = input("Marca del carro: ")
        placa = input("Placa: ")
        hora_ingreso = int(input("Hora de ingreso (0-23): "))
        hora_salida = int(input("Hora de salida (0-23): "))
        
        return Carro(color, marca, placa, hora_ingreso, hora_salida)
        
    except (ValueError, ErrorParqueadero) as e:
        raise RegistroCarroError(f"Fallo al procesar los datos del vehículo: {e}") from e


# --- Ejecución principal estable ---
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"📅 Fecha y hora: {fecha_actual}")

lista_carros = []

while True:
    try:
        nuevo_carro = registrar_carro()
        
    except RegistroCarroError as e:
        # Corrección 2: Doble guion bajo en __cause__
        logging.error(f"{e} | Causa original: {repr(e.__cause__)}")
        print(f"\n⚠️ {e}\nPor favor, intenta registrar el vehículo nuevamente.\n")
        
    else:
        lista_carros.append(nuevo_carro)
        print("✅ Vehículo registrado con éxito.")
        
    finally:
        print(f"ℹ️ Total parcial en sistema: {len(lista_carros)} carro(s).")
        continuar = input("¿Deseas registrar otro carro? (s/n): ").strip().lower()
        if continuar != "s":
            break

# --- Resumen final ---
print("\n" + "-" * 50)
print(f"📊 Total de carros registrados: {len(lista_carros)}")
print("        RESUMEN DEL DÍA")
print("-" * 50)
total_dia = 0

for carro in lista_carros:
    valor = carro.horas_a_pagar()
    total_dia += valor
    print(f"{carro.mostrar_informacion()} → Paga: $ {valor:,} pesos")

print("-" * 50)
print(f"💰 TOTAL DEL DÍA: $ {total_dia:,} pesos")
print("Proceso finalizado, codigo sin parar")
