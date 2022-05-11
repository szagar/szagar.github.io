from pathlib import Path
from plistlib import FMT_BINARY
import typer
from rich import print
from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# from global_config import cnf
# import nosql.mongo_setup as mongo_setup

app = typer.Typer()

# def config_mongo():
#    user = cnf.MONGO_USER
#    pw = cnf.MONGO_PASSWORD
#    server = cnf.MONGO_SERVER
#    print(f"{user=} {pw=} {server=}")
#    user = 'zts'
#    pw = 'Marley#99'
#    server = 'mongodb+srv://mdb-cluster-1.99iny.mongodb.net'
#    mongo_setup.global_init(user=user, password=pw, server=server)


def lookup_sector(symbol: str):
    return "tbd"


def front_matter(doc: dict, layout: str):
    sector = lookup_sector(doc["symbol"])
    fm_d = {
        "layout": layout,
        "title": "frontmatter title",
        "name": "frontmatter name",
        "source": doc["source"],
        "strategy_name": doc["strategy_name"],
        "strategy_long_name": doc["strategy_long_name"],
        "market": doc["symbol"],
        "sector": sector,
        "style": doc["trade_style"],
        "dayswing": doc["day_swing"],
        "longshort": doc["long_short"],
        "robust_level": doc["robust_level"],
        "tags": doc["tags"],
        "session": doc["settings"]["market_session"],
        "timeframe": f'{doc["settings"]["entry_timeframe"]}{doc["settings"]["entry_timeframe_unit"]}',
        "dpt": doc["process_metrics"]["dpt_applied"],
        "dps": doc["process_metrics"]["dps_applied"],
        "sfb": doc["process_metrics"]["sfb_applied"],
    }
    return fm_d


def bt_metrics(bt):
    print("bt_metrics")
    m = {
        "net_profit": bt["net_profit"],
        "trades": bt["total_trades"],
        "%winners": f'{bt["percent_profitable"]/100:.2%}',
        "avg trade": bt["avg_trade"],
        "win loss ratio": bt["win_loss_ratio"],
        "profit factor": bt["profit_factor"],
        "max intra dd": bt["max_intraday_drawdown"],
    }
    return m


def equity_curve(doc):
    print("equity_curve")
    if doc["backtest"]["test_type"] != "WF-OOS":
        print(f"WARNING: WF-OOS metrics not available for {doc['strategy_name']}")
        quit()

    bt_d = doc["backtest"]
    if "bt_start_dt" in bt_d:
        bt_start_dt = datetime.strftime(bt_d["bt_start_dt"], "%m/%d/%Y")
        bt_end_dt = datetime.strftime(bt_d["bt_end_dt"], "%m/%d/%Y")
    else:
        bt_start_dt = "na"
        bt_end_dt = "na"
    # fmt: off
    ec_d = {
        "name":             bt_d["backtest_name"],
        "trade_list_url":   bt_d["trade_list_url"],
        "equity_curve_url": bt_d["equity_curve_url"],
        "bt_start_dt":      bt_start_dt,
        "bt_end_dt":        bt_end_dt,
        "xact_costs":       bt_d["xact_costs"],
        "metrics":          bt_metrics(bt_d["metrics_all_trades"]),
    }
    # fmt: on
    return ec_d


def cross_markets(doc):
    print("cross_markets")
    cm_a = []
    for bt_doc in doc["cross_market_tests"]:
        bt_d = {
            "name": bt_doc["backtest_name"],
            "trade_list_url": bt_doc["trade_list_url"],
            "equity_curve_url": bt_doc["equity_curve_url"],
            "bt_start_dt": datetime.strftime(bt_doc["bt_start_dt"], "%m/%d/%Y"),
            "bt_end_dt": datetime.strftime(bt_doc["bt_end_dt"], "%m/%d/%Y"),
            "xact_costs": bt_doc["xact_costs"],
            "metrics": bt_metrics(bt_doc["metrics_all_trades"]),
        }
        cm_a.append(bt_d)
    return cm_a


def mae(doc):
    print("mae")
    if "mae_url" not in doc:
        return {}
    mae_d = {
        "mae_url": doc["mae_url"],
        "suggestions": [500, 1000, 1500],
    }
    return mae_d


def mfe(doc):
    mfe_d = {}
    return mfe_d


def strategy_sheet_fn(strategy_name: str):
    return f"{strategy_name}.md"


