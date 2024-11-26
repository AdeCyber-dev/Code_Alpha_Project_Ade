from scapy.all import sniff, IP, TCP, UDP, wrpcap
from rich.console import Console
from rich.table import Table
import os 

# Rich library for real-time table updates
console = Console()

# List to store captured packets for later export
captured_packets = []

# Function to process packets and display them in real time
def packet_callback(packet):
    try:
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            protocol = "Other"
            
            # Identify protocol
            if TCP in packet:
                protocol = "TCP"
                sport = packet.sport
                dport = packet.dport
                packet_info = f"{ip_src}:{sport} -> {ip_dst}:{dport} ({protocol})"
            elif UDP in packet:
                protocol = "UDP"
                sport = packet.sport
                dport = packet.dport
                packet_info = f"{ip_src}:{sport} -> {ip_dst}:{dport} ({protocol})"
            else:
                packet_info = f"{ip_src} -> {ip_dst} (Other)"
            
            # Add packet to storage for pcap export
            captured_packets.append(packet)

            # Display packet info in a table
            console.print(packet_info)

    except Exception as e:
        console.print(f"[red]Error processing packet: {e}[/red]")

def start_sniffer(filter_type=None, output_file="captured_packets.pcap"):
    # Validate the filter expression if provided
    if filter_type:
        try:
            sniff(filter=filter_type, count=1, store=0)  # Dummy sniff to test filter
        except Exception as e:
            print(f"Error: Invalid filter expression '{filter_type}'.")
            print("Details:", e)
            return

    # Validate output file path
    if os.path.exists(output_file):
        print(f"Warning: Output file '{output_file}' already exists. It will be overwritten.")

    print("Starting packet capture... Press Ctrl+C to stop.")
    print("┌───────────┬────────────────┬──────────┬───────────┐")
    print("│ Source IP │ Destination IP │ Protocol │ Info      │")
    print("├───────────┼────────────────┼──────────┼───────────┤")

    def packet_callback(packet):
        """Callback to process and display each packet."""
        try:
            src_ip = packet[0][1].src if hasattr(packet[0][1], "src") else "N/A"
            dst_ip = packet[0][1].dst if hasattr(packet[0][1], "dst") else "N/A"
            proto = packet[0].proto if hasattr(packet[0], "proto") else "N/A"
            info = repr(packet)[:20]  # Display a snippet of the packet's raw data

            # Print packet details in table format
            print(f"│ {src_ip:<10} │ {dst_ip:<14} │ {proto:<8} │ {info:<9} │")

        except Exception as e:
            print(f"Error processing packet: {e}")

    try:
        sniff(prn=packet_callback, store=False, filter=filter_type)
    except KeyboardInterrupt:
        print("\nCapture stopped.")
    except Exception as e:
        print(f"\nError during packet capture: {e}")
    finally:
        print("└───────────┴────────────────┴──────────┴───────────┘")
        print(f"Packets saved to '{output_file}' (if specified).")

if __name__ == "__main__":
    # User inputs filter type and file name
    selected_filter = input("Enter packet filter (e.g., 'tcp', 'udp', 'icmp', or leave blank for all): ").strip()
    output_filename = input("Enter output .pcap file name (default: captured_packets.pcap): ").strip()
    if not output_filename:
        output_filename = "captured_packets.pcap"
    
    start_sniffer(filter_type=selected_filter, output_file=output_filename)
