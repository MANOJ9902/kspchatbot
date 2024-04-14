import streamlit as st
import openai
import json
import time

def load_api_key():
    with open('api_key.json') as f:
        data = json.load(f)
    return data['API_KEY']

def load_keywords(file_path):
    with open(file_path) as f:
        keywords = json.load(f)
    return keywords

def api_calling(prompt, keywords):
    for key in keywords:
        if key in prompt.lower():
            completions = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=150
            )
            response = completions.choices[0].text.strip()
            return response

    return "I'm sorry, I'm not knowledgeable about that topic."


# completions = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt="Prompt: " + prompt + "\n" + prompt,
#     max_tokens=150, # Adjust max_tokens as needed
#     n=1,
#     stop=None,
#     temperature=0.7, # Adjust temperature as needed
# )


st.sidebar.title("Accident Query Assistant")
st.sidebar.write("Welcome to the Accident Query Assistant!")
st.sidebar.write("Please enter your query related to accidents in the main panel.")

st.title("Accident Query Assistant By Karnataka State Police")

# Function to get user input with validation for coal mining-related prompts
def get_text():
    input_text = st.text_input("Enter your prompt related to Accidents:", key="input")
    if not input_text.lower().startswith("accident"):
        st.warning("Please start your prompt with 'Accident' for better results.")
    return input_text

user_input = get_text()

if user_input:
    with st.spinner("Generating response..."):
        time.sleep(2)  # Simulating a delay of 2 seconds
        openai.api_key = load_api_key()
        # Load keywords for each category
        accident_keywords = load_keywords('keywords/accident_keywords.json')
        road_rules_keywords = load_keywords('keywords/road_rules_keywords.json')
        traffic_rules_keywords = load_keywords('keywords/traffic_rules_keywords.json')

        # Check user input against each category of keywords
        output = api_calling(user_input, accident_keywords) \
                 or api_calling(user_input, road_rules_keywords) \
                 or api_calling(user_input, traffic_rules_keywords)

    # Display the output
    st.write("Response:")
    st.write(output)
