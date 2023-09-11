import openai
from typing import Optional
key = "sk-EMsGrX6d6VsQ09isuTeST3BlbkFJScrbZx654ofD8BFVZFfD" //Add a working personal key! 
openai.api_key = key

#try placing the key into a txt file and use withopen and file.read to get the key*

def get_api_response(prompt: str) -> Optional[str]: #returns either string, or an optional none to resolve a bad case
    text: Optional[str] = None
    
    try:
        response: dict = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            temperature = 0.9, #affects the randomness of ai responses
            max_tokens = 150,
            top_p = 1, #alternative to temperature
            frequency_penalty = 0, #affects repetition of words
            presence_penalty = 0.6, #affects the diversity of words
            stop = [' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print("ERROR:", e)

    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response
def main():
    prompt_list: list[str] = ['You are a helper who aids in answering questions for people in a helpful and kind manner. Always use a friendly and helpful tone that sympathizes with the user and helps explain concepts or step to people. ',
                              '\nHuman: What time is it?'
                              '\nAI: It is 12:00PM']
    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, prompt_list)
        print(f'Bot: {response}')

if __name__ == '__main__':
    main()
