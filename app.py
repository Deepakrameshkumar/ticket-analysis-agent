from flask import Flask, render_template, request
from flask_socketio import SocketIO
import yaml
import os
from src.workflow import create_workflow
from src.chat_handler import ChatHandler

app = Flask(__name__)
socketio = SocketIO(app)

# Load config
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

workflow = create_workflow(config)
chat_handler = ChatHandler(config['model']['path'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(config['data']['upload_dir'], file.filename)
            file.save(filepath)
            
            # Run workflow
            result = workflow.run({"file_path": filepath})
            chat_handler.set_data(result)
            
            return render_template('report.html', report=result['summary'])
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    response = chat_handler.chat(message)
    socketio.emit('response', response)

if __name__ == '__main__':
    os.makedirs(config['data']['upload_dir'], exist_ok=True)
    socketio.run(app, debug=True)