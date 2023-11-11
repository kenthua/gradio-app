import requests
import gradio as gr
import os

json_message = {
  "model": os.environ["MODEL_ID"],
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the top 5 most popular programming languages? Please be brief."}
  ],
  "temperature": 0.7
}

def inference_interface(message, history, model_temperature):
  json_message['messages'][1]["content"] = message
  json_message['temperature'] = model_temperature

  print("request" + str(json_message))
  response = requests.post(os.environ["HOST"] + os.environ["CONTEXT_PATH"], json=json_message)
  json_data = response.json()
  output = json_data["choices"][0]["message"]["content"]
  return output 

with gr.Blocks() as app:
  model_temperature = gr.Slider(minimum=0.1, maximum=1.0, value=0.7, label="Temperature", render=False)
  gr.ChatInterface(
    inference_interface,
    additional_inputs=[
        model_temperature
    ]
  )

app.launch()
