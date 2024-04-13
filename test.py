from proxmoxer import ProxmoxAPI

# Crear una instancia de ProxmoxAPI
proxmox = ProxmoxAPI(
    "10.100.0.5:8006", user="root@pam", password="Pr0l1ant", verify_ssl=False
)

try:
    for vm in proxmox.nodes("node1").qemu.get(timeout=550):
        print(vm)
except Exception as e:
    print("Error al consultar la API:", e)


