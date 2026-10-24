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
        self.propietario = propietario  # Objeto Propietario asociado

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
        print(f"Tratamiento [{self.codigo}]: {self.descripcion} | Meds: {self.medicamentos} | Costo: ${self.costo:,.0f}")


# 5. Clase CitaVeterinaria
class CitaVeterinaria:
    def __init__(self, id_cita, fecha, motivo_consulta, mascota):
        self.id_cita = id_cita
        self.fecha = fecha
        self.motivo_consulta = motivo_consulta
        self.mascota = mascota
        self.tratamiento = None  # Se asigna después

    def asignar_tratamiento(self, tratamiento):
        self.tratamiento = tratamiento

    def mostrar_resumen_cita(self):
        print("\n" + "="*40)
        print("       RESUMEN DE LA CITA VETERINARIA       ")
        print("="*40)
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
            
        print(f"Mascota: {self.mascota.nombre} ({tipo_mascota}, {self.mascota.edad} años) -> {detalle}")
        print(f"Sonido: ", end="")
        self.mascota.emitir_sonido()
        
        if self.tratamiento:
            print("\n-- Detalle del Tratamiento --")
            self.tratamiento.mostrar_tratamiento()
        else:
            print("\nTratamiento: Pendiente de asignación.")
        print("="*40 + "\n")


# ==========================================
# 6. PROGRAMA PRINCIPAL (MENÚ INTERACTIVO)
# ==========================================
def main():
    # Listas para almacenar los datos en memoria
    lista_propietarios = []
    lista_mascotas = []
    lista_tratamientos = []
    lista_citas = []

    while True:
        print("\n*** SISTEMA DE GESTIÓN VETERINARIA ***")
        print("1. Registrar Propietario")
        print("2. Registrar Mascota (Perro o Gato)")
        print("3. Registrar Tratamiento")
        print("4. Agendar Cita Veterinaria y Asignar Tratamiento")
        print("5. Mostrar Resumen de todas las Citas")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- Registro de Propietario ---")
            nombre = input("Nombre completo: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            
            nuevo_prop = Propietario(nombre, telefono, direccion)
            lista_propietarios.append(nuevo_prop)
            print("¡Propietario registrado con éxito!")

        elif opcion == "2":
            if not lista_propietarios:
                print("\n[!] Primero debe registrar al menos un propietario.")
                continue
                
            print("\n--- Registro de Mascota ---")
            print("Propietarios disponibles:")
            for i, p in enumerate(lista_propietarios):
                print(f"{i}. {p.nombre}")
            
            try:
                idx_prop = int(input("Seleccione el número del propietario: "))
                propietario_seleccionado = lista_propietarios[idx_prop]
            except (ValueError, IndexError):
                print("[!] Opción inválida.")
                continue

            id_mascota = input("ID de la mascota (ej: M01): ")
            nombre = input("Nombre de la mascota: ")
            try:
                edad = int(input("Edad (en años): "))
            except ValueError:
                print("[!] La edad debe ser un número.")
                continue

            tipo = input("¿Qué tipo de mascota es? (1. Perro / 2. Gato): ").strip()

            if tipo == "1":
                raza = input("Raza: ")
                tamanio = input("Tamaño (Pequeño, Mediano, Grande): ")
                nueva_mascota = Perros(id_mascota, nombre, edad, propietario_seleccionado, raza, tamanio)
                lista_mascotas.append(nueva_mascota)
                print("¡Perro registrado con éxito!")
            elif tipo == "2":
                color_pelaje = input("Color de pelaje: ")
                esterilizado_str = input("¿Está esterilizado? (s/n): ").lower()
                es_esterilizado = True if esterilizado_str == 's' else False
                nueva_mascota = Gatos(id_mascota, nombre, edad, propietario_seleccionado, color_pelaje, es_esterilizado)
                lista_mascotas.append(nueva_mascota)
                print("¡Gato registrado con éxito!")
            else:
                print("[!] Tipo de mascota no válido.")

        elif opcion == "3":
            print("\n--- Registro de Tratamiento ---")
            codigo = input("Código del tratamiento (ej: T01): ")
            descripcion = input("Descripción: ")
            medicamentos = input("Medicamentos recetados: ")
            try:
                costo = float(input("Costo ($): "))
            except ValueError:
                print("[!] El costo debe ser numérico.")
                continue

            nuevo_tratamiento = Tratamiento(codigo, descripcion, medicamentos, costo)
            lista_tratamientos.append(nuevo_tratamiento)
            print("¡Tratamiento registrado con éxito!")

        elif opcion == "4":
            if not lista_mascotas:
                print("\n[!] No hay mascotas registradas para asignar a una cita.")
                continue

            print("\n--- Agendar Cita Veterinaria ---")
            id_cita = input("ID de la cita (ej: C100): ")
            fecha = input("Fecha de la cita (DD/MM/AAAA): ")
            motivo = input("Motivo de la consulta: ")

            print("\nMascotas disponibles:")
            for i, m in enumerate(lista_mascotas):
                print(f"{i}. {m.nombre} ({type(m).__name__}) - Dueño: {m.propietario.nombre}")
            
            try:
                idx_mascota = int(input("Seleccione el número de la mascota: "))
                mascota_seleccionada = lista_mascotas[idx_mascota]
            except (ValueError, IndexError):
                print("[!] Opción inválida.")
                continue

            nueva_cita = CitaVeterinaria(id_cita, fecha, motivo, mascota_seleccionada)

            # Asignar tratamiento opcional
            if lista_tratamientos:
                asociar_t = input("¿Desea asignar un tratamiento ya registrado? (s/n): ").lower()
                if asociar_t == 's':
                    print("\nTratamientos disponibles:")
                    for i, t in enumerate(lista_tratamientos):
                        print(f"{i}. {t.descripcion} (Costo: ${t.costo:,.0f})")
                    try:
                        idx_t = int(input("Seleccione el número del tratamiento: "))
                        nueva_cita.asignar_tratamiento(lista_tratamientos[idx_t])
                    except (ValueError, IndexError):
                        print("[!] Selección de tratamiento inválida. Se dejará pendiente.")

            lista_citas.append(nueva_cita)
            print("¡Cita agendada con éxito!")

        elif opcion == "5":
            if not lista_citas:
                print("\n[!] No hay citas registradas en el sistema.")
            else:
                for cita in lista_citas:
                    cita.mostrar_resumen_cita()

        elif opcion == "6":
            print("\nSaliendo del sistema de gestión veterinaria. ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción no válida. Por favor, elija un número del 1 al 6.")

if __name__ == "__main__":
    main()