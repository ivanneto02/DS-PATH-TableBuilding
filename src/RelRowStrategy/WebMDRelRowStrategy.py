from .RelRowStrategy import RelRowStrategy

class WebMDRelRowStrategy(RelRowStrategy):
    def build_row(self, row):
        return ["a", "b", "c", "webmd"]