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
    
    # Load LaunchAgent if exists (prefer Mac app method)
    if [ -f ~/Library/LaunchAgents/bot.molt.gateway.plist ]; then
        echo "🔐 Loading LaunchAgent..."
        launchctl load ~/Library/LaunchAgents/bot.molt.gateway.plist 2>/dev/null
        sleep 2
        if pgrep -f "moltbot.*gateway" > /dev/null 2>&1; then
            echo "✅ Gateway started via LaunchAgent"
            return 0
        fi
    fi
    
    # Fallback: manual start
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
    echo "🛑 Stopping moltbot gateway..."
    
    # Unload LaunchAgent if exists (Mac app auto-restart)
    if [ -f ~/Library/LaunchAgents/bot.molt.gateway.plist ]; then
        echo "🔓 Unloading LaunchAgent..."
        launchctl unload ~/Library/LaunchAgents/bot.molt.gateway.plist 2>/dev/null
    fi
    
    # Kill all moltbot gateway processes (parent + children)
    pkill -9 -f "moltbot.*gateway" 2>/dev/null
    
    # Clean up PID file
    rm -f "$PID_FILE"
    
    # Verify all killed
    sleep 1
    if pgrep -f "moltbot.*gateway" > /dev/null 2>&1; then
        echo "⚠️  Some processes still running, forcing kill..."
        pkill -9 -f "moltbot"
    fi
    
    echo "✅ Gateway stopped (LaunchAgent unloaded)"
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
        if pgrep -f "moltbot.*gateway" > /dev/null; then
            echo "⚠️  Status: Running (no PID file)"
            echo "PIDs: $(pgrep -f 'moltbot.*gateway' | tr '\n' ' ')"
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
