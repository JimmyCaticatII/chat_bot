from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# create bot instance
bot = ChatBot(
    "Dumbo",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///database.sqlite3",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        {
            "import_path": "chatterbot.logic.SpecificResponseAdapter",
            "input_text": "Name and nature?",
            "output_text": "Dumbo, a chatbot."
        },
        "chatterbot.logic.MathematicalEvaluation",
        # "chatterbot.logic.TimeLogicAdapter",
    ]
)

# create trainer using list trainer
trainer = ListTrainer(bot)

trainer.train([
    "Hello",
    "Hi there",
    "How are you?",
    "I'm doing well.",
    "That is good to hear",
    "Thank you",
    "You're welcome"
])

# get response
while True:
    try:
        user_input = input("User: ")
        bot_input = bot.get_response(user_input)
        print(f"Bot: {bot_input}")

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
