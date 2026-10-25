#!/bin/sh
# Bounded, compressed logs on the existing persistent data partition.
# Only bh-logs/ is modified. No mount, format, raw flash or audio configuration.
BASE=${BH_LOG_MOUNT:-/mnt/UDISK}
PROC=${BH_PROC_ROOT:-/proc}
RAM=${BH_LOG_RAM:-/tmp/bh-log-recorder}
DIR=$BASE/bh-logs
STATUS_CGI=${BH_STATUS_CGI:-/mnt/customer/ota/www/cgi-bin/bh-diagnostics.cgi}
RESERVE_KIB=64
MAX_BYTES=24576
PERIOD=60
num() { case "$1" in ''|*[!0-9.]*) printf null;; *) printf '%s' "$1";; esac; }
integer() { case "$1" in ''|*[!0-9]*) return 1;; *) return 0;; esac; }
read_value() { v=; if [ -r "$1" ]; then read -r v ignored < "$1"; fi; if integer "$v"; then printf '%s' "$v"; else printf 0; fi; }
now() { value=0; if [ -r "$PROC/uptime" ]; then read -r value ignored < "$PROC/uptime"; fi; printf '%s' "${value%%.*}"; }
probe() {
  REASON=mount_unavailable; TOTAL=0; FREE=0
  [ ! -L "$BASE" ] || return 1
  found=0
  if [ -r "$PROC/mounts" ]; then
    while read -r device target fs options rest; do
      if [ "$target" = "$BASE" ]; then
        case "$fs" in tmpfs|ramfs|rootfs|squashfs|overlay) return 1;; esac
        case ",$options," in *,rw,*) found=1;; esac
      fi
    done < "$PROC/mounts"
  fi
  [ "$found" = 1 ] || return 1
  [ ! -L "$DIR" ] || return 1
  REASON=storage_probe_failed
  line=$(df -Pk "$BASE" 2>/dev/null | tail -n 1)
  set -- $line
  integer "$2" && integer "$4" || return 1
  TOTAL=$2; FREE=$4; REASON=ready
  return 0
}
running() {
  pid=$(read_value "$RAM/pid")
  [ "$pid" -gt 1 ] && kill -0 "$pid" 2>/dev/null
}
state() { mkdir -p "$RAM"; printf '%s\n' "$1" > "$RAM/state"; }
valid_id() { case "$1" in 0a|0b|1a|1b|2a|2b) return 0;; *) return 1;; esac; }
status() {
  supported=false; probe && supported=true
  active=false; running && active=true
  label=$REASON
  if [ -r "$RAM/state" ]; then read -r label < "$RAM/state"; fi
  case "$label" in cleared|ready|saved|collecting|no_space|snapshot_too_large|storage_probe_failed|mount_unavailable|not_running|write_failed|initializing) :;; *) label=unknown;; esac
  printf '{"schema":1,"supported":%s,"running":%s,"state":"%s","total_kib":' "$supported" "$active" "$label"; num "$TOTAL"
  printf ',"available_kib":'; num "$FREE"
  printf ',"reserve_kib":%s,"max_snapshot_bytes":%s,"period_seconds":%s,"retained_boots_max":3,"files":[' "$RESERVE_KIB" "$MAX_BYTES" "$PERIOD"
  separator=
  for id in 0a 0b 1a 1b 2a 2b; do
    file=$DIR/log-$id.gz
    if [ -f "$file" ] && [ ! -L "$file" ]; then
      bytes=$(wc -c < "$file"); set -- $bytes; bytes=$1
      boot=; saved=
      if [ -r "$DIR/meta-$id" ]; then read -r boot saved < "$DIR/meta-$id"; fi
      printf '%s{"id":"%s","bytes":' "$separator" "$id"; num "$bytes"
      printf ',"boot":'; num "$boot"; printf ',"saved_uptime":'; num "$saved"; printf '}'
      separator=,
    fi
  done
  printf ']}\n'
}
metrics() {
  if [ -r "$STATUS_CGI" ]; then
    REQUEST_METHOD=GET QUERY_STRING=id=status sh "$STATUS_CGI" 2>/dev/null | tail -n 1 >> "$RAM/metrics.jsonl"
    tail -n 120 "$RAM/metrics.jsonl" > "$RAM/metrics.new" && mv -f "$RAM/metrics.new" "$RAM/metrics.jsonl"
  fi
}
collect() {
  lines=$1
  printf 'Bad-Hippo persistent system log 0.8.0\nBoot counter: %s\nSaved uptime: %s\nLogcat tail lines: %s\n' "$BOOT" "$(now)" "$lines"
  printf '\n=== proc snapshots ===\n'
  for name in version uptime loadavg meminfo; do
    if [ -r "$PROC/$name" ]; then printf '\n=== /proc/%s ===\n' "$name"; cat "$PROC/$name"; fi
  done
  printf '\n=== recent metrics (JSONL, in RAM) ===\n'
  if [ -r "$RAM/metrics.jsonl" ]; then cat "$RAM/metrics.jsonl"; fi
  printf '\n=== dmesg tail, 400 lines ===\n'; dmesg 2>&1 | tail -n 400
  if command -v logcat >/dev/null 2>&1; then
    # Keep the initial HU choice even after the general log tail rolls over.
    logcat -v threadtime -d 2>/dev/null | grep -Ei 'GetHUPluginVer|getAudioFormat|media .*audio rate|huInfo name=|mSysInfo' > "$RAM/hu-latest"
    if [ -r "$RAM/hu-history" ]; then cat "$RAM/hu-history" >> "$RAM/hu-latest"; fi
    sort -u "$RAM/hu-latest" | tail -n 80 > "$RAM/hu-history"
    printf '\n=== retained head-unit format selection ===\n'; cat "$RAM/hu-history"
    printf '\n=== logcat tail ===\n'; logcat -v threadtime -d 2>&1 | tail -n "$lines"
    printf '\n=== audio evidence, last 200 matching lines ===\n'
    logcat -v threadtime -d 2>/dev/null | grep -Ei 'AudioPlayerCreate|phone call rate|mic times.*rate|force music rate|SWResample|swr_|underrun|overrun|xrun|in_sample_rate|out_sample_rate' | tail -n 200
  fi
}
clear_logs() {
  probe || { state "$REASON"; return 1; }
  # Fixed own filenames only. Keep the counter and all unrelated data.
  for id in 0a 0b 1a 1b 2a 2b; do
    rm -f "$DIR/log-$id.gz" "$DIR/meta-$id" "$DIR/log-$id.gz.pending" "$DIR/meta-$id.pending" || { state write_failed; return 1; }
  done
  rm -f "$RAM/metrics.jsonl" "$RAM/metrics.new" "$RAM/snapshot.gz" "$RAM/hu-history" "$RAM/hu-latest" "$RAM/request"
  sync; state cleared
}
capture() {
  probe || { state "$REASON"; return 1; }
  state collecting
  fits=0
  for lines in 1200 600 300 100; do
    collect "$lines" | gzip -1 > "$RAM/snapshot.gz" || { state write_failed; return 1; }
    bytes=$(wc -c < "$RAM/snapshot.gz"); set -- $bytes; bytes=$1
    if [ "$bytes" -le "$MAX_BYTES" ]; then fits=1; break; fi
  done
  [ "$fits" = 1 ] || { state snapshot_too_large; return 1; }
  gzip -t "$RAM/snapshot.gz" 2>/dev/null || { state write_failed; return 1; }
  needed=$((RESERVE_KIB + (bytes + 1023) / 1024))
  [ "$FREE" -ge "$needed" ] || { state no_space; return 1; }
  side=a
  [ "$(read_value "$RAM/side")" = 0 ] || side=b
  id=$SLOT$side
  target=$DIR/log-$id.gz
  # Copy and verify a new file before replacing either complete snapshot.
  cp "$RAM/snapshot.gz" "$target.pending" || { state write_failed; return 1; }
  sync
  gzip -t "$target.pending" 2>/dev/null || { rm -f "$target.pending"; state write_failed; return 1; }
  mv -f "$target.pending" "$target" || { state write_failed; return 1; }
  printf '%s %s\n' "$BOOT" "$(now)" > "$DIR/meta-$id.pending"
  mv -f "$DIR/meta-$id.pending" "$DIR/meta-$id"
  sync
  if [ "$side" = a ]; then printf '1\n' > "$RAM/side"; else printf '0\n' > "$RAM/side"; fi
  state saved
  return 0
}
initialize() {
  probe || { state "$REASON"; return 1; }
  [ "$FREE" -ge "$((RESERVE_KIB + MAX_BYTES / 1024))" ] || { state no_space; return 1; }
  mkdir -p "$RAM" "$DIR" || return 1
  if [ -r "$RAM/boot" ]; then
    BOOT=$(read_value "$RAM/boot")
    [ "$BOOT" -gt 0 ] && [ "$BOOT" -lt 1000000000 ] || { state write_failed; return 1; }
    SLOT=$(((BOOT - 1) % 3)); return 0
  fi
  BOOT=$(read_value "$DIR/boot-counter")
  [ "$BOOT" -lt 999999999 ] || { state write_failed; return 1; }
  BOOT=$((BOOT + 1)); SLOT=$(((BOOT - 1) % 3))
  printf '%s\n' "$BOOT" > "$DIR/boot-counter.pending" || return 1
  mv -f "$DIR/boot-counter.pending" "$DIR/boot-counter" || return 1
  # Only this recorder's oldest boot slot is replaced, never unrelated data.
  for side in a b; do rm -f "$DIR/log-$SLOT$side.gz" "$DIR/meta-$SLOT$side" "$DIR/log-$SLOT$side.gz.pending" "$DIR/meta-$SLOT$side.pending"; done
  sync
  printf '%s\n' "$BOOT" > "$RAM/boot"; printf '0\n' > "$RAM/side"
}
case "${1:-}" in
  status) status;;
  request)
    probe && running || exit 1
    printf '1\n' > "$RAM/request";;
  clear)
    probe && running || exit 1
    printf '1\n' > "$RAM/clear-request";;
  clear-once)
    running && exit 1
    clear_logs;;
  has)
    valid_id "$2" && [ -f "$DIR/log-$2.gz" ] && [ ! -L "$DIR/log-$2.gz" ] && gzip -t "$DIR/log-$2.gz" 2>/dev/null;;
  cat)
    valid_id "$2" && [ -f "$DIR/log-$2.gz" ] && [ ! -L "$DIR/log-$2.gz" ] || exit 1
    cat "$DIR/log-$2.gz";;
  unpack)
    valid_id "$2" && [ -f "$DIR/log-$2.gz" ] && [ ! -L "$DIR/log-$2.gz" ] || exit 1
    gzip -cd "$DIR/log-$2.gz";;
  once)
    initialize && metrics && capture;;
  run)
    mkdir -p "$RAM"
    running && exit 0
    printf '%s\n' "$$" > "$RAM/pid"
    trap 'rm -f "$RAM/pid"' EXIT INT TERM
    state initializing
    tries=0
    until initialize; do tries=$((tries + 1)); [ "$tries" -lt 12 ] || exit 1; sleep 5; done
    last=-60
    while :; do
      if [ -f "$RAM/clear-request" ]; then
        rm -f "$RAM/clear-request"; clear_logs; last=$(now)
      fi
      metrics
      tick=$(now); request=0; [ ! -f "$RAM/request" ] || request=1
      if [ "$((tick - last))" -ge "$PERIOD" ] || { [ "$request" = 1 ] && [ "$((tick - last))" -ge 10 ]; }; then
        rm -f "$RAM/request"; capture; last=$tick
      fi
      sleep 5
    done;;
  *) exit 2;;
esac
