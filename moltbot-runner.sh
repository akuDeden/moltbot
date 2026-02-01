#!/bin/bash
# OpenClaw Gateway Runner
# Usage: ./moltbot-runner.sh [start|stop|restart|status|logs]

LOG_FILE="/tmp/openclaw-gateway.log"

start() {
    echo "🚀 Starting OpenClaw gateway..."
    openclaw gateway start
    echo ""
    echo "📊 Dashboard: http://127.0.0.1:18789/"
    echo "📄 Logs: openclaw logs --follow"
}

stop() {
    echo "🛑 Stopping OpenClaw gateway..."
    openclaw gateway stop
    echo "✅ Gateway stopped"
}

restart() {
    echo "🔄 Restarting OpenClaw gateway..."
    openclaw gateway restart
    echo "✅ Gateway restarted"
    echo ""
    echo "📊 Dashboard: http://127.0.0.1:18789/"
}

status() {
    echo "📊 OpenClaw Gateway Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    openclaw gateway status
    echo ""
    echo "Dashboard: http://127.0.0.1:18789/"
}

logs() {
    echo "📄 Tailing logs (Ctrl+C to stop)..."
    openclaw logs --follow
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
        echo "  start    - Start OpenClaw gateway"
        echo "  stop     - Stop OpenClaw gateway"
        echo "  restart  - Restart OpenClaw gateway"
        echo "  status   - Show gateway status"
        echo "  logs     - Tail gateway logs"
        echo ""
        echo "Direct commands:"
        echo "  openclaw gateway start"
        echo "  openclaw status"
        echo "  openclaw logs --follow"
        exit 1
        ;;
esac
