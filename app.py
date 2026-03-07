from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO
import socket
import requests
import argparse


app = Flask(__name__)
socketio = SocketIO(app)

CONNECTIONS = set() # Tracks with which peers one is connected
            
def get_my_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
    finally:
        sock.close()
        
def get_my_connection():
    my_port = request.host.split(':')[-1]
    return f"{get_my_ip()}:{my_port}"
    
        
# =============================================================================
#   Events
# =============================================================================
@socketio.on('connect_to_peer')
def handle_connect_to_peer(data):
    peer_ip = data.get('peer_ip')
    
    if not peer_ip:
        socketio.emit('connect_response', {
            'success': False,
            'message': 'peer_ip is required'
        })
        return
        
    try:
        json = { 'from_ip': get_my_connection(), 'to_ip': peer_ip }
        url = f"http://{peer_ip}/webhook/connect_request"
        response = requests.post(url, json=json)
        
        if response.status_code != 200:
            socketio.emit('connect_response', {
                'success': False,
                'message': 'Failed to request connection'
            })
    except Exception as e:
        print(e)
        socketio.emit('connect_response', {
            'success': False,
            'message': 'Error connecting to peer'
        })
        
@socketio.on('connect_confirmation')
def confirm_connect(data):
    try:
        url = f"http://{data['to_ip']}/webhook/connect_confirm"

        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            CONNECTIONS.add(data['to_ip'])
            socketio.emit('goto_chat', { 'to_ip': data['to_ip'] })
        else:
            socketio.emit('connect_response', {
                'success': False,
                'message': 'Failed to allow connection'
            })
    except Exception as e:
        print(e)
        socketio.emit('connect_response', {
            'success': False,
            'message': 'Error connecting to peer'
        })
        
@socketio.on('chat_send_message')
def handle_chat_message(data):
    print(data)
    
    message = data['message']
    to_ip = data['to_ip']

    if not message or not to_ip: return

    try:
        url = f"http://{to_ip}/webhook/receive_message"
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            socketio.emit('chat_send_response', {
                'success': True,
                'message': message
            })
        else:
            socketio.emit('chat_send_response', {
                'success': False,
                'message': 'Failed to send message'
            })
    except Exception as e:
        print(e)
        socketio.emit('chat_send_response', {
            'success': False,
            'message': 'Error connecting to peer'
        })    
            
# =============================================================================
#   Routes
# =============================================================================
@app.route('/')
def index():    
    return render_template('index.html', my_ip=get_my_connection())

@app.route('/chat')
def chat():
    to_ip = request.args.get('peer_ip')
    from_ip = get_my_connection()
    
    if (not to_ip) or (to_ip not in CONNECTIONS):
        return redirect(url_for('index'))
    
    return render_template('chat.html', to_ip=to_ip, from_ip=from_ip)

# Web hooks ___________________________________________________________________    
@app.route('/webhook/connect_request', methods=['POST'])
def connect_request():
    data = request.json
    socketio.emit('connect_request', data)
    return jsonify({"message": "Connection request sent"}), 200

@app.route('/webhook/connect_confirm', methods=['POST'])
def connect_confirm():
    data = request.json
    
    if data['allow']:
        CONNECTIONS.add(data['from_ip'])
        data = { 'to_ip': data['from_ip'] }
        socketio.emit('goto_chat', data)
        return jsonify({"message": "Connection made"}), 200
    else:
        socketio.emit('connect_response', {
            'success': False,
            'message': 'Connection request was denied'
        })
        
@app.route('/webhook/receive_message', methods=['POST'])
def receive_message():
    data = request.json
    socketio.emit('chat_receive_message', data)
    return jsonify({"message": "Message sent successfully"}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a Flask chat server instance")
    parser.add_argument('--port', type=int, default=5000, help="Port to run the server on")
    
    args = parser.parse_args()
    
    socketio.run(app, host='0.0.0.0', port=args.port, debug=True)