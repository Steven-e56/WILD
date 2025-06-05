import subprocess
import gradio as gr

""" 
 === Diagnostic & Operational Communicator (DOC!) ===
 === Created by JHUAPL (not) interns! ===
 === AI-generated triage bot === 
"""

#Below is the code used to start each file.
#First string in the list is the language used
#Second string in the list is the respecive file for the source code

def run_camera():
    subprocess.Popen(["python", "final_script_v3.py"]) # Change this line to the respective camera file name!
    return "DOC camera loading..."
    
def run_chatbot():
    subprocess.Popen(["python", "DOC-chatbot.py"]) #Change this line to the respective chatbot file
    return "DOC chat-version opening..."
    
"""Below is the UI using Gradio"""

with gr.Blocks() as demo:
    gr.Markdown("## Choose an Option")
    
    with gr.Row():
        camera_button = gr.Button("DOC Eyes")
        chatbot_button = gr.Button("DOC Chat")
        
    output = gr.Textbox(label="Status")
    
    camera_button.click(fn=run_camera, outputs=output)
    chatbot_button.click(fn=run_chatbot, outputs=output)
    
demo.launch()

"""P.S. make sure the camera and chatbot file names are corrected on lines 15 and 19 as well as making
sure they are in the same directory! """