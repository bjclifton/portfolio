import time
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

# Generate ASCII banner
banner = pyfiglet.figlet_format("BRAD TCP")
print(Fore.CYAN + banner + Style.RESET_ALL)

# Project header
print(Fore.YELLOW + "-----------------------------------------------------------")
print("Project: TCP Protocol Implementation")
print("Description: From-scratch TCP in C++ — connection mgmt, retransmission, congestion control")
print("Skills: C++, Networking, Socket Programming, Unit Testing")
print("-----------------------------------------------------------" + Style.RESET_ALL)
time.sleep(0.5)

# Build output (fake)
print(Fore.GREEN + ">> Building project")
print(Fore.WHITE + "g++ -std=c++17 -O2 -I include -o build/tcp_impl src/*.cpp")
print(Fore.WHITE + "Linking: build/tcp_impl")
print(Fore.GREEN + "Build succeeded (0 warnings)" + Style.RESET_ALL)
time.sleep(0.6)

# Unit tests (fake)
print(Fore.GREEN + "\n>> Running unit tests")
tests = [
    ("Checksum", True),
    ("SequenceNumbering", True),
    ("ConnectionEstablishment", True),
    ("RetransmissionTimer", True),
    ("CongestionControl", True),
    ("EdgeCases", True),
]
for name, ok in tests:
    status = Fore.GREEN + "OK" if ok else Fore.RED + "FAIL"
    print(Fore.WHITE + f"[  TEST  ] {name:<24} {status}")
    time.sleep(0.15)
print(Fore.GREEN + "All tests passed: 6 passed, 0 failed" + Style.RESET_ALL)
time.sleep(0.6)

# Simulated runtime / tcp trace
print(Fore.MAGENTA + "\n>> Live trace: connection 10.0.0.2:50000 -> 10.0.0.1:80" + Style.RESET_ALL)
print(Fore.WHITE + "[Time]    Event                        Seq       Len   Ack     cwnd    ssthresh   RTT(ms)")
time.sleep(0.3)

# Connection establishment
print(Fore.CYAN + "[0.000] SENT    -> SYN              seq=1000     len=0   ---     cwnd=1     ssthresh=64   rtt=---")
time.sleep(0.4)
print(Fore.GREEN + "[0.035] RECV    <- SYN-ACK          seq=5000     len=0   ack=1001  cwnd=1     ssthresh=64   rtt=35.2")
time.sleep(0.3)
print(Fore.CYAN + "[0.036] SENT    -> ACK              seq=1001     len=0   ack=5001  cwnd=1     ssthresh=64   rtt=35.2")
time.sleep(0.5)

# Data transfer: show cwnd growth, retransmit on loss of segment 4
cwnd = 1.0
ssthresh = 64
rtt = 35.2
base_seq = 1001
for i in range(1, 9):
    seq = base_seq + (i - 1) * 1460
    length = 1460
    # simulate slow start doubling cwnd until it surpasses ssthresh then linear growth
    if cwnd < ssthresh:
        cwnd = min(cwnd * 2, 20)  # cap for display
        state = "SLOW-START"
    else:
        cwnd += 1
        state = "CONG-AVOID"
    # artificially create a packet loss at i==4
    if i == 4:
        print(Fore.CYAN + f"[0.{i:03d}] SENT    -> DATA             seq={seq:<8} len={length}  ack=5001  cwnd={cwnd:.1f}   ssthresh={ssthresh}")
        time.sleep(0.35)
        # no ack arrives -> retransmission after timeout / fast retransmit
        print(Fore.RED + f"[0.{i+1:03d}] TIMEOUT  Retransmit        seq={seq:<8} len={length}  cwnd={cwnd:.1f}   ssthresh={ssthresh}")
        # on timeout, ssthresh = cwnd/2, cwnd reset to 1
        ssthresh = max(int(cwnd / 2), 2)
        cwnd = 1.0
        print(Fore.YELLOW + f"[0.{i+2:03d}] RECOVERY Transition -> FAST-RETRANS: ssthresh={ssthresh}, cwnd={cwnd}")
        time.sleep(0.45)
        # retransmitted packet ack
        rtt = round(rtt + 5.1, 1)
        print(Fore.GREEN + f"[0.{i+3:03d}] RECV    <- ACK (dup cleared) seq=5001    len=0   ack={seq+length}  cwnd={cwnd:.1f}   ssthresh={ssthresh}  rtt={rtt}")
        time.sleep(0.35)
    else:
        # normal data send and ack
        rtt = round(rtt + (0.4 if i % 2 == 0 else -0.2), 1)
        print(Fore.CYAN + f"[0.{i:03d}] SENT    -> DATA             seq={seq:<8} len={length}  ack=5001  cwnd={cwnd:.1f}   ssthresh={ssthresh}")
        time.sleep(0.28)
        print(Fore.GREEN + f"[0.{i+0:03d}] RECV    <- ACK              seq=5001     len=0   ack={seq+length}  cwnd={cwnd:.1f}   ssthresh={ssthresh}  rtt={rtt}")
        time.sleep(0.18)

# Final stats summary
print(Fore.MAGENTA + "\n>> Connection closed gracefully (FIN/ACK exchange)")
time.sleep(0.25)
print(Fore.WHITE + "[SUMMARY]  Bytes sent: 11680   Segments sent: 8   Retransmissions: 1")
print(Fore.WHITE + f"[SUMMARY]  Final cwnd: {cwnd:.1f}   Final ssthresh: {ssthresh}   Avg RTT: {round(rtt,1)} ms")
time.sleep(0.25)

# Project notes / README-like mock
print(Fore.YELLOW + "\n-----------------------------------------------------------")
print("Notes:")
print("- Implemented: three-way handshake, sliding window, selective retransmit (SACK-lite),")
print("- Retransmission Timer (RTO) with dynamic RTT estimation (Jacobson/Karels)")
print("- Congestion Control: Slow Start, Congestion Avoidance, Fast Retransmit/Recovery")
print("- Tests: deterministic packet loss simulator used for validation")
print("-----------------------------------------------------------" + Style.RESET_ALL)

print(Fore.CYAN + "\nTCP Implementation demo complete." + Style.RESET_ALL)
