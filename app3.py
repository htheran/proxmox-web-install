from flask import Flask, render_template, request
from proxmoxer import ProxmoxAPI
import getpass

app = Flask(__name__)

# Configuración de la API de Proxmox
PROXMOX_HOST = '10.100.0.5'
PROXMOX_USER = 'root@pam'

# Solicitar la contraseña de Proxmox de forma segura
PROXMOX_PASSWORD = getpass.getpass("Contraseña Proxmox: ")

def deploy_vm(vm_id, vm_name, ram, cores, hdd, red):
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
            scsi0='iso:{}'.format(hdd),
            net0='virtio,bridge={}'.format(red)
        )
        return True
    except Exception as e:
        print("Hubo un error al desplegar la máquina virtual. Detalles del error:")
        print(e)
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    vm_id = request.form['vm_id']
    vm_name = request.form['vm_name']
    ram = request.form['ram']
    cores = request.form['cores']
    hdd = request.form['hdd']
    red = request.form['red']

    if deploy_vm(vm_id, vm_name, ram, cores, hdd, red):
        # Pasar los detalles de la máquina virtual a la plantilla
        message = {
            'vmid': vm_id,
            'name': vm_name,
            'ram': ram,
            'cores': cores,
            'hdd': hdd,
            'red': red
        }
        return render_template('result.html', message=message)
    else:
        return "Hubo un error al desplegar la máquina virtual."

if __name__ == '__main__':
    app.run(host='0.0.0.0')

