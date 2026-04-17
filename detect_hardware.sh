#!/usr/bin/env bash
echo "CPU:"
lscpu | grep "Model name\|CPU(s):\|Socket(s):"
echo
echo "Memory:"
free -h
echo
echo "Disk:"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
echo
echo "GPU (NVIDIA):"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
  echo "nvidia-smi not found (no NVIDIA or drivers)."
fi
echo
echo "Suggested tier:"
CORES=$(grep -c ^processor /proc/cpuinfo)
MEM=$(free -m | awk '/Mem:/ {print $2}')
if [ "$CORES" -lt 12 ] || [ "$MEM" -lt 64000 ]; then
  echo "Minimum (CPU-only) — try 7B quantized models."
else
  echo "Recommended — consider GPU (24–48 GB) or large CPU (16+ cores, 64–128 GB RAM)."
fi