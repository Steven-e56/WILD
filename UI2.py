from __future__ import annotations
import subprocess
import gradio as gr
from typing import Iterable
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

# === Custom Gradio Theme ===
class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.gray,
        secondary_hue: colors.Color | str = colors.blue,
        neutral_hue: colors.Color | str = colors.slate,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Nunito"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )

seafoam = Seafoam()

# === Functions to Launch Scripts ===
def run_camera():
    subprocess.Popen(["python", "final_script_v3.py"])
    print("D.O.C. Eyes launching...")
    return "D.O.C. Eyes is launching..."

def run_chatbot():
    subprocess.Popen(["python", "DOC-chatbot.py"])
    print("D.O.C. Chat launching...")
    return "D.O.C. Chat is launching..."

# === Gradio UI ===
with gr.Blocks(theme=seafoam, css="""
#main-title {
    text-align: center;
    margin-bottom: 30px;
    font-size: 65px !important;
    font-weight: bold;
}
.square-button {
    width: 450px !important;
    height: 450px !important;
    font-size: 1.5em !important;
}
#status-box textarea {
    height: 100px !important;
    font-size: 1.1em;
}
""") as demo:
    gr.Markdown("Choose a D.O.C. Operation:", elem_id="main-title")

    with gr.Row(equal_height=True):
        camera_button = gr.Button("D.O.C. Eyes", elem_classes=["square-button"])
        chatbot_button = gr.Button("D.O.C. Chat", elem_classes=["square-button"])

    output = gr.Textbox(label="Status", lines=2, interactive=False, elem_id="status-box")

    camera_button.click(fn=run_camera, outputs=output)
    chatbot_button.click(fn=run_chatbot, outputs=output)

demo.launch(inbrowser=True)




# from __future__ import annotations
# import subprocess
# import gradio as gr
# import time

# # Import necessary types for the custom theme
# from typing import Iterable
# from gradio.themes.base import Base
# from gradio.themes.utils import colors, fonts, sizes

# """
 # === Diagnostic & Operational Communicator (DOC!) ===
 # === Created by JHUAPL (not) interns! ===
 # === AI-generated triage bot ===
# """

# # --- Custom Gradio Theme Definition (from your provided code) ---
# class Seafoam(Base):
    # def __init__(
        # self,
        # *,
        # primary_hue: colors.Color | str = colors.gray,
        # secondary_hue: colors.Color | str = colors.blue,
        # neutral_hue: colors.Color | str = colors.slate,
        # spacing_size: sizes.Size | str = sizes.spacing_md,
        # radius_size: sizes.Size | str = sizes.radius_md,
        # text_size: sizes.Size | str = sizes.text_lg,
        # font: fonts.Font
        # | str
        # | Iterable[fonts.Font | str] = (
            # fonts.GoogleFont("McLaren"),
            # "ui-sans-serif",
            # "sans-serif",
        # ),
        # font_mono: fonts.Font
        # | str
        # | Iterable[fonts.Font | str] = (
            # fonts.GoogleFont("IBM Plex Mono"),
            # "ui-monospace",
            # "monospace",
        # ),
    # ):
        # super().__init__(
            # primary_hue=primary_hue,
            # secondary_hue=secondary_hue,
            # neutral_hue=neutral_hue,
            # spacing_size=spacing_size,
            # radius_size=radius_size,
            # text_size=text_size,
            # font=font,
            # font_mono=font_mono,
        # )

# seafoam = Seafoam()
# # --- End of Custom Gradio Theme Definition ---


# # Below is the code used to start each file.
# # First string in the list is the language used
# # Second string in the list is the respective file for the source code

# # Define a variable to hold the main UI content that we can hide
# main_ui_container = None

# def run_camera():
    # global main_ui_container # Declare intent to modify the global variable
    # subprocess.Popen(["python", "final_script_v3.py"]) # Change this line to the respective camera file name!
    # print("DOC camera loading...") # For debugging purposes
    # # Return output for the status box and an update to hide the main UI
    # return "DOC camera loading...", gr.update(visible=False)

# def run_chatbot():
    # global main_ui_container # Declare intent to modify the global variable
    # subprocess.Popen(["python", "DOC-chatbot.py"]) #Change this line to the respective chatbot file
    # print("DOC chat-version opening...") # For debugging purposes
    # # Return output for the status box and an update to hide the main UI
    # return "DOC chat-version opening...", gr.update(visible=False)

# """Below is the UI using Gradio"""

# # Apply your custom 'seafoam' theme here
# with gr.Blocks(theme=seafoam) as demo: 
    # # Wrap all the UI components you want to hide in a Column
    # main_ui_container = gr.Row()
    # with main_ui_container:
        # gr.Markdown("## Choose an Option")

        # with gr.Row():
            # camera_button = gr.Button("DOC Eyes", scale=1)
            # chatbot_button = gr.Button("DOC Chat", scale=1)

        # # The output box will remain visible to show the status message
        # # but the buttons will disappear.
        # gr.Markdown("")
        # gr.Markdown("")
        # gr.Markdown("")
        # gr.Markdown("")
        # output = gr.Textbox(label="Status")

    # # Link the buttons to the functions
    # # The outputs now include both the 'output' textbox and the 'main_ui_container'
    # camera_button.click(fn=run_camera, outputs=[output, main_ui_container])
    # chatbot_button.click(fn=run_chatbot, outputs=[output, main_ui_container])

# demo.launch(inbrowser=True)

# """P.S. make sure the camera and chatbot file names are corrected on lines 15 and 19 as well as making
# sure they are in the same directory! """