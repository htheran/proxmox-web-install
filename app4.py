from proxmoxer import ProxmoxAPI
import getpass

# Configuración de la API de Proxmox
PROXMOX_HOST = '10.100.0.5'
PROXMOX_USER = 'root@pam'

# Configuración por defecto
DEFAULT_DISK_SIZE = '20'
DEFAULT_RAM = '2048'
DEFAULT_CORES = '2'
DEFAULT_NETWORK = 'vmbr0'

# Solicitar la contraseña de Proxmox de forma segura
PROXMOX_PASSWORD = getpass.getpass("Contraseña Proxmox: ")

def get_next_vm_id():
    # Inicializar la conexión a la API de Proxmox
    proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')

    try:
        # Consultar VM ID más alto
        max_vm_id = max([int(vm['vmid']) for vm in proxmox.cluster.resources.get(type='vm')])
        return str(max_vm_id + 1)
    except Exception as e:
        print("Hubo un error al consultar el próximo VM ID. Detalles del error:")
        print(e)
        return None

def get_networks():
    # Inicializar la conexión a la API de Proxmox
    proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')

    try:
        # Consultar redes disponibles
        networks = [net['iface'] for net in proxmox.nodes('test').network.get()]
        return networks
    except Exception as e:
        print("Hubo un error al consultar las redes disponibles. Detalles del error:")
        print(e)
        return None

def deploy_vm(vm_name, ram=DEFAULT_RAM, cores=DEFAULT_CORES, disk_size=DEFAULT_DISK_SIZE, network=DEFAULT_NETWORK):
    # Obtener el próximo VM ID disponible
    vm_id = get_next_vm_id()
    if vm_id is None:
        return False

    # Inicializar la conexión a la API de Proxmox
    proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')
    
    try:
        # Crear la máquina virtual con almacenamiento iso en lugar de local
        proxmox.nodes('test').qemu.create(
            vmid=vm_id,
            name=vm_name,
            memory=ram,
            cores=cores,
            sockets=cores,
            ostype='l26',
            scsi0='local-lvm:{},size={}'.format(disk_size, disk_size),
            net0='virtio,bridge={}'.format(network)
        )
        return vm_id
    except Exception as e:
        print("Hubo un error al desplegar la máquina virtual. Detalles del error:")
        print(e)
        return None

def main():
    print("Bienvenido a la aplicación de despliegue de VMs.")
    
    # Listar las redes disponibles
    networks = get_networks()
    if networks is None:
        print("No se pudieron obtener las redes disponibles. Saliendo del programa.")
        return

    print("Redes disponibles:")
    for i, net in enumerate(networks, start=1):
        print(f"{i}. {net}")

    # Solicitar al usuario que seleccione una red
    while True:
        try:
            selected_network_index = int(input("Por favor, seleccione el número de la red deseada: ")) - 1
            selected_network = networks[selected_network_index]
            break
        except (ValueError, IndexError):
            print("Selección inválida. Intente de nuevo.")

    # Desplegar la VM con los valores por defecto y la red seleccionada
    vm_name = input("Ingrese el nombre de la VM: ")
    vm_id = deploy_vm(vm_name, network=selected_network)

    if vm_id is not None:
        # Mostrar los detalles de la VM desplegada
        print("\nLa VM se ha desplegado exitosamente con los siguientes detalles:")
        print(f"VM ID: {vm_id}")
        print(f"Nombre: {vm_name}")
        print(f"RAM: {DEFAULT_RAM} MB")
        print(f"Núcleos: {DEFAULT_CORES}")
        print(f"Disco: {DEFAULT_DISK_SIZE} GB")
        print(f"Red: {selected_network}")
    else:
        print("Hubo un error al desplegar la máquina virtual.")

if __name__ == '__main__':
    main()
