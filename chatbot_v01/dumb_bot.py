import csv

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot import comparisons
from chatterbot import response_selection

dumbo = ChatBot(
    'Dumbo',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': comparisons.LevenshteinDistance,
            'response_selection_method': response_selection.get_first_response,
        }
    ],
    database_uri='sqlite:///enrollment_chat_db.db'
)

dialogue_pairs = []

# load Conversation.csv file
# with open('Conversation.csv', 'r', newline='', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         questions = row[1]
#         answers = row[2]
#         dialogue_pairs.append(questions)
#         dialogue_pairs.append(answers)

# for pair in dialogue_pairs:
#     print(pair, type(pair))

trainer = ChatterBotCorpusTrainer(dumbo)

trainer.train('./dumbo_trainer.yml')

trainer.train('./beekeeper_cleaned.yml')

while True:
    try:
        print(dumbo.get_response(input("User: ")))

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
