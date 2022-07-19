class RelRowStrategy:
    def __init__(self, ctx):
        self.ctx = ctx
        self.data = ctx.data # import data from context

    def build_row(self):
        '''Override this function for each strategy'''
        pass