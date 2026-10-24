from abc import ABC, abstractmethod
import json
import os

# Archivo donde se guardarán los datos
ARCHIVO_DATOS = "veterinaria_datos.json"

# 1. Clase Propietario
class Propietario:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def mostra_informacion(self):
        print(f"Propietario: {self.nombre} | Tel: {self.telefono} | Dirección: {self.direccion}")

    def to_dict(self):
        """Convierte el objeto a diccionario para guardarlo en JSON"""
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion
        }


# 2. Clase Base (Abstracta) Mascota
class Mascota(ABC):
    def __init__(self, id_mascotas, nombre, edad, propietario):
        self.id_mascotas = id_mascotas
        self.nombre = nombre
        self.edad = edad
        self.propietario = propietario  # Objeto Propietario

    @abstractmethod
    def emitir_sonido(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


# 3. Clases Hijas: Perros y Gatos
class Perros(Mascota):
    def __init__(self, id_mascotas, nombre, edad, propietario, raza, tamanio):
        super().__init__(id_mascotas, nombre, edad, propietario)
        self.raza = raza
        self.tamanio = tamanio

    def emitir_sonido(self):
        print("¡Guau guau!")

    def to_dict(self):
        return {
            "tipo": "Perro",
            "id_mascotas": self.id_mascotas,
            "nombre": self.nombre,
            "edad": self.edad,
            "propietario_nombre": self.propietario.nombre, # Guardamos el nombre para enlazarlo
            "raza": self.raza,
            "tamanio": self.tamanio
        }


class Gatos(Mascota):
    def __init__(self, id_mascotas, nombre, edad, propietario, color_pelaje, es_esterilizado):
        super().__init__(id_mascotas, nombre, edad, propietario)
        self.color_pelaje = color_pelaje
        self.es_esterilizado = es_esterilizado

    def emitir_sonido(self):
        print("¡Miau miau!")

    def to_dict(self):
        return {
            "tipo": "Gato",
            "id_mascotas": self.id_mascotas,
            "nombre": self.nombre,
            "edad": self.edad,
            "propietario_nombre": self.propietario.nombre,
            "color_pelaje": self.color_pelaje,
            "es_esterilizado": self.es_esterilizado
        }


# 4. Clase Tratamiento
class Tratamiento:
    def __init__(self, codigo, descripcion, medicamentos, costo):
        self.codigo = codigo
        self.descripcion = descripcion
        self.medicamentos = medicamentos
        self.costo = costo

    def mostrar_tratamiento(self):
        print(f"Tratamiento [{self.codigo}]: {self.descripcion} | Meds: {self.medicamentos} | Costo: ${self.costo:,.0f}")

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "medicamentos": self.medicamentos,
            "costo": self.costo
        }


# 5. Clase CitaVeterinaria
class CitaVeterinaria:
    def __init__(self, id_cita, fecha, motivo_consulta, mascota, tratamiento=None):
        self.id_cita = id_cita
        self.fecha = fecha
        self.motivo_consulta = motivo_consulta
        self.mascota = mascota
        self.tratamiento = tratamiento

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
# FUNCIONES DE GUARDADO Y CARGA (JSON)
# ==========================================
def guardar_datos(lista_propietarios, lista_mascotas, lista_tratamientos):
    datos = {
        "propietarios": [p.to_dict() for p in lista_propietarios],
        "mascotas": [m.to_dict() for m in lista_mascotas],
        "tratamientos": [t.to_dict() for t in lista_tratamientos]
    }
    with open(ARCHIVOS_DATOS := ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_datos():
    lista_propietarios = []
    lista_mascotas = []
    lista_tratamientos = []

    if not os.path.exists(ARCHIVO_DATOS):
        return lista_propietarios, lista_mascotas, lista_tratamientos

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)

            # Cargar propietarios
            for p_data in datos.get("propietarios", []):
                prop = Propietario(p_data["nombre"], p_data["telefono"], p_data["direccion"])
                lista_propietarios.append(prop)

            # Cargar mascotas y enlazar con su propietario
            for m_data in datos.get("mascotas", []):
                # Buscar el objeto Propietario por su nombre
                prop_asociado = next((p for p in lista_propietarios if p.nombre == m_data["propietario_nombre"]), None)
                if prop_asociado:
                    if m_data["tipo"] == "Perro":
                        mascota = Perros(m_data["id_mascotas"], m_data["nombre"], m_data["edad"], prop_asociado, m_data["raza"], m_data["tamanio"])
                    else:
                        mascota = Gatos(m_data["id_mascotas"], m_data["nombre"], m_data["edad"], prop_asociado, m_data["color_pelaje"], m_data["es_esterilizado"])
                    lista_mascotas.append(mascota)

            # Cargar tratamientos
            for t_data in datos.get("tratamientos", []):
                trat = Tratamiento(t_data["codigo"], t_data["descripcion"], t_data["medicamentos"], t_data["costo"])
                lista_tratamientos.append(trat)

    except Exception as e:
        print(f"[!] Error al cargar los datos guardados: {e}")

    return lista_propietarios, lista_mascotas, lista_tratamientos


