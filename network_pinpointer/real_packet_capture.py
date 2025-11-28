#!/usr/bin/env python3
"""
Real Packet Capture: Capture and Analyze Actual Network Traffic

Uses scapy to capture real packets and extract protocol metadata
for semantic LJPW analysis.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import subprocess
import re

try:
    from scapy.all import (
        sniff, IP, ICMP, TCP, UDP, DNS,
        DNSQR, DNSRR, Raw, Ether
    )
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("WARNING: scapy not available. Install with: pip install scapy")


@dataclass
class ICMPMetadata:
    """Metadata extracted from ICMP packet"""
    type: int
    code: int
    ttl: int
    packet_size: int
    sequence: Optional[int]
    timestamp: datetime
    source_ip: str
    dest_ip: str

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "code": self.code,
            "ttl": self.ttl,
            "packet_size": self.packet_size,
            "sequence": self.sequence,
            "timestamp": self.timestamp.isoformat(),
            "source_ip": self.source_ip,
            "dest_ip": self.dest_ip,
        }


@dataclass
class TCPMetadata:
    """Metadata extracted from TCP packet"""
    source_port: int
    dest_port: int
    seq_num: int
    ack_num: int
    flags: str  # SYN, ACK, RST, FIN, etc.
    window_size: int
    ttl: int
    options: List[tuple]
    timestamp: datetime
    source_ip: str
    dest_ip: str

    def to_dict(self) -> Dict:
        return {
            "source_port": self.source_port,
            "dest_port": self.dest_port,
            "seq_num": self.seq_num,
            "ack_num": self.ack_num,
            "flags": self.flags,
            "window_size": self.window_size,
            "ttl": self.ttl,
            "options": str(self.options),
            "timestamp": self.timestamp.isoformat(),
            "source_ip": self.source_ip,
            "dest_ip": self.dest_ip,
        }


@dataclass
class DNSMetadata:
    """Metadata extracted from DNS packet"""
    query_name: Optional[str]
    query_type: Optional[str]
    answers: List[str]
    answer_ttls: List[int]
    response_time: Optional[float]
    ttl: int
    timestamp: datetime
    source_ip: str
    dest_ip: str

    def to_dict(self) -> Dict:
        return {
            "query_name": self.query_name,
            "query_type": self.query_type,
            "answers": self.answers,
            "answer_ttls": self.answer_ttls,
            "response_time": self.response_time,
            "ttl": self.ttl,
            "timestamp": self.timestamp.isoformat(),
            "source_ip": self.source_ip,
            "dest_ip": self.dest_ip,
        }


class RealPacketCapture:
    """Capture and parse real network packets"""

    def __init__(self):
        if not SCAPY_AVAILABLE:
            raise ImportError("scapy is required for packet capture")

        self.captured_packets = []

    def capture_icmp(
        self,
        count: int = 10,
        timeout: int = 10,
        filter_str: str = "icmp"
    ) -> List[ICMPMetadata]:
        """
        Capture ICMP packets from network

        Args:
            count: Number of packets to capture
            timeout: Timeout in seconds
            filter_str: BPF filter string

        Returns:
            List of parsed ICMP metadata
        """
        print(f"Capturing {count} ICMP packets (timeout: {timeout}s)...")

        packets = sniff(
            filter=filter_str,
            count=count,
            timeout=timeout,
            store=True
        )

        metadata_list = []

        for pkt in packets:
            if IP in pkt and ICMP in pkt:
                metadata = self._parse_icmp_packet(pkt)
                if metadata:
                    metadata_list.append(metadata)

        print(f"Captured {len(metadata_list)} ICMP packets")
        return metadata_list

    def capture_tcp(
        self,
        count: int = 10,
        timeout: int = 10,
        filter_str: str = "tcp"
    ) -> List[TCPMetadata]:
        """
        Capture TCP packets from network

        Args:
            count: Number of packets to capture
            timeout: Timeout in seconds
            filter_str: BPF filter string

        Returns:
            List of parsed TCP metadata
        """
        print(f"Capturing {count} TCP packets (timeout: {timeout}s)...")

        packets = sniff(
            filter=filter_str,
            count=count,
            timeout=timeout,
            store=True
        )

        metadata_list = []

        for pkt in packets:
            if IP in pkt and TCP in pkt:
                metadata = self._parse_tcp_packet(pkt)
                if metadata:
                    metadata_list.append(metadata)

        print(f"Captured {len(metadata_list)} TCP packets")
        return metadata_list

    def capture_dns(
        self,
        count: int = 10,
        timeout: int = 10,
        filter_str: str = "udp port 53"
    ) -> List[DNSMetadata]:
        """
        Capture DNS packets from network

        Args:
            count: Number of packets to capture
            timeout: Timeout in seconds
            filter_str: BPF filter string

        Returns:
            List of parsed DNS metadata
        """
        print(f"Capturing {count} DNS packets (timeout: {timeout}s)...")

        packets = sniff(
            filter=filter_str,
            count=count,
            timeout=timeout,
            store=True
        )

        metadata_list = []

        for pkt in packets:
            if IP in pkt and UDP in pkt and DNS in pkt:
                metadata = self._parse_dns_packet(pkt)
                if metadata:
                    metadata_list.append(metadata)

        print(f"Captured {len(metadata_list)} DNS packets")
        return metadata_list

    def _parse_icmp_packet(self, pkt) -> Optional[ICMPMetadata]:
        """Parse ICMP packet into metadata structure"""
        try:
            ip_layer = pkt[IP]
            icmp_layer = pkt[ICMP]

            # Extract sequence number if available
            sequence = None
            if hasattr(icmp_layer, 'seq'):
                sequence = icmp_layer.seq

            return ICMPMetadata(
                type=icmp_layer.type,
                code=icmp_layer.code,
                ttl=ip_layer.ttl,
                packet_size=len(pkt),
                sequence=sequence,
                timestamp=datetime.now(),
                source_ip=ip_layer.src,
                dest_ip=ip_layer.dst,
            )
        except Exception as e:
            print(f"Error parsing ICMP packet: {e}")
            return None

    def _parse_tcp_packet(self, pkt) -> Optional[TCPMetadata]:
        """Parse TCP packet into metadata structure"""
        try:
            ip_layer = pkt[IP]
            tcp_layer = pkt[TCP]

            # Extract TCP flags
            flags = []
            if tcp_layer.flags.S: flags.append("SYN")
            if tcp_layer.flags.A: flags.append("ACK")
            if tcp_layer.flags.F: flags.append("FIN")
            if tcp_layer.flags.R: flags.append("RST")
            if tcp_layer.flags.P: flags.append("PSH")
            if tcp_layer.flags.U: flags.append("URG")

            flags_str = "|".join(flags) if flags else "NONE"

            # Extract TCP options
            options = []
            if hasattr(tcp_layer, 'options'):
                options = tcp_layer.options

            return TCPMetadata(
                source_port=tcp_layer.sport,
                dest_port=tcp_layer.dport,
                seq_num=tcp_layer.seq,
                ack_num=tcp_layer.ack,
                flags=flags_str,
                window_size=tcp_layer.window,
                ttl=ip_layer.ttl,
                options=options,
                timestamp=datetime.now(),
                source_ip=ip_layer.src,
                dest_ip=ip_layer.dst,
            )
        except Exception as e:
            print(f"Error parsing TCP packet: {e}")
            return None

    def _parse_dns_packet(self, pkt) -> Optional[DNSMetadata]:
        """Parse DNS packet into metadata structure"""
        try:
            ip_layer = pkt[IP]
            dns_layer = pkt[DNS]

            # Extract query information
            query_name = None
            query_type = None
            if dns_layer.qd:
                query_name = dns_layer.qd.qname.decode('utf-8') if dns_layer.qd.qname else None
                query_type = dns_layer.qd.qtype

            # Extract answers
            answers = []
            answer_ttls = []
            if dns_layer.an:
                for i in range(dns_layer.ancount):
                    try:
                        rr = dns_layer.an[i]
                        if hasattr(rr, 'rdata'):
                            answers.append(str(rr.rdata))
                        if hasattr(rr, 'ttl'):
                            answer_ttls.append(rr.ttl)
                    except (AttributeError, IndexError, TypeError):
                        pass

            return DNSMetadata(
                query_name=query_name,
                query_type=str(query_type) if query_type else None,
                answers=answers,
                answer_ttls=answer_ttls,
                response_time=None,  # Would need query/response correlation
                ttl=ip_layer.ttl,
                timestamp=datetime.now(),
                source_ip=ip_layer.src,
                dest_ip=ip_layer.dst,
            )
        except Exception as e:
            print(f"Error parsing DNS packet: {e}")
            return None


class FallbackPacketCapture:
    """
    Fallback packet capture using system ping/traceroute commands

    Used when scapy is not available or root access not possible
    """

    def capture_icmp_via_ping(
        self,
        target: str,
        count: int = 10
    ) -> List[ICMPMetadata]:
        """
        Capture ICMP data by running ping command and parsing output

        This is a fallback when direct packet capture isn't available
        """
        print(f"Running ping to {target} ({count} packets)...")

        try:
            # Run ping command
            result = subprocess.run(
                ['ping', '-c', str(count), target],
                capture_output=True,
                text=True,
                timeout=30
            )

            return self._parse_ping_output(result.stdout, target)

        except subprocess.TimeoutExpired:
            print("Ping command timed out")
            return []
        except FileNotFoundError:
            print("Ping command not found")
            return []
        except Exception as e:
            print(f"Error running ping: {e}")
            return []

    def _parse_ping_output(self, output: str, target: str) -> List[ICMPMetadata]:
        """Parse ping command output to extract metadata"""
        metadata_list = []

        # Parse each ping line
        # Format: 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=10.2 ms
        pattern = r'(\d+) bytes from ([^:]+): icmp_seq=(\d+) ttl=(\d+) time=([\d.]+)'

        for line in output.split('\n'):
            match = re.search(pattern, line)
            if match:
                size = int(match.group(1))
                source = match.group(2)
                seq = int(match.group(3))
                ttl = int(match.group(4))
                # time in ms, not used here

                metadata = ICMPMetadata(
                    type=0,  # Echo reply
                    code=0,
                    ttl=ttl,
                    packet_size=size,
                    sequence=seq,
                    timestamp=datetime.now(),
                    source_ip=source,
                    dest_ip=target,
                )
                metadata_list.append(metadata)

        return metadata_list


def get_packet_capture() -> Any:
    """
    Factory function to get appropriate packet capture implementation

    Returns scapy-based capture if available, otherwise fallback
    """
    if SCAPY_AVAILABLE:
        try:
            return RealPacketCapture()
        except Exception as e:
            print(f"Could not initialize scapy capture: {e}")
            print("Falling back to command-based capture")
            return FallbackPacketCapture()
    else:
        print("Scapy not available, using fallback capture")
        return FallbackPacketCapture()


if __name__ == "__main__":
    # Demo: Show what we can capture
    print("Network Packet Capture Demo")
    print("=" * 70)

    capture = get_packet_capture()

    if isinstance(capture, RealPacketCapture):
        print("\n✓ Scapy-based capture available (full protocol access)")
        print("\nNote: Packet capture requires root/admin privileges")
        print("Run with: sudo python3 real_packet_capture.py")
    else:
        print("\n✓ Command-based capture available (limited metadata)")
        print("\nTesting with ping to 8.8.8.8...")

        metadata = capture.capture_icmp_via_ping("8.8.8.8", count=5)

        if metadata:
            print(f"\nCaptured {len(metadata)} ICMP packets:")
            for i, m in enumerate(metadata[:3], 1):
                print(f"\nPacket {i}:")
                print(f"  Source: {m.source_ip}")
                print(f"  TTL: {m.ttl}")
                print(f"  Sequence: {m.sequence}")
                print(f"  Size: {m.packet_size} bytes")
