import cohere
import json

co = cohere.Client(
    api_key="4UrXb6IpkzMjQKXyufNd1G8ZbV0XJgj0njjSQ9Se"
)

# load chat history
with open('rules.json', 'r') as lf:
    chat_history = json.load(lf)


def export_chat_history(sorted_chat_history):
    with open('chat_history.json', 'w') as sf:
        json.dump(sorted_chat_history, sf, indent=4, sort_keys=True)

    print("Chat history exported.")


def export_for_dumbo(sorted_chat_history):
    with open('dumbo_trainer.yml', 'w') as f:
        f.write('categories:\n- enrollment\nconversations:\n')

        for line in sorted_chat_history:
            if '\n' in line['message']:
                line['message'] = line['message'].replace('\n', '')
            if line['role'] in ['USER', 'SYSTEM']:
                f.write('- - "' + line['message'] + '"\n')
            else:
                f.write('  - "' + line['message'] + '"\n')


answer_list = []
message = "Hey MAYA!"
enrollment_assistant_preamble = '''
## Task & Context
Your name is MAYA and you are a professional enrollment assistant that students can ask 
questions about when enrolling in a course at the School of Information Technology in the University of Baguio.

## Style Guide
Always start a new chat session by briefly introducing yourself and asking the student's current year level. Be brief 
and concise in responding, however you can respond in lengthy explanations only if you are asked to elaborate/expound.
'''

print("MAYA - ENROLLMENT ASSISTANCE CHATBOT")
print("Starting MAYA. Type 'quit' to exit.")

while True:
    try:
        # get bot response
        for event in co.chat(
                message=message,
                model="command",
                chat_history=chat_history,
                preamble_override=enrollment_assistant_preamble,
                stream=True
        ):
            if event.event_type == "text-generation":
                answer = event.text
                print(f'{answer}', end="")
                answer_list.append(answer)

        bot_answer = ''.join(answer_list)
        answer_list.clear()

        # get user message
        message = input("\nUser: ")

        # add message and answer to the chat history
        bot_message = {
            "role": "CHATBOT",
            "message": bot_answer
        }
        user_message = {
            "role": "USER",
            "message": message
        }

        chat_history.append(bot_message)
        chat_history.append(user_message)
        for i in chat_history:
            i['id'] = chat_history.index(i)

        sorted_chat_history = sorted(chat_history, key=lambda x: x['id'])

        if message == "quit":
            print('Ending MAYA.')
            export_chat_history(sorted_chat_history)  # train for the  api
            export_for_dumbo(sorted_chat_history)  # training set for dumbo
            break

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
