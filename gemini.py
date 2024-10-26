import google.generativeai as genai
import os, time

import requests
import imageio
import io

from sat import ImgSat

def upload_sat_img(link):
    response = requests.get(link)
    response.raise_for_status()

    gif_bytes = io.BytesIO(response.content)
    gif = imageio.mimread(gif_bytes, format='gif')

    video_bytes = io.BytesIO()
    imageio.mimsave(video_bytes, gif, format='mp4', fps=2)
    video_bytes.seek(0)
    response = genai.upload_file(video_bytes, mime_type='video/mp4')
    return response


if __name__ == "__main__":
    genai.configure(api_key=os.environ['GEMINI_KEY'])
    model = genai.GenerativeModel("gemini-1.5.flash")
    isat = ImgSat()
    link = isat.query(26.5624, -80.044)
    video_file = upload_sat_img(link)
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    # Create the prompt.
    prompt = "What is this?"

    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Make the LLM request.
    print("Making LLM inference request...")
    response = model.generate_content([prompt, video_file],
                                    request_options={"timeout": 600})

    # Print the response, rendering any Markdown
    print(response.text)
    


    
