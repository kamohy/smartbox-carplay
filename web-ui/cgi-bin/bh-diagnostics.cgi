#!/bin/sh
# Fixed diagnostic operations, plus one bounded recorder-save request.
PROC=${BH_PROC_ROOT:-/proc}
SYS=${BH_SYS_ROOT:-/sys}
RECORDER=${BH_RECORDER:-/tmp/bh-recorder.sh}
if [ -z "${BH_RECORDER:-}" ] && [ ! -r "$RECORDER" ]; then RECORDER=/mnt/customer/app/bh-log-recorder.sh; fi
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
if [ "${REQUEST_METHOD:-GET}" = POST ] && { [ "${QUERY_STRING:-}" = id=save ] || [ "${QUERY_STRING:-}" = id=clear ]; }; then
  case "${HTTP_ORIGIN:-}" in ''|'http://192.168.1.101') :;; *)
    printf 'Status: 403 Forbidden\r\n'; header application/json; printf '\r\n{"error":"Local origin required"}\n'; exit 0;;
  esac
  action=request; [ "$QUERY_STRING" != id=clear ] || action=clear
  if [ -r "$RECORDER" ] && sh "$RECORDER" "$action"; then
    printf 'Status: 202 Accepted\r\n'; header application/json; printf '\r\n{"queued":true}\n'
  else
    printf 'Status: 503 Service Unavailable\r\n'; header application/json; printf '\r\n{"error":"Recorder/storage unavailable"}\n'
  fi
  exit 0
fi
if [ "${REQUEST_METHOD:-GET}" != GET ]; then
  printf 'Status: 405 Method Not Allowed\r\nAllow: GET\r\n'; header application/json
  printf '\r\n{"error":"GET only"}\n'; exit 0
