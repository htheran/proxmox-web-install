from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(
    "10.100.0.5", user="root@pam", password="Pr0l1ant", verify_ssl=False
)

# Obtener una lista de nodos
nodes = proxmox.nodes.get()

# Iterar sobre los nodos y obtener una lista de máquinas virtuales en cada nodo
for node in nodes:
    print(f"Máquinas virtuales en el nodo {node['node']}:")
    vms = proxmox.nodes(node['node']).qemu.get()
    for vm in vms:
        print(f"  - VM ID: {vm['vmid']}, Nombre: {vm['name']}, Estado: {vm['status']}")

