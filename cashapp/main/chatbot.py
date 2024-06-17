from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def get_chatbot():
    chatbot = ChatBot('FinanceBot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english.finance")
    return chatbot


chatbot = get_chatbot()
