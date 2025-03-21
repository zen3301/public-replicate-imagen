from cog import BasePredictor

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(self) -> str:
        return "hello world"