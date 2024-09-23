from config.schema import Config


def main():
    schema = Config().schema

    print(schema)


if __name__ == "__main__":
    main()
