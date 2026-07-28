# Enterprise Zero-Trust Network Architecture & Security Implementation

## 📌 Project Overview
This project demonstrates the design and implementation of a secure, enterprise-grade Local Area Network (LAN) utilizing Zero-Trust principles. The architecture is built upon Cisco routing and switching technologies, focusing on strict logical isolation, physical layer security, and traffic filtering to mitigate common internal and external cyber threats.

## 🏗️ Topology & Architecture
The network follows a hierarchical model consisting of a Core Layer (L3 Routing) and an Access Layer (L2 Switching), terminating at an Edge Router.

*   **Core Switch (`CSW-CORE-01`):** Acts as the L3 backbone, handling Inter-VLAN routing and enforcing initial security boundaries.
*   **Access Switches (`ASW-FLOOR-01`, `ASW-SERVER-01`):** Distributes end-user and server connectivity with strict physical port security.
*   **Edge Router (`RTR-EDGE-01`):** Serves as the primary gateway, connected via a /30 transit network to the Core Switch.

### VLAN Scheme
| VLAN ID | Name | Subnet | Gateway (SVI) | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **10** | `IT_MGMT` | 10.0.10.0/24 | 10.0.10.1 | IT Department |
| **20** | `STAFF` | 10.0.20.0/24 | 10.0.20.1 | General Employees |
| **30** | `GUEST` | 10.0.30.0/24 | 10.0.30.1 | Guest Access |
| **99** | `DMZ` | 10.0.99.0/24 | 10.0.99.1 | Server Infrastructure |
| **999** | `BLACKHOLE`| N/A | N/A | Security (Native VLAN) |

## 🛡️ Cybersecurity Implementations

This lab specifically addresses L2 and L3 attack vectors through the following configurations:

### 1. Mitigation of VLAN Hopping
*   **Disabled DTP:** Dynamic Trunking Protocol is disabled (`switchport nonegotiate`) on all trunk links to prevent attackers from negotiating trunk states.
*   **Native VLAN Blackholing:** The default Native VLAN 1 is administratively moved to an unused, unrouted VLAN (VLAN 999). This prevents 802.1Q double-tagging attacks.

### 2. Physical Layer Security (Zero-Trust Access)
*   **Port Security:** Implemented on all active access ports (`switchport port-security`).
*   **MAC Limiting & Sticky:** Restricted to a single MAC address per port (`maximum 1`). Addresses are dynamically learned and saved to the running config (`mac-address sticky`).
*   **Violation Enforcement:** Unauthorized device connections immediately trigger an `err-disable` state (`violation shutdown`).
*   **Port Shutdown:** All unused switch ports are administratively shut down to prevent unauthorized physical network access.

### 3. Traffic Filtering and Access Control Lists (ACL)
*   **Guest Isolation:** An Extended IPv4 Access Control List (`GUEST_SECURITY`) is applied inbound on the Guest SVI (VLAN 30).
*   **Rule Set:** The Guest network is explicitly denied access to IT, STAFF, and DMZ subnets, while permitted standard outbound internet traffic.

## 🚀 How to Run (Packet Tracer)
1. Download the `Zero_Trust_Architecture.pkt` file from this repository.
2. Open with Cisco Packet Tracer.
3. Test connectivity: PCs within the same VLAN can ping each other.
4. Test Security: Connect a rogue laptop to `ASW-FLOOR-01`; observe the port transitioning to a shutdown state.

## 🛠️ Technologies & Protocols
*   **Routing:** Static Routing, Inter-VLAN Routing (SVI)
*   **Switching:** 802.1Q Trunking, VTP (Transparent), Access Ports
*   **Security:** ACLs, Port Security, DTP Disabling, Native VLAN isolation
