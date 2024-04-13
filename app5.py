from flask import Flask, render_template, request
from proxmoxer import ProxmoxAPI
import getpass

app = Flask(__name__)

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

@app.route('/')
def index():
    networks = get_networks()
    return render_template('despliegue.html', networks=networks)

@app.route('/deploy', methods=['POST'])
def deploy():
    vm_name = request.form['vm_name']
    ram = request.form.get('ram', DEFAULT_RAM)
    cores = request.form.get('cores', DEFAULT_CORES)
    disk_size = request.form.get('disk_size', DEFAULT_DISK_SIZE)
    network = request.form['network']

    vm_id = deploy_vm(vm_name, ram, cores, disk_size, network)

    if vm_id is not None:
        return render_template('resultado.html', vm_id=vm_id, vm_name=vm_name, ram=ram, cores=cores, disk_size=disk_size, network=network)
    else:
        return "Hubo un error al desplegar la máquina virtual."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
