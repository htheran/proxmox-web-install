import requests

# Endpoint de la API de Proxmox
PROXMOX_API_URL = "https://10.100.0.5:8006/api2/json/"

def deploy_vm():
    # Datos de autenticación
    usuario = "root@pam"
    contrasena = "tokentest"
    token = "668f27c4-e4f3-404b-a2e3-abbc8a8c6022"

    # Obtener datos de la máquina virtual desde la consola
    vm_id = input("ID de la máquina virtual: ")
    nombre_vm = input("Nombre de la máquina virtual: ")
    ram = input("RAM (MB): ")
    procesador = input("Número de procesadores (cores): ")
    hdd = input("Capacidad del disco duro (GB): ")
    red = input("Red (puente): ")

    # Construir la solicitud para la API de Proxmox
    payload = {
        "vmid": vm_id,
        "vmname": nombre_vm,
        "memory": ram,
        "cores": procesador,
        "sockets": procesador,
        "ostype": "l26",
        "ide": "local",
        "scsi": "virtio",
        "virtio0": f"local:{hdd}",
        "net0": f"virtio,bridge={red}",
        "skipinst": "1",
        "ticket": token  # Pasar el token como parámetro de consulta
    }

    # Imprimir el encabezado
    print("Encabezado de la solicitud:")
    print(payload)

    # Enviar la solicitud a la API de Proxmox
    response = requests.post(PROXMOX_API_URL + 'nodes/test/qemu', json=payload, verify=False)
    print(response.content)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        print("¡La máquina virtual fue desplegada con éxito!")
    else:
        print("Hubo un error al desplegar la máquina virtual. Detalles del error:")
        print(response.text)

if __name__ == '__main__':
    print("Creación de una nueva máquina virtual en Proxmox")
    print("Por favor, proporcione los siguientes datos:")
    deploy_vm()
