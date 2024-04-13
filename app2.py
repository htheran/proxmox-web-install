from flask import Flask, render_template, request
from proxmoxer import ProxmoxAPI
import getpass

app = Flask(__name__)

# Configuración de la API de Proxmox
PROXMOX_HOST = '10.100.0.5'
PROXMOX_USER = 'root@pam'

# Solicitar la contraseña de Proxmox de forma segura
PROXMOX_PASSWORD = getpass.getpass("Contraseña Proxmox: ")

proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy_vm():
    vm_id = request.form['vm_id']
    vm_name = request.form['vm_name']
    ram = request.form['ram']
    cores = request.form['cores']
    hdd = request.form['hdd']
    red = request.form['red']
    
    try:
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
        message = "¡La máquina virtual {} fue desplegada con éxito!".format(vm_name)
    except Exception as e:
        message = "Hubo un error al desplegar la máquina virtual. Detalles del error: {}".format(e)
    
    return render_template('result.html', message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
