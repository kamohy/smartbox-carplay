#!/bin/sh
# Fixed, read-only operations. No user-supplied command or filesystem path.
PROC=${BH_PROC_ROOT:-/proc}
SYS=${BH_SYS_ROOT:-/sys}
header() {
  printf 'Content-Type: %s; charset=utf-8\r\nCache-Control: no-store\r\n' "$1"
}
number() {
  case "$1" in ''|*[!0-9.]*) printf 'null';; *) printf '%s' "$1";; esac
}
read_number() {
  value=
  if [ -r "$1" ]; then IFS= read -r value < "$1"; fi
  number "$value"
}
audio_dump() {
  printf '%s\n' '=== ALSA hw_params (if exposed by the driver) ==='
  for path in "$PROC"/asound/card*/pcm*/sub*/hw_params; do
    if [ -r "$path" ]; then printf '\n%s\n' "$path"; cat "$path"; fi
  done
  printf '\n%s\n' '=== Last 200 matching audio log lines ==='
  if command -v logcat >/dev/null 2>&1; then
    logcat -v threadtime -d 2>/dev/null | grep -Ei 'AudioPlayerCreate|phone call rate|mic times.*rate|force music rate|SWResample|swr_|underrun|overrun|xrun|in_sample_rate|out_sample_rate' | tail -n 200
  else
    printf '%s\n' 'logcat unavailable'
  fi
}
if [ "${REQUEST_METHOD:-GET}" != GET ]; then
  printf 'Status: 405 Method Not Allowed\r\nAllow: GET\r\n'; header application/json
  printf '\r\n{"error":"GET only"}\n'; exit 0
fi
case "${QUERY_STRING:-}" in
  id=status)
    uptime=; load1=; load5=; load15=; total=; available=
    user=0; nice=0; system=0; idle=0; iowait=0; irq=0; softirq=0; steal=0
    if [ -r "$PROC/uptime" ]; then read -r uptime ignored < "$PROC/uptime"; fi
    if [ -r "$PROC/loadavg" ]; then read -r load1 load5 load15 ignored < "$PROC/loadavg"; fi
    if [ -r "$PROC/meminfo" ]; then
      while read -r key value unit; do
        case "$key" in MemTotal:) total=$value;; MemAvailable:) available=$value;; esac
      done < "$PROC/meminfo"
    fi
    cpu_total=; cpu_idle=
    if [ -r "$PROC/stat" ]; then
      read -r label user nice system idle iowait irq softirq steal ignored < "$PROC/stat"
      cpu_total=$((user + nice + system + idle + iowait + irq + softirq + steal))
      cpu_idle=$((idle + iowait))
    fi
    iface=
    if [ -d "$SYS/class/net/p2p-wlan0-0" ]; then iface=p2p-wlan0-0
    elif [ -d "$SYS/class/net/wlan0" ]; then iface=wlan0; fi
    usb=unknown
    for path in "$SYS"/class/udc/*/state; do
      if [ -r "$path" ]; then IFS= read -r usb < "$path"; break; fi
    done
    case "$usb" in configured|connected|disconnected|attached|powered|default|addressed|suspended|'not attached') :;; *) usb=unknown;; esac
    header application/json; printf '\r\n{"schema":1,"uptime_seconds":'; number "$uptime"
    printf ',"memory_kib":{"total":'; number "$total"; printf ',"available":'; number "$available"; printf '}'
    printf ',"cpu":{"total_jiffies":'; number "$cpu_total"; printf ',"idle_jiffies":'; number "$cpu_idle"; printf '}'
    printf ',"load":['; number "$load1"; printf ','; number "$load5"; printf ','; number "$load15"; printf ']'
    printf ',"usb_state":"%s","network":{"interface":"%s"' "$usb" "$iface"
    for metric in rx_bytes tx_bytes rx_dropped tx_dropped rx_errors tx_errors; do
      printf ',"%s":' "$metric"; read_number "$SYS/class/net/$iface/statistics/$metric"
    done
    printf '}}\n'
    ;;
  id=audio)
    header text/plain; printf '\r\n'; audio_dump
    ;;
  id=logs)
    header text/plain
    printf 'Content-Disposition: attachment; filename="smartbox-diagnostics.txt"\r\n\r\n'
    printf '%s\n' 'Bad-Hippo SmartBox diagnostics 0.6.0 - fresh read, no log buffer clear'
    for name in version uptime loadavg meminfo stat; do
      if [ -r "$PROC/$name" ]; then printf '\n=== /proc/%s ===\n' "$name"; cat "$PROC/$name"; fi
    done
    printf '\n%s\n' '=== dmesg ==='; dmesg 2>&1
    printf '\n%s\n' '=== logcat ==='
    if command -v logcat >/dev/null 2>&1; then logcat -v threadtime -d 2>&1; fi
    printf '\n'; audio_dump
    ;;
  *)
    printf 'Status: 400 Bad Request\r\n'; header application/json
    printf '\r\n{"error":"Supported queries: id=status, id=audio, id=logs"}\n'
    ;;
esac
