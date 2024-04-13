from proxmoxer import ProxmoxAPI
import getpass

# Configuración de la API de Proxmox
PROXMOX_HOST = '10.100.0.5'
PROXMOX_USER = 'root@pam'

# Solicitar la contraseña de Proxmox de forma segura
PROXMOX_PASSWORD = getpass.getpass("Contraseña Proxmox: ")

def main():
    # Inicializar la conexión a la API de Proxmox
    proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')
    
    # Solicitar los datos de la máquina virtual
    vm_id = input("ID de la máquina virtual: ")
    vm_name = input("Nombre de la máquina virtual: ")
    ram = input("RAM (MB): ")
    cores = input("Número de procesadores (cores): ")
    hdd = input("Capacidad del disco duro (GB): ")
    red = input("Red (puente): ")

    try:
        # Crear la máquina virtual con almacenamiento iso en lugar de local
        proxmox.nodes('test').qemu.create(
            vmid=vm_id,
            name=vm_name,
            memory=ram,
            cores=cores,
            sockets=cores,
            ostype='l26',
            scsi0='iso:{}'.format(hdd),
            net0='virtio,bridge={}'.format(red)
        )
        print("¡La máquina virtual fue desplegada con éxito!")
    except Exception as e:
        print("Hubo un error al desplegar la máquina virtual. Detalles del error:")
        print(e)

if __name__ == "__main__":
    main()