fi
case "${QUERY_STRING:-}" in
  id=space)
    header application/json; printf '\r\n{"schema":1,"memory_available_kib":'
    available=$(awk '/^MemAvailable:/ {print $2; exit}' "$PROC/meminfo" 2>/dev/null); number "$available"
    printf ',"filesystems":['; separator=
    for path in /tmp /mnt/UDISK /mnt/customer /; do
      line=$(df -Pk "$path" 2>/dev/null | tail -n 1)
      set -- $line
      printf '%s{"path":"%s","total_kib":' "$separator" "$path"; number "$2"
      printf ',"used_kib":'; number "$3"; printf ',"available_kib":'; number "$4"
      options=$(awk -v target="$6" '$2 == target {print $4; exit}' "$PROC/mounts" 2>/dev/null)
      writable=null; case ",$options," in *,rw,*) writable=true;; *,ro,*) writable=false;; esac
      printf ',"writable":%s}' "$writable"
      separator=,
    done
    printf ']}\n';;
  id=errors)
    header text/plain; printf '\r\nBad-Hippo error report 0.9.0\n'
    printf '\n=== Update status ===\n'
    path="$SYS/class/misc/ly_misc_dev/ly/update"
    if [ -r "$path" ]; then cat "$path"; else printf 'unavailable\n'; fi
    printf '\n=== Filesystem capacity (KiB) ===\n'; df -Pk /tmp /mnt/UDISK /mnt/customer / 2>&1
    printf '\n=== Current mounts ===\n'; cat "$PROC/mounts" 2>/dev/null
    printf '\n=== Updater process evidence ===\n'; ps 2>/dev/null | grep -E '(^|[ /])(update|swupdate)( |$)' | head -n 12
    printf '\n=== Kernel errors (last 80 matching lines) ===\n'
    dmesg 2>&1 | grep -Ei 'error|fail|no space|out of memory|oom|killed process|read-only' | tail -n 80 | head -c 12288
    printf '\n=== Application/update errors (last 120 matching lines) ===\n'
    if command -v logcat >/dev/null 2>&1; then
      logcat -v threadtime -d 2>&1 | grep -Ei 'update|upload|error|fail|no space|out of memory|oom|killed process' | tail -n 120 | head -c 16384
    fi
    for path in /tmp/update.log /tmp/swupdate.log /var/log/messages; do
      if [ -f "$path" ] && [ ! -L "$path" ]; then printf '\n=== %s (tail) ===\n' "$path"; tail -n 80 "$path" | head -c 8192; fi
    done
    printf '\n';;
  id=hardware)
    header text/plain; printf '\r\nBad-Hippo hardware probe 0.9.0\n'
    for name in cpuinfo meminfo mtd partitions mounts; do
      if [ -r "$PROC/$name" ]; then printf '\n=== /proc/%s ===\n' "$name"; cat "$PROC/$name"; fi
    done
    for path in "$SYS"/devices/system/cpu/cpu0/cpufreq/*freq* "$SYS"/class/net/*/device/modalias "$SYS"/class/net/*/device/vendor "$SYS"/class/net/*/device/device "$SYS"/bus/usb/devices/*/idVendor "$SYS"/bus/usb/devices/*/idProduct "$SYS"/bus/usb/devices/*/product; do
      if [ -f "$path" ] && [ -r "$path" ]; then printf '\n%s: ' "$path"; cat "$path"; fi
    done
    for command in lsusb hciconfig; do
      if command -v "$command" >/dev/null 2>&1; then
        printf '\n=== %s ===\n' "$command"
        if [ "$command" = hciconfig ]; then hciconfig -a 2>&1; else lsusb 2>&1; fi
      fi
    done
    ;;
  id=storage)
    header application/json; printf '\r\n'
    if [ -r "$RECORDER" ]; then sh "$RECORDER" status; else printf '{"supported":false,"running":false,"state":"not_running","files":[]}\n'; fi
    ;;
  id=stored0a|id=stored0b|id=stored1a|id=stored1b|id=stored2a|id=stored2b)
    id=${QUERY_STRING#id=stored}
    if [ -r "$RECORDER" ] && sh "$RECORDER" has "$id"; then
      header application/gzip; printf 'Content-Disposition: attachment; filename="smartbox-log-%s.gz"\r\n\r\n' "$id"
      sh "$RECORDER" cat "$id"
    else
      printf 'Status: 404 Not Found\r\n'; header application/json; printf '\r\n{"error":"Stored log unavailable"}\n'
    fi
    ;;
  'id=audio&source=0a'|'id=audio&source=0b'|'id=audio&source=1a'|'id=audio&source=1b'|'id=audio&source=2a'|'id=audio&source=2b')
    id=${QUERY_STRING#id=audio&source=}
    if [ -r "$RECORDER" ] && sh "$RECORDER" has "$id"; then
      header text/plain; printf '\r\n=== Stored log %s: last 200 matching audio lines ===\n' "$id"
      sh "$RECORDER" unpack "$id" | grep -Ei 'AudioPlayerCreate|phone call rate|mic times.*rate|force music rate|SWResample|swr_|underrun|overrun|xrun|in_sample_rate|out_sample_rate' | tail -n 200
    else
      printf 'Status: 404 Not Found\r\n'; header application/json; printf '\r\n{"error":"Stored audio log unavailable"}\n'
    fi
    ;;
  id=status)
    uptime=; idle_seconds=; load1=; load5=; load15=; total=; available=
    user=0; nice=0; system=0; idle=0; iowait=0; irq=0; softirq=0; steal=0
    if [ -r "$PROC/uptime" ]; then read -r uptime idle_seconds < "$PROC/uptime"; fi
    if [ -r "$PROC/loadavg" ]; then read -r load1 load5 load15 ignored < "$PROC/loadavg"; fi
    if [ -r "$PROC/meminfo" ]; then
      while read -r key value unit; do
        case "$key" in MemTotal:) total=$value;; MemAvailable:) available=$value;; esac
      done < "$PROC/meminfo"
    fi
    cpu_total=; cpu_idle=; cpu_count=0
    if [ -r "$PROC/stat" ]; then
      while read -r label user nice system idle iowait irq softirq steal ignored; do
        case "$label" in
          cpu) cpu_total=$((user + nice + system + idle + iowait + irq + softirq + steal)); cpu_idle=$((idle + iowait));;
          cpu[0-9]*) cpu_count=$((cpu_count + 1));;
          *) break;;
        esac
      done < "$PROC/stat"
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
    printf ',"idle_seconds":'; number "$idle_seconds"
    printf ',"memory_kib":{"total":'; number "$total"; printf ',"available":'; number "$available"; printf '}'
    printf ',"cpu":{"total_jiffies":'; number "$cpu_total"; printf ',"idle_jiffies":'; number "$cpu_idle"; printf ',"count":'; number "$cpu_count"; printf '}'
    printf ',"load":['; number "$load1"; printf ','; number "$load5"; printf ','; number "$load15"; printf ']'
    printf ',"usb_state":"%s","network":{"interface":"%s"' "$usb" "$iface"
    for metric in rx_bytes tx_bytes rx_dropped tx_dropped rx_errors tx_errors; do
      printf ',"%s":' "$metric"; read_number "$SYS/class/net/$iface/statistics/$metric"
    done
    printf '},"networks":['
    separator=
    for path in "$SYS"/class/net/*; do
      [ -d "$path" ] || continue
      name=${path##*/}; case "$name" in lo|*[!a-zA-Z0-9_.:-]*) continue;; esac
      printf '%s{"interface":"%s"' "$separator" "$name"
      for metric in rx_bytes tx_bytes rx_dropped tx_dropped rx_errors tx_errors; do
        printf ',"%s":' "$metric"; read_number "$path/statistics/$metric"
      done
      printf '}'; separator=,
    done
    printf ']}\n'
    ;;
  id=audio)
    header text/plain; printf '\r\n'; audio_dump
    ;;
  id=logs)
    header text/plain
    printf 'Content-Disposition: attachment; filename="smartbox-diagnostics.txt"\r\n\r\n'
    printf '%s\n' 'Bad-Hippo SmartBox diagnostics 0.9.0 - fresh read, no log buffer clear'
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
    printf '\r\n{"error":"Unsupported diagnostics query"}\n'
    ;;
esac
