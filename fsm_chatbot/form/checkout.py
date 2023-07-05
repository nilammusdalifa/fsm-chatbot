class Checkout:
    """_summary_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        self.slot = dict.fromkeys(['merk', 'tipe', 'jumlah', 'multiple'])

    def delete_slot_checkout(self):
        self.slot['merk'] = None
        self.slot['tipe'] = None
        self.slot['jumlah'] = None
        self.slot['multiple'] = None
        self.slot['harga'] = None