# ==========================================
# 6. PROGRAMA PRINCIPAL (MENÚ INTERACTIVO)
# ==========================================
def main():
    # Cargar datos guardados previamente en el archivo JSON
    lista_propietarios, lista_mascotas, lista_tratamientos = cargar_datos()
    lista_citas = [] # Las citas se pueden mantener en sesión o guardar igual si lo deseas

    while True:
        print("\n*** SISTEMA DE GESTIÓN VETERINARIA ***")
        print("1. Registrar Propietario")
        print("2. Registrar Mascota (Perro o Gato)")
        print("3. Registrar Tratamiento")
        print("4. Agendar Cita Veterinaria y Asignar Tratamiento")
        print("5. Ver Historial General (Todas las Citas)")
        print("6. Ver Listado de Propietarios y Mascotas Guardados")
        print("7. Salir")
        
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- Registro de Propietario ---")
            nombre = input("Nombre completo: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            
            nuevo_prop = Propietario(nombre, telefono, direccion)
            lista_propietarios.append(nuevo_prop)
            guardar_datos(lista_propietarios, lista_mascotas, lista_tratamientos)
            print("¡Propietario registrado y guardado con éxito!")

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
                guardar_datos(lista_propietarios, lista_mascotas, lista_tratamientos)
                print("¡Perro registrado y guardado con éxito!")
            elif tipo == "2":
                color_pelaje = input("Color de pelaje: ")
                esterilizado_str = input("¿Está esterilizado? (s/n): ").lower()
                es_esterilizado = True if esterilizado_str == 's' else False
                nueva_mascota = Gatos(id_mascota, nombre, edad, propietario_seleccionado, color_pelaje, es_esterilizado)
                lista_mascotas.append(nueva_mascota)
                guardar_datos(lista_propietarios, lista_mascotas, lista_tratamientos)
                print("¡Gato registrado y guardado con éxito!")
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
            guardar_datos(lista_propietarios, lista_mascotas, lista_tratamientos)
            print("¡Tratamiento registrado y guardado con éxito!")

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
                        print("[!] Selección inválida. Se dejará pendiente.")

            lista_citas.append(nueva_cita)
            print("¡Cita agendada con éxito!")

        elif opcion == "5":
            if not lista_citas:
                print("\n[!] No hay citas registradas en esta sesión.")
            else:
                for cita in lista_citas:
                    cita.mostrar_resumen_cita()

        elif opcion == "6":
            print("\n--- REGISTROS GUARDADOS EN EL SISTEMA ---")
            print(f"\n[Propietarios ({len(lista_propietarios)}):]")
            for p in lista_propietarios:
                p.mostra_informacion()
                
            print(f"\n[Mascotas ({len(lista_mascotas)}):]")
            for m in lista_mascotas:
                tipo = type(m).__name__
                print(f"- {m.nombre} ({tipo}) | Edad: {m.edad} años | Dueño: {m.propietario.nombre}")

        elif opcion == "7":
            print("\nSaliendo del sistema de gestión veterinaria. ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción no válida. Elija un número del 1 al 7.")

if __name__ == "__main__":
    main()