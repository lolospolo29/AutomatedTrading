from main.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum


def main():
    res = StrategyResultStatusEnum.NEWTRADE.value

    match res:
        case "NEWTRADE":  # Match against the actual value
            print("NEWTRADE")
        case _:  # Catch-all for unmatched cases
            print("No match")

if __name__ == "__main__":
    main()