def write_strategy_sheet(sheet_data):
    fn = Path("_strategies") / strategy_sheet_fn(sheet_data["strategy_name"])
    with open(fn, "w") as fh:
        fh.write("---\n")
        for k, v in sheet_data["front_matter"].items():
            fh.write(f"{k:20}: {v}\n")
        fh.write("---\n")

        fh.write("equity_curve<br>\n")
        fh.write(
            f"<img src='{sheet_data['equity_curve']['equity_curve_url']}' alt='' border=3 height=200>"
        )
        fh.write("<br><br>\n")
        for k, v in sheet_data["equity_curve"].items():
            fh.write("================\n")
            fh.write(f"{k:20}: {v}<br>\n")

        fh.write("cross_markets<br>\n")
        for cm in sheet_data["cross_markets"]:
            print(sheet_data.keys())
            fh.write(f"<img src='{cm['equity_curve_url']}' alt='' border=3 height=100>")
            # fh.write(f"![image tooltip here]({cm['equity_curve_url']})")
            # for k, v in cm.items():
            #    fh.write(f"{k:20}: {v}<br>\n")
        fh.write("<br><br>\n")

        fh.write("MAE\n")
        for k, v in sheet_data["mae"].items():
            fh.write(f"{k:20}: {v}<br>\n")

        fh.write("MFE\n")
        for k, v in sheet_data["mfe"].items():
            fh.write(f"{k:20}: {v}<br>\n")

    return fh


def write_static_page(page_data):
    page = "_strategies/new_page.md"
    with open(page, "w") as fh:
        fh.write("---\n\n")
        for k, v in page_data["front_matter"].items():
            fh.write(f"{k}: '{v}'\n")
        fh.write("---\n\n")

        for l in page_data["content"]:
            fh.write(l + "\n")


