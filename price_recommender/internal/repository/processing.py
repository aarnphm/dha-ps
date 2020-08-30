import json
import typing as t

import pandas as pd

from price_recommender.core import config
from price_recommender.core.logging import LogInfo
from price_recommender.internal.domains.common import get_columns
from price_recommender.internal.domains.products import ProductsRepository


def __get_product_name_and_table(df: pd.DataFrame, idx: int):
    product_table = df.loc[df[config.IDX_COLUMN] == idx]
    product_name = product_table["product_name"].unique()[0]
    return product_table, product_name


def __get_attr_name(table: pd.DataFrame, idx: int) -> pd.DataFrame:
    return table.loc[table["attribute_id"] == idx]["attribute_value_name"].unique()


def __get_product_description(table: pd.DataFrame, idx: int) -> str:
    product_table, formatted = __get_product_name_and_table(table, idx)
    sizes = __format_product_size(product_table)
    try:
        colours = __format_colour(product_table)
    except Exception:
        colours = ""

    _attr_idx = [i for i in product_table["attribute_id"].unique()]
    for i in _attr_idx:
        if i == config.SIZE_VAL:
            formatted += sizes
        elif i == config.COLOUR_VAL:
            formatted += colours
        else:
            for name in product_table.loc[product_table["attribute_id"] == i][
                "attribute_value_name"
            ]:
                formatted += f" {name}"
    return formatted


def __format_product_size(product_table: pd.DataFrame) -> str:
    product_table = __get_attr_name(product_table, config.SIZE_VAL)
    _idx = [config.SIZE.index(j) for j in product_table]
    sorted_size = [x for _, x in sorted(zip(_idx, product_table), key=lambda p: p[0])]
    formatted = ""
    if len(sorted_size) > 1:
        formatted = f" ({sorted_size[0]}-{sorted_size[-1]})"
    elif len(sorted_size) == 1:
        formatted = f" ({sorted_size[0]})"
    else:
        formatted = " "
    return formatted


def __format_colour(product_table: pd.DataFrame) -> str:
    product_table = __get_attr_name(product_table, config.COLOUR_VAL)
    return f" {len(product_table)} colours"


# Helpers function
def null_handler(data: list) -> list:
    """
    handles value types from sql.NullString
    `attribute_value_name` is type NullString, therefore contains (String, bool)
    """
    for prod in data:
        prod["attribute_value_name"] = (
            prod["attribute_value_name"]["String"]
            if prod["attribute_value_name"]["Valid"] == True
            else None
        )
    return data


# processing
def get_attr_idx(content: list, fpath: t.Optional[str] = None) -> t.List:
    if fpath is not None:
        content = json.load(open(fpath, "r"))
        content = [i["value"] for i in content]
        return [i if i is not None else str(i).replace("None", "*") for i in content]
    return [i if i != "nan" else str(i).replace("nan", "*") for i in content]


def convert_to_dataframe(
    content: t.List[t.Dict], fpath: t.Optional[str] = None
) -> pd.DataFrame:
    pcolumns = get_columns(ProductsRepository)
    content = null_handler(content)
    try:
        if fpath is not None:
            df = pd.read_csv(fpath, header=pcolumns)
        else:
            df = pd.DataFrame.from_dict(content)
    except ValueError as e:
        raise e
    # drop value that is null since it is useless anyway
    return df.dropna()


def sort_table(product: pd.DataFrame, order: list) -> pd.DataFrame:
    # order <-- __get_attr_idx
    product = product[product["attribute_id"].isin(order)]
    sorter = dict(zip(order, range(len(order))))
    product["attribute_id_rank"] = product["attribute_id"].map(sorter)
    product.sort_values(by=["attribute_id_rank"], inplace=True)
    product.drop(columns=["attribute_id_rank"], inplace=True)
    return product


def __prepare(
    body: t.List[t.Dict],
    csv_path: t.Optional[str] = None,
    ord_body: t.List[t.Dict] = None,
    orders_path: t.Optional[str] = None,
) -> t.List[t.Dict]:
    # do the sorting
    df = convert_to_dataframe(content=body, fpath=csv_path)
    attr_idx = get_attr_idx(content=ord_body, fpath=orders_path)
    sorted_df = sort_table(df, attr_idx)
    return sorted_df


def gen_corpus(**kwargs) -> t.Dict[str, int]:
    """Generate corpus from requests"""
    sorted_df = __prepare(
        body=kwargs.get("body"),
        csv_path=kwargs.get("csv_path"),
        ord_body=kwargs.get("ord_body"),
        orders_path=kwargs.get("orders_path"),
    )

    res = dict()
    for idx in sorted(list(sorted_df["product_id"].unique())):
        res[__get_product_description(sorted_df, int(idx))] = int(idx)
    return [{"description": k, "product_id": str(v)} for k, v in res.items()]
