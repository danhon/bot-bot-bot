class TraceryBot:
    """A JSON-defined tracery bot"""

    def __init__(self, name, grammar_json, grammar_directory, corpora_directory):
        self.name = name
        self.grammar_json = grammar_json
        self.grammar_directory = grammar_directory
        self.corpora_directory = corpora_directory
        self.corpora = []
        self.service = []
        

class BotService:
    """Defines a bot service"""

    def __init__(self, service_type):
        self.service_type = service_type
        self.username = username
        self.password = client
        self.threaded = threaded


