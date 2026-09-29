#!/bin/bash
# Supply Chain Digital Twin - System Health Check
# This script checks system health metrics and application availability

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
HOSTNAME=$(hostname)
LOG_FILE="/opt/supply-chain/logs/health_check.log"

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}  Supply Chain Digital Twin Health Check${NC}"
echo -e "${BLUE}  Host: ${HOSTNAME}${NC}"
echo -e "${BLUE}  Time: ${TIMESTAMP}${NC}"
echo -e "${BLUE}==========================================${NC}"
echo

# --- CPU Check ---
echo -e "${YELLOW}[CPU]${NC}"
CPU_USAGE=$(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)
CPU_CORES=$(nproc)
LOAD_AVG=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
echo "  Usage: ${CPU_USAGE}%"
echo "  Cores: ${CPU_CORES}"
echo "  Load Average: ${LOAD_AVG}"
if (( $(echo "$CPU_USAGE > 80" | bc -l 2>/dev/null || echo 0) )); then
    echo -e "  Status: ${RED}WARNING - High CPU usage${NC}"
else
    echo -e "  Status: ${GREEN}OK${NC}"
fi
echo

# --- Memory Check ---
echo -e "${YELLOW}[MEMORY]${NC}"
MEM_TOTAL=$(free -m | awk 'NR==2{print $2}')
MEM_USED=$(free -m | awk 'NR==2{print $3}')
MEM_FREE=$(free -m | awk 'NR==2{print $4}')
MEM_PERCENT=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
echo "  Total: ${MEM_TOTAL} MB"
echo "  Used: ${MEM_USED} MB (${MEM_PERCENT}%)"
echo "  Free: ${MEM_FREE} MB"
if (( $(echo "$MEM_PERCENT > 90" | bc -l 2>/dev/null || echo 0) )); then
    echo -e "  Status: ${RED}WARNING - High memory usage${NC}"
else
    echo -e "  Status: ${GREEN}OK${NC}"
fi
echo

# --- Disk Check ---
echo -e "${YELLOW}[DISK]${NC}"
df -h / | tail -1 | awk '{print "  Root: " $3 " used of " $2 " (" $5 " used)"}'
if mountpoint -q /opt/supply-chain 2>/dev/null; then
    df -h /opt/supply-chain | tail -1 | awk '{print "  Data: " $3 " used of " $2 " (" $5 " used)"}'
fi
ROOT_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$ROOT_USAGE" -gt 85 ]; then
    echo -e "  Status: ${RED}WARNING - Disk usage above 85%${NC}"
else
    echo -e "  Status: ${GREEN}OK${NC}"
fi
echo

# --- Network Check ---
echo -e "${YELLOW}[NETWORK]${NC}"
PRIVATE_IP=$(hostname -I | awk '{print $1}')
echo "  Private IP: ${PRIVATE_IP}"
PUBLIC_IP=$(curl -s --connect-timeout 5 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'N/A')
echo "  Public IP: ${PUBLIC_IP}"
if ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
    echo -e "  Internet: ${GREEN}Connected${NC}"
else
    echo -e "  Internet: ${RED}Disconnected${NC}"
fi
echo

# --- Docker Check ---
echo -e "${YELLOW}[DOCKER]${NC}"
if command -v docker &>/dev/null; then
    if systemctl is-active --quiet docker; then
        echo -e "  Service: ${GREEN}Running${NC}"
        CONTAINERS_RUNNING=$(docker ps -q 2>/dev/null | wc -l)
        CONTAINERS_TOTAL=$(docker ps -aq 2>/dev/null | wc -l)
        IMAGES=$(docker images -q 2>/dev/null | wc -l)
        echo "  Containers Running: ${CONTAINERS_RUNNING}"
        echo "  Containers Total: ${CONTAINERS_TOTAL}"
        echo "  Images: ${IMAGES}"
    else
        echo -e "  Service: ${RED}Stopped${NC}"
    fi
else
    echo -e "  Status: ${YELLOW}Not Installed${NC}"
fi
echo

# --- Services Check ---
echo -e "${YELLOW}[SERVICES]${NC}"
for svc in docker ssh; do
    if systemctl is-active --quiet $svc 2>/dev/null; then
        echo -e "  ${svc}: ${GREEN}Active${NC}"
    else
        echo -e "  ${svc}: ${RED}Inactive${NC}"
    fi
done
echo

# --- Application Check ---
echo -e "${YELLOW}[APPLICATION]${NC}"
if curl -s --connect-timeout 3 http://localhost:5000/health &>/dev/null; then
    echo -e "  Flask App (5000): ${GREEN}Responding${NC}"
else
    echo -e "  Flask App (5000): ${YELLOW}Not Running${NC}"
fi
if curl -s --connect-timeout 3 http://localhost:8080/actuator/health &>/dev/null; then
    echo -e "  Spring Boot (8080): ${GREEN}Responding${NC}"
else
    echo -e "  Spring Boot (8080): ${YELLOW}Not Running${NC}"
fi
echo

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}  Health Check Complete${NC}"
echo -e "${BLUE}==========================================${NC}"

# Log results
mkdir -p /opt/supply-chain/logs
echo "${TIMESTAMP} | CPU: ${CPU_USAGE}% | MEM: ${MEM_PERCENT}% | DISK: ${ROOT_USAGE}% | Docker: $(systemctl is-active docker 2>/dev/null || echo 'N/A')" >> "${LOG_FILE}"
