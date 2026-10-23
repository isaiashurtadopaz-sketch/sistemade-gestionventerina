from abc import ABC, abstractmethod

# 1. Clase Propietario
class Propietario:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def mostra_informacion(self):
        print(f"Propietario: {self.nombre} | Tel: {self.telefono} | Dirección: {self.direccion}")


# 2. Clase Base (Abstracta) Mascota
class Mascota(ABC):
    def __init__(self, id_mascotas, nombre, edad, propietario):
        self.id_mascotas = id_mascotas
        self.nombre = nombre
        self.edad = edad
        self.propietario = propietario  # Relación con Propietario

    @abstractmethod
    def emitir_sonido(self):
        pass


# 3. Clases Hijas: Perros y Gatos
class Perros(Mascota):
    def __init__(self, id_mascotas, nombre, edad, propietario, raza, tamanio):
        super().__init__(id_mascotas, nombre, edad, propietario)
        self.raza = raza
        self.tamanio = tamanio

    def emitir_sonido(self):
        print("¡Guau guau!")


class Gatos(Mascota):
    def __init__(self, id_mascotas, nombre, edad, propietario, color_pelaje, es_esterilizado):
        super().__init__(id_mascotas, nombre, edad, propietario)
        self.color_pelaje = color_pelaje
        self.es_esterilizado = es_esterilizado

    def emitir_sonido(self):
        print("¡Miau miau!")


# 4. Clase Tratamiento
class Tratamiento:
    def __init__(self, codigo, descripcion, medicamentos, costo):
        self.codigo = codigo
        self.descripcion = descripcion
        self.medicamentos = medicamentos
        self.costo = costo

    def mostrar_tratamiento(self):
        print(f"Tratamiento: {self.descripcion} | Medicamentos: {self.medicamentos} | Costo: ${self.costo:,.0f}")


# 5. Clase CitaVeterinaria
class CitaVeterinaria:
    def __init__(self, id_cita, fecha, motivo_consulta, mascota, tratamiento=None):
        self.id_cita = id_cita
        self.fecha = fecha
        self.motivo_consulta = motivo_consulta
        self.mascota = mascota
        self.tratamiento = tratamiento  # Se asigna después

    def asignar_tratamiento(self, tratamiento):
        self.tratamiento = tratamiento

    def mostrar_resumen_cita(self):
        print("--- RESUMEN DE LA CITA VETERINARIA ---")
        print(f"Cita ID: {self.id_cita} | Fecha: {self.fecha}")
        print(f"Motivo: {self.motivo_consulta}")
        self.mascota.propietario.mostra_informacion()
        
        tipo_mascota = type(self.mascota).__name__
        if isinstance(self.mascota, Perros):
            detalle = f"Raza: {self.mascota.raza} | Tamaño: {self.mascota.tamanio}"
        elif isinstance(self.mascota, Gatos):
            esterilizado = "Sí" if self.mascota.es_esterilizado else "No"
            detalle = f"Pelaje: {self.mascota.color_pelaje} | Esterilizado: {esterilizado}"
        else:
            detalle = "N/A"
            
        print(f"Mascota: {self.mascota.nombre} ({tipo_mascota}) -> {detalle}")
        
        if self.tratamiento:
            self.tratamiento.mostrar_tratamiento()
        else:
            print("Tratamiento: Pendiente de asignación.")
        print("-------------------------------------")


# ==========================================
# 6. EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    # Registrar un propietario
    dueno1 = Propietario("María Gómez", "3001234567", "Calle 10 # 5-20")

    # Registrar una mascota (en este caso, un Perro de la clase Perros)
    perro1 = Perros("M01", "Max", 3, dueno1, "Labrador", "Grande")

    # Crear la cita veterinaria (exactamente con los campos del diagrama)
    cita1 = CitaVeterinaria("C100", "22/10/2026", "Chequeo general y vacuna antirrábica", perro1)

    # Crear y asignar un tratamiento
    tratamiento1 = Tratamiento("T01", "Vacunación y desparasitación", "Vacuna Antirrábica 1ml + Pastilla Drontal", 45000)
    cita1.asignar_tratamiento(tratamiento1)

    # Mostrar resultados
    cita1.mostrar_resumen_cita()
    
    print(f"Sonido de {perro1.nombre}: ", end="")
    perro1.emitir_sonido()