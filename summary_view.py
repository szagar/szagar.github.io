import typer
from pymongo import MongoClient

app = typer.Typer()


@app.command()
def view1(symbol: str, robust_level: int = 3):

    password = r"Marley%2399"
    client = MongoClient(
        f"mongodb+srv://zts:{password}@mdb-cluster-1.99iny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.zts
    strategy = db.strategies
    for doc in strategy.find(
        {"status": "Strategy", "state": "Ready", "symbol": symbol, "robust_level": robust_level}
    ).sort("strategy_long_name"):
        bt = doc["backtest"]["metrics_all_trades"]
        print(bt)
        print(
            f"{doc['strategy_long_name']:25}{bt['profit_factor']:4.1f}{bt['avg_trade']:6.2f}{bt['total_trades']:6d}"
        )


if __name__ == "__main__":
    app()
