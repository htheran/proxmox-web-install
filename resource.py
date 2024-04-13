from proxmoxer import ProxmoxAPI

# Datos de autenticación y configuración de Proxmox
PROXMOX_HOST = "10.100.0.5"
PROXMOX_USER = "root@pam"
PROXMOX_PASSWORD = "Pr0l1ant"  # Reemplaza con tu contraseña
PROXMOX_REALM = "pam"

# Inicializar la conexión con Proxmox
proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASSWORD, verify_ssl=False, backend='https')

# Obtener información de los nodos
for node in proxmox.nodes.get():
    print(f"Nodo: {node['node']}, Estado: {node['status']}")
