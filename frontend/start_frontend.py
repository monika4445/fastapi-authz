#!/usr/bin/env python3
"""
start_frontend.py - Easy way to serve your index.html on port 3000
Place this file in the same directory as your index.html and run it
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_frontend_server():
    PORT = 3000
    
    # Check if index.html exists in current directory
    if not Path("index.html").exists():
        print("❌ Error: index.html not found in current directory")
        print("💡 Make sure you're in the same folder as your index.html file")
        sys.exit(1)
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    
    print("🚀 FastAPI Auth Service Frontend")
    print("=" * 50)
    print(f"✅ Server starting on port {PORT}")
    print(f"🌐 Frontend URL: http://localhost:{PORT}")
    print(f"📂 Serving from: {os.getcwd()}")
    print("=" * 50)
    print("📧 Email verification links will now work perfectly!")
    print("🔗 Links format: http://localhost:3000?token=abc123")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Auto-open browser
    try:
        webbrowser.open(f"http://localhost:{PORT}")
        print("🎉 Browser opened automatically!")
    except:
        print("💡 Manually open: http://localhost:3000")
    
    print()
    
    # Start server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()
        print("✅ Frontend server shut down cleanly")

if __name__ == "__main__":
    start_frontend_server()