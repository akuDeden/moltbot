#!/bin/bash
# Moltbot Gateway Runner
# Usage: ./moltbot-runner.sh [start|stop|restart|status]

MOLTBOT_DIR="/Users/ahmadfaris/moltbot"
LOG_FILE="/tmp/moltbot-gateway.log"
PID_FILE="/tmp/moltbot-gateway.pid"

start() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "❌ Gateway sudah running (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    echo "🚀 Starting moltbot gateway..."
    cd "$MOLTBOT_DIR"
    
    # Start gateway di background
    nohup pnpm moltbot gateway run --bind loopback --port 18789 > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 2
    
    if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "✅ Gateway started (PID: $(cat $PID_FILE))"
        echo "📄 Log: $LOG_FILE"
    else
        echo "❌ Gateway failed to start. Check log: $LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️  PID file not found. Killing by process name..."
        pkill -9 -f moltbot-gateway
        echo "✅ Killed all moltbot-gateway processes"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    echo "🛑 Stopping gateway (PID: $PID)..."
    
    if kill -0 $PID 2>/dev/null; then
        kill -9 $PID
        rm -f "$PID_FILE"
        echo "✅ Gateway stopped"
    else
        echo "⚠️  Process not running, cleaning up..."
        rm -f "$PID_FILE"
        pkill -9 -f moltbot-gateway
    fi
}

restart() {
    echo "🔄 Restarting gateway..."
    stop
    sleep 1
    start
}

status() {
    echo "📊 Moltbot Gateway Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "✅ Status: Running"
            echo "🆔 PID: $PID"
            echo "📄 Log: $LOG_FILE"
            echo ""
            echo "Recent logs:"
            tail -n 10 "$LOG_FILE"
        else
            echo "❌ Status: Dead (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        # Check by process name
        if pgrep -f moltbot-gateway > /dev/null; then
            echo "⚠️  Status: Running (no PID file)"
            echo "PIDs: $(pgrep -f moltbot-gateway | tr '\n' ' ')"
        else
            echo "⭕ Status: Stopped"
        fi
    fi
    
    # Check port
    echo ""
    if lsof -i :18789 > /dev/null 2>&1; then
        echo "🔌 Port 18789: IN USE"
    else
        echo "🔌 Port 18789: FREE"
    fi
}

logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "❌ Log file not found: $LOG_FILE"
        return 1
    fi
    
    echo "📄 Tailing logs (Ctrl+C to stop)..."
    tail -f "$LOG_FILE"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start    - Start moltbot gateway"
        echo "  stop     - Stop moltbot gateway"
        echo "  restart  - Restart moltbot gateway"
        echo "  status   - Show gateway status"
        echo "  logs     - Tail gateway logs"
        exit 1
        ;;
esac
