import requests
import gradio as gr
import os

def inference_interface(message, history, model_temperature):

  json_message = {
    "model": os.environ["MODEL_ID"],
    "messages": [],
    "temperature": 0.7
  }

  print("* History: " + str(history))

  system_message = {"role": "system", "content": "You are a helpful assistant."}
  json_message["messages"].append(system_message)
  json_message['temperature'] = model_temperature

  if len(history) == 0:
    print("** Before adding messages: " + str(json_message['messages']))
    # when there is no history
    new_user_message = {"role": "user", "content": message}
    json_message['messages'].append(new_user_message)
  else:
    print("** Before adding additional messages: " + str(json_message['messages']))
    # we have history
    for item in history:
      user_message = {"role": "user", "content": item[0]}
      assistant_message = {"role": "assistant", "content": item[1]}
      json_message["messages"].append(user_message)
      json_message["messages"].append(assistant_message)
    new_user_message = {"role": "user", "content": message}
    json_message["messages"].append(new_user_message)
      
  print("*** Request" + str(json_message), flush=True)
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

app.launch(server_name="0.0.0.0")
