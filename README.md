# DHCP Starvation Attack Script
**Autor:** Jonathan Sención  
**Matrícula:** 20250851  
**Institución:** ITLA - Instituto Tecnológico de las Américas  

---

## Objetivo del Laboratorio
Demostrar cómo un atacante puede agotar el pool de direcciones IP de un servidor DHCP 
legítimo enviando solicitudes DHCP masivas con MACs aleatorias, dejando a los clientes 
legítimos sin poder obtener una dirección IP.

---

## Objetivo del Script
Generar miles de paquetes DHCP Discover con MACs falsas y aleatorias para agotar 
completamente el pool de IPs del servidor DHCP, causando una denegación de servicio 
a los clientes legítimos de la red.

### Parámetros Usados
| Parámetro | Valor | Descripción |
|---|---|---|
| `src` | `RandMAC()` | MAC aleatoria por paquete |
| `dst` | `ff:ff:ff:ff:ff:ff` | Broadcast Ethernet |
| `src IP` | `0.0.0.0` | IP origen (cliente sin IP) |
| `dst IP` | `255.255.255.255` | Broadcast IP |
| `sport` | `68` | Puerto cliente DHCP |
| `dport` | `67` | Puerto servidor DHCP |
| `iface` | `eth0` | Interfaz de red atacante |

### Requisitos
- Kali Linux
- Python 3
- Scapy (`sudo apt install python3-scapy`)
- Ejecutar como root (`sudo`)

---

## Funcionamiento del Script
1. Se genera una MAC aleatoria diferente por cada paquete
2. Se construye un DHCP Discover completo con esa MAC
3. El servidor DHCP reserva una IP para cada MAC recibida
4. El pool de IPs se agota rápidamente
5. Los clientes legítimos reciben `Can't find DHCP server`

---

## Topología de Red
[Kali Atacante] eth0 ──── e0/2 [SW1] e0/0 ──── e0/0 [SW2] e0/1 ──── eth0 [VPC1]
192.168.85.10                10.20.25.1              10.20.25.2         192.168.85.20
│
e0/1 └──── e0/0 [SW3] e0/1 ──── eth0 [VPC2]
10.20.25.3         192.168.51.20

### VLANs
| VLAN | Nombre | Red |
|---|---|---|
| VLAN 10 | VLAN10-20250851 | 192.168.85.0/24 |
| VLAN 20 | VLAN20-20250851 | 192.168.51.0/24 |
| Management | MGMT | 10.20.25.0/24 |

---

## Ejecución
```bash
sudo python3 dhcp_starvation.py
```

### Verificación del Ataque
En Wireshark filtrar:
bootp
En VPC1:
dhcp
Debe fallar con `Can't find DHCP server`.

En SW1:
show mac address-table count

---

## Capturas de Pantalla
<img width="641" height="599" alt="image" src="https://github.com/user-attachments/assets/d9f66b28-0042-4225-bb05-4c33a793fceb" />

<img width="765" height="333" alt="image" src="https://github.com/user-attachments/assets/41047186-707d-4a03-8c6b-2b55afb4783f" />

<img width="637" height="397" alt="image" src="https://github.com/user-attachments/assets/1cab159a-1caa-4f32-a5cc-a9d4f27b7b0f" />

---

## Contramedidas
### 1. DHCP Snooping con límite de rate
ip dhcp snooping
ip dhcp snooping vlan 10
interface e0/2
ip dhcp snooping limit rate 15
interface e0/0
ip dhcp snooping trust
### 2. Port Security
interface e0/2
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address sticky
switchport port-security violation shutdown
### 3. Verificación
show ip dhcp snooping statistics
show port-security interface e0/2
