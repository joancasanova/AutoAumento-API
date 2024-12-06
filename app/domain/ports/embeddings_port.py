class EmbeddingsPort:
    def get_similarity(self, text1: str, text2: str) -> float:
        """Return a similarity score between text1 and text2."""
        raise NotImplementedError
