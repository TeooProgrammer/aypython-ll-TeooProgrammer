
def agregar_participante(participantes, nombre, edad, correoelectronico="Desconocido"):
    participante.append([nombre, edad, ciudad]) # type: ignore
    print(f"Participante{nombre} agregado exitosamente")

def mostrar_participante(participante):
    print(f"Total de participante: {len(participante)}")
    i = 1
    for participante in participantes: # type: ignore
        print(f"Participante {i}: {participante[0]}, Edad: {estudiante[1]}, Correo electronico: {estudiante[2]}") # type: ignore
        print(f"Tipo de dato: {type(estudiante)}, ID: {id(estudiante)}") # type: ignore
        i += 1

def eliminar_participante(participantes, nombre):
    for i in range(len(participantes)):
        if participantes[i][0].lower() == nombre.lower():
            del participantes[i]
            return f"participante {nombre} eliminado exitosamente."
    return f"Estudiante {nombre} no encontrado."

def calcular_edad_promedio(participantes):
    if not estudiantes: # type: ignore
        print("no hay participantes para calcular promedio.")
        return
    total_edad = sum(participante[1] for participante in participantes)
    promedio = total_edad / len(participantes)
    print(f"Edad promedio de los estudiantes: {promedio:.2f}")

