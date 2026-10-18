# Generador de HWID

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplicación de escritorio para generar un **Identificador de Hardware (HWID)** único a partir de componentes del sistema. El HWID se obtiene combinando seriales de hardware y aplicando un hash **SHA-256** truncado a 16 caracteres.

---

## 📋 Índice

- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Flujo de Generación del HWID](#-flujo-de-generación-del-hwid)
- [Diagrama de Clases](#-diagrama-de-clases)
- [Interfaz Gráfica](#-interfaz-gráfica)
- [Requisitos](#-requisitos)
- [Ejecución](#-ejecución)
- [Compilación a .exe](#-compilación-a-exe)
- [Prueba del Módulo Lógico](#-prueba-del-módulo-lógico)
- [Manejo de Errores](#-manejo-de-errores)

---

## 📁 Estructura del Proyecto

```mermaid
flowchart TD
    subgraph Raíz [hwid_generator/]
        A[main.py] --> B[src/]
        C[requirements.txt]
        D[build_exe.bat]
        E[README.md]
        F[HWID_Generator.spec]
        G[dist/]
    end

    subgraph src [src/]
        direction LR
        H[__init__.py]
        I[logic.py]
        J[gui.py]
    end

    B --> H
    B --> I
    B --> J

    G --> K[HWID_Generator.exe]

    style Raíz fill:#1a1a2e,color:#fff,stroke:#e94560
    style src fill:#16213e,color:#fff,stroke:#0f3460
    style A fill:#e94560,color:#fff
    style I fill:#533483,color:#fff
    style J fill:#0f3460,color:#fff
    style K fill:#00b4d8,color:#fff
```

### Descripción de archivos

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Punto de entrada de la aplicación. Inicializa la ventana tkinter. |
| `src/logic.py` | Módulo de lógica: obtiene seriales de hardware y genera el hash SHA-256. |
| `src/gui.py` | Módulo de interfaz: construye la ventana, botones y manejo de eventos. |
| `requirements.txt` | Lista de dependencias necesarias (`pywin32`, `wmi`, `pyinstaller`). |
| `build_exe.bat` | Script para compilar el proyecto a un ejecutable `.exe`. |
| `dist/HWID_Generator.exe` | Ejecutable compilado listo para usar. |

---

## 🏗️ Arquitectura

```mermaid
flowchart LR
    subgraph Usuario
        U[Usuario]
    end

    subgraph GUI [Capa de Presentación - gui.py]
        V[Ventana tkinter]
        B1[Botón: Generar HWID]
        B2[Botón: Copiar]
        E[Entry - Solo lectura]
    end

    subgraph LOGIC [Capa de Lógica - logic.py]
        W1[get_bios_serial]
        W2[get_baseboard_serial]
        W3[get_disk_serial]
        H[generate_hwid<br>SHA-256 → truncado 16 chars]
    end

    subgraph OS [Sistema Operativo Windows]
        WMIC1[wmic bios get serialnumber]
        WMIC2[wmic baseboard get serialnumber]
        WMIC3[wmic diskdrive get serialnumber]
    end

    U --> V
    V --> B1
    V --> B2
    V --> E

    B1 --> H
    H --> W1
    H --> W2
    H --> W3

    W1 --> WMIC1
    W2 --> WMIC2
    W3 --> WMIC3

    WMIC1 --> |Serial BIOS| H
    WMIC2 --> |Serial Placa Base| H
    WMIC3 --> |Serial Disco| H

    H --> |Resultado: HWID| E
    B2 --> |Copia al portapapeles| E

    style GUI fill:#0f3460,color:#fff
    style LOGIC fill:#533483,color:#fff
    style OS fill:#1a1a2e,color:#fff
    style WMIC1 color:#e94560
    style WMIC2 color:#e94560
    style WMIC3 color:#e94560
```

La aplicación sigue una **arquitectura de 3 capas**:

1. **Capa de Presentación** (`gui.py`): Interfaz gráfica construida con tkinter.
2. **Capa de Lógica** (`logic.py`): Contiene toda la lógica de negocio (obtención de datos + hashing).
3. **Capa de Sistema** (Windows API): Consultas `wmic` al sistema operativo.

---

## 🔄 Flujo de Generación del HWID

```mermaid
sequenceDiagram
    actor User as Usuario
    participant GUI as gui.py
    participant Logic as logic.py
    participant WMIC as wmic.exe
    participant Hash as SHA-256

    User->>GUI: Click "Generar HWID"
    GUI->>Logic: generate_hwid()

    Logic->>WMIC: wmic bios get serialnumber
    WMIC-->>Logic: "ABC123"
    Logic->>Logic: Fallback "N/A" si falla

    Logic->>WMIC: wmic baseboard get serialnumber
    WMIC-->>Logic: "MB456"
    Logic->>Logic: Fallback "N/A" si falla

    Logic->>WMIC: wmic diskdrive get serialnumber
    WMIC-->>Logic: "DISK789"
    Logic->>Logic: Fallback "N/A" si falla

    Logic->>Logic: Concatenar: "ABC123-MB456-DISK789"
    Logic->>Hash: SHA-256(concatenación)
    Hash-->>Logic: Hash hexadecimal (64 chars)
    Logic->>Logic: Truncar a 16 caracteres
    Logic-->>GUI: "A1B2C3D4E5F6G7H8"

    GUI-->>User: Muestra HWID en campo readonly

    User->>GUI: Click "Copiar al portapapeles"
    GUI-->>User: "HWID copiado al portapapeles"
```

### Paso a paso

1. El usuario hace clic en **"Generar HWID"**.
2. `logic.py` ejecuta 3 consultas `wmic` para obtener seriales de BIOS, placa base y disco duro.
3. Si alguna consulta falla, se usa `"N/A"` como valor de reemplazo (nunca se interrumpe el proceso).
4. Los 3 valores se concatenan con guiones: `SERIAL_BIOS-SERIAL_BASE-SERIAL_DISCO`.
5. Se calcula el hash **SHA-256** de esa cadena.
6. El resultado se trunca a **16 caracteres hexadecimales**.
7. El HWID se muestra en el campo de texto de solo lectura.
8. El usuario puede copiarlo al portapapeles con el botón **"Copiar"**.

---

## 🧩 Diagrama de Clases

```mermaid
classDiagram
    class HWIDApp {
        -root: Tk
        -entry_hwid: Entry
        +__init__(root)
        +_center_window()
        +_on_generate()
        +_on_copy()
    }

    class logic {
        +_run_wmic_command(command) str
        +get_bios_serial() str
        +get_baseboard_serial() str
        +get_disk_serial() str
        +generate_hwid() str
    }

    class main {
        +main()
    }

    HWIDApp --> logic : llama
    main --> HWIDApp : instancia
    logic --> subprocess : ejecuta wmic
    logic --> hashlib : SHA-256
```

---

## 🖥️ Interfaz Gráfica

La ventana principal se construye con **tkinter** y tiene las siguientes secciones:

```mermaid
flowchart TB
    VENTANA["Ventana Principal 540x220"]

    VENTANA --> TITULO["Titulo:
    Identificador de Hardware (HWID)"]

    VENTANA --> C_HWID["Fila HWID:
    Label 'HWID:' + Entry readonly (Consolas 10)"]

    VENTANA --> BOTONES["Fila Botones"]
    BOTONES --> BTN1["Boton: Generar HWID
    Fondo verde #4CAF50"]
    BOTONES --> BTN2["Boton: Copiar al portapapeles
    Fondo azul #2196F3"]

    VENTANA --> SEP["Separador visual"]

    VENTANA --> INFO["Texto informativo:
    Serial BIOS · Serial Placa Base · Serial Disco Duro"]
```

### Disposición visual

```
┌─────────────────────────────────────────────────────────┐
│         Identificador de Hardware (HWID)                │
│                                                         │
│    HWID: [_______________________________________]     │
│                                                         │
│     [Generar HWID]    [Copiar al portapapeles]          │
│    ─────────────────────────────────────────────         │
│    Basado en: Serial BIOS · Serial Placa Base · Serial  │
│    Disco Duro                                            │
└─────────────────────────────────────────────────────────┘
```

### Características de la interfaz

| Elemento | Descripción |
|----------|-------------|
| **Título** | "Identificador de Hardware (HWID)" en negrita, tamaño 14 |
| **Campo HWID** | Caja de texto con fuente `Consolas`, solo lectura, ancho 55 |
| **Botón Generar** | Fondo verde `#4CAF50`, texto blanco, llama a `generate_hwid()` |
| **Botón Copiar** | Fondo azul `#2196F3`, texto blanco, copia al portapapeles |
| **Texto inferior** | Indica las fuentes del HWID en gris, tamaño 8 |
| **Ventana** | 540x220 píxeles, no redimensionable, centrada en pantalla |

---

## 📦 Compilación a .exe

```mermaid
flowchart LR
    A[main.py] --> B[PyInstaller]
    C[src/logic.py] --> B
    D[src/gui.py] --> B
    B --> E[dist/HWID_Generator.exe]

    B --> F[Flags:]
    F --> G[--onefile<br>Único archivo]
    F --> H[--noconsole<br>Sin terminal]
    F --> I[--name HWID_Generator<br>Nombre salida]
```

### Método 1: Script automatizado

Ejecuta `build_exe.bat` (doble clic o desde terminal):

```bash
cd hwid_generator
build_exe.bat
```

### Método 2: Manual con PyInstaller

```bash
cd hwid_generator
pip install -r requirements.txt
pyinstaller --onefile --noconsole --name HWID_Generator main.py
```

### Resultado

```mermaid
flowchart LR
    A[Código fuente<br>.py] -->|PyInstaller| B[HWID_Generator.exe<br>~7 MB]
    B --> C[Cualquier PC<br>Windows]
    B --> D[Sin Python<br>necesario]
    B --> E[Portátil<br>USB]
```

> **Nota:** El `.exe` incluye Python y todas las dependencias. Puedes llevarlo en un USB y ejecutarlo en cualquier PC con Windows.

---

## 🧪 Prueba del Módulo Lógico

```bash
cd hwid_generator
python -m src.logic
```

Salida esperada:
```
Generando HWID...
HWID Generado: A1B2C3D4E5F6G7H8
```

---

## 🛠️ Manejo de Errores

### Errores en la obtención de hardware (`logic.py`)

```mermaid
flowchart TB
    INICIO["generate_hwid()"] --> BIOS["get_bios_serial()"]

    BIOS --> CHECK1{"wmic responde?"}
    CHECK1 -->|"si"| OK1["Retorna serial obtenido"]
    CHECK1 -->|"no / excepción"| FALLBACK1["Retorna 'N/A'"]

    OK1 --> BASE["get_baseboard_serial()"]
    FALLBACK1 --> BASE

    BASE --> CHECK2{"wmic responde?"}
    CHECK2 -->|"si"| OK2["Retorna serial obtenido"]
    CHECK2 -->|"no / excepción"| FALLBACK2["Retorna 'N/A'"]

    OK2 --> DISK["get_disk_serial()"]
    FALLBACK2 --> DISK

    DISK --> CHECK3{"wmic responde?"}
    CHECK3 -->|"si"| OK3["Retorna serial obtenido"]
    CHECK3 -->|"no / excepción"| FALLBACK3["Retorna 'N/A'"]

    OK3 --> CHECK_TODO{"Todos son 'N/A'?"}
    FALLBACK3 --> CHECK_TODO

    CHECK_TODO -->|"si"| ERROR["Retorna mensaje de error"]
    CHECK_TODO -->|"no"| HASH["SHA-256 → truncado 16 chars"]
    HASH --> HWID["HWID generado correctamente"]
```

### Errores en la interfaz gráfica (`gui.py`)

```mermaid
flowchart TB
    USUARIO["Usuario"] --> CLICK_GENERAR["Click 'Generar HWID'"]

    CLICK_GENERAR --> TRY{"try: generate_hwid()"}
    TRY -->|"éxito"| MOSTRAR["Muestra HWID en campo readonly"]
    TRY -->|"error"| MSGBOX_ERROR["messagebox.showerror()
    Muestra error al usuario"]

    USUARIO --> CLICK_COPIAR["Click 'Copiar al portapapeles'"]
    CLICK_COPIAR --> CHECK_HWID{"Campo HWID tiene texto?"}
    CHECK_HWID -->|"si"| COPIAR["Copia al portapapeles
    messagebox.showinfo('Copiado')"]
    CHECK_HWID -->|"no"| ADVERTENCIA["messagebox.showwarning
    'Primero genera un HWID'"]
```

### Casos contemplados y su comportamiento

| Escenario | ¿Dónde ocurre? | Comportamiento |
|-----------|---------------|---------------|
| `wmic` no está disponible en el sistema | `logic.py` | `try/except` captura `FileNotFoundError`, retorna `None` → se asigna `"N/A"` |
| Serial de BIOS vacío | `logic.py` | `get_bios_serial()` retorna `"N/A"` |
| Serial de placa base vacío | `logic.py` | `get_baseboard_serial()` retorna `"N/A"` |
| Serial de disco duro vacío | `logic.py` | `get_disk_serial()` retorna `"N/A"` |
| Los 3 seriales fallan (todos `"N/A"`) | `logic.py` | `generate_hwid()` retorna `"ERROR: No se pudieron obtener suficientes datos de hardware"` |
| Error inesperado al generar HWID | `gui.py` | `messagebox.showerror()` muestra el detalle de la excepción al usuario |
| Usuario hace clic en "Copiar" sin HWID generado | `gui.py` | `messagebox.showwarning()` informa que primero debe generar un HWID |

---

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y distribuirlo.

---
