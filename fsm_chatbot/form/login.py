class Login:
    """_summary_
    """
    
    def __init__(self):
        self.slot = dict.fromkeys(['email', 'pass'])

    def delete_slot_login(self):
        self.slot['email'] = None
        self.slot['pass'] = None