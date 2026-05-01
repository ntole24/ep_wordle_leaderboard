class wordle_player:
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.total = 0

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_total(self):
        return self.total
    
    def add_total(self, guess_number):
        self.total = self.total + guess_number

    