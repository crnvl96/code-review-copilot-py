from config.tinyllama_config import ModelConfig
from model.tinyllama import TinyLlama
from pipeline.github_pipe import Github, Platform


class CodeReview:
    def __init__(self, platform: Platform):
        self.platform = platform

    def generate(self) -> None:
        self.platform.review()


def main():
    config = ModelConfig()
    model = TinyLlama(config)
    platform = Github(model)
    review = CodeReview(platform)

    review.generate()


if __name__ == "__main__":
    main()
