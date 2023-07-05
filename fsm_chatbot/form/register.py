class Register():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    def __init__(self):
        self.slot = dict.fromkeys(['nama', 'email', 'pass'])

    def delete_slot_regis(self):
        self.slot['nama'] = None
        self.slot['email'] = None
        self.slot['pass'] = None