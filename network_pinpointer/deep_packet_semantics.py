#!/usr/bin/env python3
"""
Deep Packet Semantic Analysis - Experimental Module

This module moves beyond metadata interpretation to discover and imbue
semantic meaning at the individual packet level.

Instead of inferring LJPW from aggregate metrics, we analyze each packet's
actual communication intent and assign semantic coordinates based on what
the packet is truly trying to accomplish.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

try:
    from .semantic_engine import Coordinates
except ImportError:
    # Running as main for testing
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from network_pinpointer.semantic_engine import Coordinates


class SemanticIntent(Enum):
    """Fundamental semantic intents in network communication"""
    CONNECTION_ESTABLISHMENT = "connection_establishment"  # Love
    INFORMATION_REQUEST = "information_request"            # Wisdom
    INFORMATION_RESPONSE = "information_response"          # Wisdom
    AUTHENTICATION = "authentication"                      # Justice
    AUTHORIZATION = "authorization"                        # Justice
    DATA_TRANSFER = "data_transfer"                        # Power
    POLICY_ENFORCEMENT = "policy_enforcement"              # Justice
    CONNECTION_MAINTENANCE = "connection_maintenance"      # Love
    CONNECTION_TERMINATION = "connection_termination"      # Love (negative)
    SECURITY_NEGOTIATION = "security_negotiation"          # Justice
    SERVICE_DISCOVERY = "service_discovery"                # Wisdom
    ERROR_SIGNALING = "error_signaling"                    # Varies


@dataclass
class PacketSemantics:
    """Semantic analysis of a single packet"""
    timestamp: datetime
    packet_num: int

    # Network layer info
    src_ip: str
    dst_ip: str
    protocol: str
    size: int

    # Semantic classification
    intent: SemanticIntent
    ljpw_coordinates: Coordinates

    # Detailed analysis
    layer7_protocol: Optional[str] = None
    semantic_description: str = ""
    confidence: float = 1.0

    # Flow context
    flow_id: Optional[str] = None
    flow_position: Optional[int] = None


@dataclass
class SemanticFlow:
    """Aggregate semantics of a communication flow"""
    flow_id: str
    start_time: datetime
    end_time: Optional[datetime]

    src_ip: str
    dst_ip: str

    packets: List[PacketSemantics]
    aggregate_ljpw: Coordinates

    dominant_intent: SemanticIntent
    flow_pattern: str  # e.g., "API Query", "File Transfer", "Auth Flow"


class DeepPacketSemanticAnalyzer:
    """
    Analyzes packets at payload level to discover inherent semantic meaning

    This goes beyond metadata interpretation to understand what each packet
    is actually trying to communicate.
    """

    def __init__(self):
        self.flows: Dict[str, SemanticFlow] = {}
        self.packet_count = 0

    def analyze_packet(self, packet_data: bytes, metadata: Dict) -> PacketSemantics:
        """
        Analyze a single packet and imbue it with semantic meaning

        Args:
            packet_data: Raw packet bytes
            metadata: Metadata from packet capture (IPs, ports, protocol, etc.)

        Returns:
            PacketSemantics with LJPW coordinates based on actual intent
        """
        self.packet_count += 1

        # Determine semantic intent from packet contents
        intent = self._determine_intent(packet_data, metadata)

        # Calculate LJPW coordinates based on intent
        ljpw = self._calculate_packet_ljpw(intent, packet_data, metadata)

        # Generate semantic description
        description = self._describe_packet_semantics(intent, metadata)

        # Detect layer 7 protocol
        l7_protocol = self._detect_layer7_protocol(packet_data, metadata)

        return PacketSemantics(
            timestamp=datetime.now(),
            packet_num=self.packet_count,
            src_ip=metadata.get('src_ip', 'unknown'),
            dst_ip=metadata.get('dst_ip', 'unknown'),
            protocol=metadata.get('protocol', 'unknown'),
            size=len(packet_data),
            intent=intent,
            ljpw_coordinates=ljpw,
            layer7_protocol=l7_protocol,
            semantic_description=description,
            confidence=self._calculate_confidence(intent, packet_data, metadata)
        )

    def _determine_intent(self, packet_data: bytes, metadata: Dict) -> SemanticIntent:
        """Determine the semantic intent of this packet"""

        protocol = metadata.get('protocol', '').upper()
        flags = metadata.get('tcp_flags', {})
        dst_port = metadata.get('dst_port', 0)

        # TCP Connection establishment
        if protocol == 'TCP' and flags.get('SYN') and not flags.get('ACK'):
            return SemanticIntent.CONNECTION_ESTABLISHMENT

        # TCP Connection termination
        if protocol == 'TCP' and (flags.get('FIN') or flags.get('RST')):
            return SemanticIntent.CONNECTION_TERMINATION

        # DNS queries - pure information seeking
        if protocol == 'UDP' and dst_port == 53:
            return SemanticIntent.INFORMATION_REQUEST

        # HTTP/HTTPS detection
        if self._is_http_request(packet_data):
            http_method = self._extract_http_method(packet_data)
            if http_method in ['GET', 'HEAD', 'OPTIONS']:
                return SemanticIntent.INFORMATION_REQUEST
            elif http_method in ['POST', 'PUT', 'PATCH']:
                # Check if auth endpoint
                if self._is_auth_endpoint(packet_data):
                    return SemanticIntent.AUTHENTICATION
                else:
                    return SemanticIntent.DATA_TRANSFER
            elif http_method == 'DELETE':
                return SemanticIntent.AUTHORIZATION  # Need permission to delete

        # TLS/SSL handshake - security negotiation
        if self._is_tls_handshake(packet_data):
            return SemanticIntent.SECURITY_NEGOTIATION

        # Large data transfers
        if len(packet_data) > 1400:  # Near MTU
            return SemanticIntent.DATA_TRANSFER

        # TCP ACK-only packets (connection maintenance)
        if protocol == 'TCP' and flags.get('ACK') and len(packet_data) < 100:
            return SemanticIntent.CONNECTION_MAINTENANCE

        # ICMP errors
        if protocol == 'ICMP':
            icmp_type = metadata.get('icmp_type', -1)
            if icmp_type in [3, 4, 5, 11]:  # Dest unreachable, source quench, redirect, time exceeded
                return SemanticIntent.ERROR_SIGNALING

        # Default: data transfer
        return SemanticIntent.DATA_TRANSFER

    def _calculate_packet_ljpw(
        self,
        intent: SemanticIntent,
        packet_data: bytes,
        metadata: Dict
    ) -> Coordinates:
        """
        Calculate LJPW coordinates based on packet's semantic intent

        This is where we IMBUE meaning - each intent has inherent semantic coordinates
        """

        # Base coordinates for each intent type
        intent_semantics = {
            SemanticIntent.CONNECTION_ESTABLISHMENT: {
                'love': 1.0,    # PURE connectivity attempt
                'justice': 0.3, # Some security context
                'power': 0.1,   # Minimal resources
                'wisdom': 0.2   # Minimal information
            },
            SemanticIntent.INFORMATION_REQUEST: {
                'love': 0.7,    # Seeking connection
                'justice': 0.2, # Minimal policy
                'power': 0.3,   # Low resource usage
                'wisdom': 0.9   # HIGH information seeking
            },
            SemanticIntent.INFORMATION_RESPONSE: {
                'love': 0.8,    # Providing response
                'justice': 0.2, # Minimal policy
                'power': 0.5,   # Medium resources (sending data)
                'wisdom': 0.9   # HIGH information content
            },
            SemanticIntent.AUTHENTICATION: {
                'love': 0.6,    # Establishing trust
                'justice': 0.9, # HIGH policy enforcement
                'power': 0.3,   # Low resources
                'wisdom': 0.5   # Credentials = information
            },
            SemanticIntent.AUTHORIZATION: {
                'love': 0.4,    # Checking permission
                'justice': 1.0, # PURE policy check
                'power': 0.2,   # Minimal resources
                'wisdom': 0.4   # Access info
            },
            SemanticIntent.DATA_TRANSFER: {
                'love': 0.8,    # Active connection
                'justice': 0.2, # Minimal policy
                'power': 0.9,   # HIGH resource usage
                'wisdom': 0.5   # Payload content
            },
            SemanticIntent.POLICY_ENFORCEMENT: {
                'love': 0.0,    # Blocking connection
                'justice': 1.0, # PURE policy
                'power': 0.0,   # No resources allowed
                'wisdom': 0.3   # Limited metadata
            },
            SemanticIntent.CONNECTION_MAINTENANCE: {
                'love': 0.9,    # Keeping connection alive
                'justice': 0.1, # No policy
                'power': 0.1,   # Minimal resources
                'wisdom': 0.2   # Keepalive metadata
            },
            SemanticIntent.CONNECTION_TERMINATION: {
                'love': 0.2,    # Ending connection
                'justice': 0.2, # Graceful close
                'power': 0.1,   # Minimal resources
                'wisdom': 0.3   # Termination metadata
            },
            SemanticIntent.SECURITY_NEGOTIATION: {
                'love': 0.6,    # Establishing secure connection
                'justice': 0.8, # HIGH security policy
                'power': 0.4,   # Crypto overhead
                'wisdom': 0.6   # Cipher/cert metadata
            },
            SemanticIntent.SERVICE_DISCOVERY: {
                'love': 0.7,    # Finding services
                'justice': 0.2, # Minimal policy
                'power': 0.2,   # Small packets
                'wisdom': 0.9   # HIGH discovery information
            },
            SemanticIntent.ERROR_SIGNALING: {
                'love': 0.3,    # Communication problem
                'justice': 0.5, # May indicate policy block
                'power': 0.2,   # Error packet
                'wisdom': 0.6   # Error information
            }
        }

        base = intent_semantics.get(intent, {
            'love': 0.5, 'justice': 0.5, 'power': 0.5, 'wisdom': 0.5
        })

        # Adjust based on packet characteristics
        love = base['love']
        justice = base['justice']
        power = base['power']
        wisdom = base['wisdom']

        # Large packets increase Power
        if len(packet_data) > 1000:
            power = min(1.0, power + 0.2)

        # Encrypted traffic increases Justice
        if self._is_encrypted(packet_data, metadata):
            justice = min(1.0, justice + 0.2)

        # Rich protocol metadata increases Wisdom
        if metadata.get('layer7_info'):
            wisdom = min(1.0, wisdom + 0.1)

        return Coordinates(
            love=love,
            justice=justice,
            power=power,
            wisdom=wisdom
        )

    def _describe_packet_semantics(self, intent: SemanticIntent, metadata: Dict) -> str:
        """Generate human-readable semantic description"""

        descriptions = {
            SemanticIntent.CONNECTION_ESTABLISHMENT: "Attempting to establish connection (Love=1.0)",
            SemanticIntent.INFORMATION_REQUEST: "Seeking information (Wisdom=0.9)",
            SemanticIntent.INFORMATION_RESPONSE: "Providing requested information (Wisdom=0.9)",
            SemanticIntent.AUTHENTICATION: "Authenticating identity (Justice=0.9)",
            SemanticIntent.AUTHORIZATION: "Checking access permission (Justice=1.0)",
            SemanticIntent.DATA_TRANSFER: "Transferring data (Power=0.9)",
            SemanticIntent.POLICY_ENFORCEMENT: "Enforcing network policy (Justice=1.0)",
            SemanticIntent.CONNECTION_MAINTENANCE: "Maintaining active connection (Love=0.9)",
            SemanticIntent.CONNECTION_TERMINATION: "Terminating connection",
            SemanticIntent.SECURITY_NEGOTIATION: "Negotiating security parameters (Justice=0.8)",
            SemanticIntent.SERVICE_DISCOVERY: "Discovering available services (Wisdom=0.9)",
            SemanticIntent.ERROR_SIGNALING: "Signaling error condition"
        }

        return descriptions.get(intent, "Unknown semantic intent")

    def _is_http_request(self, data: bytes) -> bool:
        """Check if packet contains HTTP request"""
        try:
            text = data[:100].decode('utf-8', errors='ignore')
            return any(text.startswith(method) for method in
                      ['GET ', 'POST ', 'PUT ', 'DELETE ', 'HEAD ', 'OPTIONS ', 'PATCH '])
        except:
            return False

    def _extract_http_method(self, data: bytes) -> Optional[str]:
        """Extract HTTP method from packet"""
        try:
            text = data[:100].decode('utf-8', errors='ignore')
            for method in ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']:
                if text.startswith(method):
                    return method
        except:
            pass
        return None

    def _is_auth_endpoint(self, data: bytes) -> bool:
        """Check if HTTP request is to authentication endpoint"""
        try:
            text = data[:500].decode('utf-8', errors='ignore').lower()
            auth_patterns = ['/auth', '/login', '/oauth', '/token', '/signin', 'authenticate']
            return any(pattern in text for pattern in auth_patterns)
        except:
            return False

    def _is_tls_handshake(self, data: bytes) -> bool:
        """Check if packet is TLS handshake"""
        if len(data) < 6:
            return False
        # TLS record: type (22=handshake), version (0x03, 0x01-0x04)
        return data[0] == 0x16 and data[1] == 0x03 and data[2] in [0x01, 0x02, 0x03, 0x04]

    def _is_encrypted(self, data: bytes, metadata: Dict) -> bool:
        """Check if packet appears to be encrypted"""
        dst_port = metadata.get('dst_port', 0)
        # Common encrypted ports
        if dst_port in [443, 22, 3389, 8443]:
            return True
        # Check for TLS
        if self._is_tls_handshake(data):
            return True
        return False

    def _detect_layer7_protocol(self, data: bytes, metadata: Dict) -> Optional[str]:
        """Detect application layer protocol"""
        dst_port = metadata.get('dst_port', 0)

        # Port-based detection
        port_protocols = {
            80: 'HTTP',
            443: 'HTTPS',
            53: 'DNS',
            22: 'SSH',
            25: 'SMTP',
            110: 'POP3',
            143: 'IMAP',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            6379: 'Redis',
            27017: 'MongoDB'
        }

        if dst_port in port_protocols:
            return port_protocols[dst_port]

        # Content-based detection
        if self._is_http_request(data):
            return 'HTTP'
        if self._is_tls_handshake(data):
            return 'TLS'

        return metadata.get('protocol', 'Unknown')

    def _calculate_confidence(self, intent: SemanticIntent, data: bytes, metadata: Dict) -> float:
        """Calculate confidence in semantic classification"""
        confidence = 1.0

        # Lower confidence for ambiguous packets
        if intent == SemanticIntent.DATA_TRANSFER and len(data) < 100:
            confidence = 0.6

        # High confidence for protocol-specific intents
        if intent in [SemanticIntent.CONNECTION_ESTABLISHMENT,
                     SemanticIntent.AUTHENTICATION,
                     SemanticIntent.SECURITY_NEGOTIATION]:
            confidence = 0.95

        return confidence

    def track_flow(self, packet_semantics: PacketSemantics):
        """Track packet as part of a semantic flow"""
        flow_id = f"{packet_semantics.src_ip}:{packet_semantics.dst_ip}"

        if flow_id not in self.flows:
            self.flows[flow_id] = SemanticFlow(
                flow_id=flow_id,
                start_time=packet_semantics.timestamp,
                end_time=None,
                src_ip=packet_semantics.src_ip,
                dst_ip=packet_semantics.dst_ip,
                packets=[],
                aggregate_ljpw=Coordinates(0, 0, 0, 0),
                dominant_intent=packet_semantics.intent,
                flow_pattern="Unknown"
            )

        flow = self.flows[flow_id]
        flow.packets.append(packet_semantics)
        flow.end_time = packet_semantics.timestamp

        # Recalculate aggregate LJPW
        flow.aggregate_ljpw = self._calculate_flow_ljpw(flow)

        # Determine flow pattern
        flow.flow_pattern = self._classify_flow_pattern(flow)
        flow.dominant_intent = self._determine_dominant_intent(flow)

    def _calculate_flow_ljpw(self, flow: SemanticFlow) -> Coordinates:
        """Calculate aggregate LJPW for entire flow"""
        if not flow.packets:
            return Coordinates(0, 0, 0, 0)

        total_love = sum(p.ljpw_coordinates.love for p in flow.packets)
        total_justice = sum(p.ljpw_coordinates.justice for p in flow.packets)
        total_power = sum(p.ljpw_coordinates.power for p in flow.packets)
        total_wisdom = sum(p.ljpw_coordinates.wisdom for p in flow.packets)

        count = len(flow.packets)

        return Coordinates(
            love=total_love / count,
            justice=total_justice / count,
            power=total_power / count,
            wisdom=total_wisdom / count
        )

    def _classify_flow_pattern(self, flow: SemanticFlow) -> str:
        """Classify what type of communication this flow represents"""
        intents = [p.intent for p in flow.packets]
        ljpw = flow.aggregate_ljpw

        # API Query pattern
        if (SemanticIntent.INFORMATION_REQUEST in intents and
            ljpw.wisdom > 0.7):
            return "API Query Flow"

        # Authentication flow
        if (SemanticIntent.AUTHENTICATION in intents or
            SemanticIntent.AUTHORIZATION in intents):
            return "Authentication Flow"

        # File transfer pattern
        if (ljpw.power > 0.7 and
            len([p for p in flow.packets if p.size > 1000]) > 5):
            return "Large Data Transfer"

        # Connection establishment only
        if all(p.intent == SemanticIntent.CONNECTION_ESTABLISHMENT for p in flow.packets):
            return "Connection Attempt"

        # Secure communication
        if (SemanticIntent.SECURITY_NEGOTIATION in intents and
            ljpw.justice > 0.6):
            return "Secure Communication Session"

        return "General Data Flow"

    def _determine_dominant_intent(self, flow: SemanticFlow) -> SemanticIntent:
        """Determine the primary semantic intent of this flow"""
        from collections import Counter
        intent_counts = Counter(p.intent for p in flow.packets)
        return intent_counts.most_common(1)[0][0]

    def get_flow_summary(self, flow_id: str) -> Optional[Dict]:
        """Get semantic summary of a flow"""
        if flow_id not in self.flows:
            return None

        flow = self.flows[flow_id]

        return {
            'flow_id': flow_id,
            'duration': (flow.end_time - flow.start_time).total_seconds() if flow.end_time else 0,
            'packet_count': len(flow.packets),
            'pattern': flow.flow_pattern,
            'dominant_intent': flow.dominant_intent.value,
            'aggregate_ljpw': {
                'love': flow.aggregate_ljpw.love,
                'justice': flow.aggregate_ljpw.justice,
                'power': flow.aggregate_ljpw.power,
                'wisdom': flow.aggregate_ljpw.wisdom
            },
            'semantic_journey': [
                {
                    'packet': p.packet_num,
                    'intent': p.intent.value,
                    'ljpw': (p.ljpw_coordinates.love, p.ljpw_coordinates.justice,
                            p.ljpw_coordinates.power, p.ljpw_coordinates.wisdom)
                }
                for p in flow.packets[:10]  # First 10 packets
            ]
        }


if __name__ == "__main__":
    # Demo: Simulate packet analysis
    analyzer = DeepPacketSemanticAnalyzer()

    print("Deep Packet Semantic Analysis - Demo")
    print("=" * 60)

    # Simulate different packet types
    test_packets = [
        {
            'data': b'SYN packet simulation',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'SYN': True, 'ACK': False},
                'src_ip': '192.168.1.100',
                'dst_ip': '10.0.0.50',
                'dst_port': 443
            }
        },
        {
            'data': b'GET /api/users HTTP/1.1\r\nHost: api.example.com',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': '10.0.0.50',
                'dst_port': 80
            }
        },
        {
            'data': b'POST /auth/login HTTP/1.1\r\nContent-Type: application/json',
            'metadata': {
                'protocol': 'TCP',
                'tcp_flags': {'ACK': True},
                'src_ip': '192.168.1.100',
                'dst_ip': '10.0.0.50',
                'dst_port': 443
            }
        }
    ]

    for i, test in enumerate(test_packets, 1):
        print(f"\nPacket #{i}:")
        sem = analyzer.analyze_packet(test['data'], test['metadata'])

        print(f"  Intent: {sem.intent.value}")
        print(f"  Description: {sem.semantic_description}")
        print(f"  LJPW: L={sem.ljpw_coordinates.love:.2f}, "
              f"J={sem.ljpw_coordinates.justice:.2f}, "
              f"P={sem.ljpw_coordinates.power:.2f}, "
              f"W={sem.ljpw_coordinates.wisdom:.2f}")
        print(f"  Protocol: {sem.layer7_protocol}")
        print(f"  Confidence: {sem.confidence:.0%}")

        analyzer.track_flow(sem)

    print("\n" + "=" * 60)
    print("Flow Analysis:")
    flow_id = list(analyzer.flows.keys())[0]
    summary = analyzer.get_flow_summary(flow_id)
    print(f"\nFlow: {summary['flow_id']}")
    print(f"Pattern: {summary['pattern']}")
    print(f"Packets: {summary['packet_count']}")
    print(f"Dominant Intent: {summary['dominant_intent']}")
    print(f"Aggregate LJPW: L={summary['aggregate_ljpw']['love']:.2f}, "
          f"J={summary['aggregate_ljpw']['justice']:.2f}, "
          f"P={summary['aggregate_ljpw']['power']:.2f}, "
          f"W={summary['aggregate_ljpw']['wisdom']:.2f}")
