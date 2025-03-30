from flask import Flask, render_template, request
from flask_socketio import SocketIO
import yaml
import os
import logging
from src.workflow import create_workflow, run_workflow
from src.chat_handler import ChatHandler

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app)

with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

workflow = create_workflow(config)
chat_handler = ChatHandler(config['model'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(config['data']['upload_dir'], file.filename)
            file.save(filepath)
            
            initial_state = {"file_path": filepath}
            logger.debug(f"Starting workflow with initial state: {initial_state}")
            result = run_workflow(workflow, initial_state)
            logger.debug(f"Workflow result: {result}")
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