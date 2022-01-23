class Config:
    def __init__(self, **kwargs):
        self.n_per_page = kwargs.get('n_per_page', 1)
        self.dry = kwargs.get('dry', True)

        self.file = kwargs.get('file')
        self.printer = kwargs.get('printer')
