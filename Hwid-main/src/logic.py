import subprocess
import hashlib

def _run_wmic_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_lines = result.stdout.strip().split('\n')
        if len(output_lines) > 1:
            return output_lines[1].strip()
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_bios_serial():
    serial = _run_wmic_command(["wmic", "bios", "get", "serialnumber"])
    return serial if serial else "N/A"

def get_baseboard_serial():
    serial = _run_wmic_command(["wmic", "baseboard", "get", "serialnumber"])
    return serial if serial else "N/A"

def get_disk_serial():
    serial = _run_wmic_command(["wmic", "diskdrive", "get", "serialnumber"])
    return serial if serial else "N/A"

def generate_hwid():
    bios_serial = get_bios_serial()
    baseboard_serial = get_baseboard_serial()
    disk_serial = get_disk_serial()

    combined_string = f"{bios_serial}-{baseboard_serial}-{disk_serial}"
    if not any([bios_serial, baseboard_serial, disk_serial]):
        return "ERROR: No se pudieron obtener suficientes datos de hardware."

    hwid = hashlib.sha256(combined_string.encode('utf-8')).hexdigest().upper()
    return hwid[:16]

if __name__ == "__main__":
    print("Generando HWID...")
    hwid = generate_hwid()
    print(f"HWID Generado: {hwid}")