@app.command()
def strategy_sheet(strategy_name: str):

    password = r"Marley%2399"
    client = MongoClient(
        f"mongodb+srv://zts:{password}@mdb-cluster-1.99iny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.zts
    strategy = db.strategies
    print(strategy)
    sheet_data = {
        "strategy_name": strategy_name,
    }
    for doc in strategy.find({"strategy_name": strategy_name}):
        pprint(doc)
        print(f"long_name = {doc['strategy_long_name']}")
        sheet_data["front_matter"] = front_matter(doc, layout="strategy_sheet")
        sheet_data["equity_curve"] = equity_curve(doc)
        sheet_data["cross_markets"] = cross_markets(doc)
        sheet_data["mae"] = mae(doc)
        sheet_data["mfe"] = mfe(doc)
    print(sheet_data)
    pprint(sheet_data)
    write_strategy_sheet(sheet_data)


@app.command()
def dpt_compare():
    password = r"Marley%2399"
    client = MongoClient(
        f"mongodb+srv://zts:{password}@mdb-cluster-1.99iny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.zts
    strategy = db.strategies
    cmp_data = {}
    print(
        f"{'DPT':>20} / {'Parent':15} {'Mkt':>4} {'NetProfit':>22} {'ProfitFactor':>20} {'AvgTrade':>16}"
    )
    cmp_data["front_matter"] = {"layout": "compare_dpt"}
    cmp_data["content"] = []

    cmp_data["content"].append("<table border=1>")
    cmp_data["content"].append("<tr>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("Strategy")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("NetProfit")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("PF")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("AvgTrade")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("Parent")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("  <th>")
    cmp_data["content"].append("DPT")
    cmp_data["content"].append("  </th>")
    cmp_data["content"].append("</tr>")

    summ_np = 0
    summ_pf = 0
    summ_at = 0
    cnt = 0
    for dpt_doc in strategy.find({"source": "DPT_opt"}):
        # print(dpt_doc["strategy_name"], dpt_doc["symbol"])
        p_doc = strategy.find_one({"_id": ObjectId(dpt_doc["parent_id"])})
        # print(p_doc["strategy_name"], p_doc["backtest"]["metrics_all_trades"].keys())
        # print(
        #    f'{p_doc["strategy_name"]:20} {p_doc["backtest"]["metrics_all_trades"]["net_profit"]:,} {p_doc["backtest"]["metrics_all_trades"]["profit_factor"]:5.02} {p_doc["backtest"]["metrics_all_trades"]["avg_trade"]:6.2f}'
        # )
        # print(
        #    f'{dpt_doc["strategy_name"]:20} {dpt_doc["backtest"]["metrics_all_trades"]["net_profit"]:,} {float(dpt_doc["backtest"]["metrics_all_trades"]["profit_factor"]):5.2} {dpt_doc["backtest"]["metrics_all_trades"]["avg_trade"]:6.2f}'
        # )
        # print(
        #    f'{"compare":>20} {dpt_doc["backtest"]["metrics_all_trades"]["net_profit"]-p_doc["backtest"]["metrics_all_trades"]["net_profit"]:,} {(dpt_doc["backtest"]["metrics_all_trades"]["profit_factor"]-p_doc["backtest"]["metrics_all_trades"]["profit_factor"]):.2} {(dpt_doc["backtest"]["metrics_all_trades"]["avg_trade"]-p_doc["backtest"]["metrics_all_trades"]["avg_trade"]):6.2f}'
        # )
        # print(dpt_doc["strategy_name"], dpt_doc["parent_id"])

        cnt += 1

        dpt_s = dpt_doc["strategy_name"]
        parent_s = p_doc["strategy_name"]
        symbol = p_doc["symbol"]
        np_diff = (
            dpt_doc["backtest"]["metrics_all_trades"]["net_profit"]
            - p_doc["backtest"]["metrics_all_trades"]["net_profit"]
        )
        np_perc = np_diff / abs(p_doc["backtest"]["metrics_all_trades"]["net_profit"])
        summ_np += np_perc
        pf_diff = (
            dpt_doc["backtest"]["metrics_all_trades"]["profit_factor"]
            - p_doc["backtest"]["metrics_all_trades"]["profit_factor"]
        )
        pf_perc = pf_diff / abs(p_doc["backtest"]["metrics_all_trades"]["profit_factor"])
        summ_pf += pf_perc
        # print(
        #    dpt_doc["backtest"]["metrics_all_trades"]["net_profit"],
        #    p_doc["backtest"]["metrics_all_trades"]["net_profit"],
        #    np_diff,
        #    np_perc,
        # )
        at_diff = (
            dpt_doc["backtest"]["metrics_all_trades"]["avg_trade"]
            - p_doc["backtest"]["metrics_all_trades"]["avg_trade"]
        )
        at_perc = at_diff / abs(p_doc["backtest"]["metrics_all_trades"]["avg_trade"])
        summ_at += at_perc
        # print(f'pf: {dpt_doc["backtest"]["metrics_all_trades"]["profit_factor"]}')
        # print(f'pf: {p_doc["backtest"]["metrics_all_trades"]["profit_factor"]}')

        parent_curve = p_doc["backtest"]["equity_curve_url".replace(".png", "_128x128.png")]
        dpt_curve = dpt_doc["backtest"]["equity_curve_url"].replace(".png", "_128x128.png")
        print(
            f"{dpt_s:>20} / {parent_s:15} {symbol:>4} {np_diff:12,}({np_perc:8.1%}) {pf_diff:12.4f}({pf_perc:6.1%}) {at_diff:8.2f}({at_perc:6.1%}) {dpt_curve}"
        )
        cmp_data["content"].append("<tr>")
        cmp_data["content"].append("  <td>")
        cmp_data["content"].append(f"    {dpt_doc['strategy_long_name']}")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("  <td align=center>")
        cmp_data["content"].append(
            f"    {p_doc['backtest']['metrics_all_trades']['net_profit']:,} / {dpt_doc['backtest']['metrics_all_trades']['net_profit']:,}<BR>"
        )
        cmp_data["content"].append(f"    {np_perc:.1%}")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("  <td align=center>")
        cmp_data["content"].append(
            f"    {p_doc['backtest']['metrics_all_trades']['profit_factor']:,.4} / {dpt_doc['backtest']['metrics_all_trades']['profit_factor']:,.4}<BR>"
        )
        cmp_data["content"].append(f"    {pf_perc:.1%}")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("  <td align=center>")
        cmp_data["content"].append(
            f"    {p_doc['backtest']['metrics_all_trades']['avg_trade']:,.2f} / {dpt_doc['backtest']['metrics_all_trades']['avg_trade']:,.2f}<BR>"
        )
        cmp_data["content"].append(f"    {at_perc:.1%}")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("  <td>")
        cmp_data["content"].append(f"<img src='{parent_curve}' alt='' border=3 height=100>")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("  <td>")
        cmp_data["content"].append(f"<img src='{dpt_curve}' alt='' border=3 height=100>")
        cmp_data["content"].append("  </td>")
        cmp_data["content"].append("</tr>")
    cmp_data["content"].append("</table>")

    print(f"averger NP perc change = {summ_np/cnt}")
    print(f"averger PF perc change = {summ_pf/cnt}")
    print(f"averger AT perc change = {summ_at/cnt}")

    write_static_page(cmp_data)
    #    cmp_data["equity_curve"] = equity_curve(dpt_doc)
    #    sheet_data["cross_markets"] = cross_markets(doc)
    #    sheet_data["mae"] = mae(doc)
    #    sheet_data["mfe"] = mfe(doc)
    # print(sheet_data)
    # pprint(cmp_data)
    # write_strategy_sheet(sheet_data)

    # config_mongo()
    # strat_doc = StrategyMdb.objects(strategy_name=strategy_name).first()
    # assets_dir = ""
    # collection_dir = ""
    # print(strat_doc.strategy_long_name)


if __name__ == "__main__":
    app()
