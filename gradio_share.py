import gradio as gr

import requests
import json

# Function to process the input text


def qo_qk_convertor(input_text):
    url = "http://127.0.0.1:7001/QO_QK_convertor"
    headers = {
        "Content-Type": "application/json"
    }
    # Wrap the input in the expected structure
    payload = {"di": input_text}
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Assuming the API returns a JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to process the input text
def process_text(input_text):
    input_text=json.loads(input_text)
    print("t imput", type(input_text))
    result = qo_qk_convertor(input_text)
    print("results:", result)
    return result

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Text Processing Tool\nEnter your long text below, click 'Run', and share the results!")

    with gr.Row():
        input_text = gr.Textbox(placeholder="Enter your long text here...", lines=10, label="Input Text")
        output_text = gr.Textbox(label="Processed Text", lines=10, interactive=False)

    # Process text when "Run" button is clicked
    gr.Button("Run").click(process_text, inputs=input_text, outputs=output_text)


    # def generate_share_link(input_text):
    #     """Generate a shareable link containing the input text."""
    #     base_url = "https://share.gradio.app/"  # Replace with your app's base URL if hosted elsewhere
    #     shareable_url = f"{base_url}?text={gr.utils.urlencode(input_text)}"
    #     return shareable_url





    # Generate shareable link when "Generate Shareable Link" button is clicked
    #share_button.click(generate_share_link, inputs=input_text, outputs=share_link)

# Launch the Gradio app
demo.launch(share=True)
