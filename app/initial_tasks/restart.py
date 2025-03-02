from blinker import signal

reload_signal = signal('reload-app')

# In your blueprint code
@reload_signal.connect
def handle_reload(sender):
    # Recreate your blueprint and re-register it
    recreate_dynamic_apis_blueprint()

# In your API endpoint
@app.route('/api/sync', methods=['POST'])
def sync_application():
    reload_signal.send(app)
    return jsonify({"status": "synced"})