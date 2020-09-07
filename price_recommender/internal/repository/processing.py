import typing as t

import pandas as pd
from loguru import logger as log

from price_recommender.core import config
from price_recommender.internal.domains.common import get_columns
from price_recommender.internal.domains.products import ProductsRepository


def null_handler(data: list) -> list:
    """
    handles value types from sql.NullString
    `attribute_value_name` is type NullString, therefore contains (String, bool)
    """
    return [
        prod["attribute_value_name"]["String"]
        for prod in data
        if prod["attribute_value_name"]["Valid"]
    ]


def get_attr_name(table: pd.DataFrame, idx: int) -> t.List:
    return table.loc[table["attribute_id"] == idx]["attribute_value_name"].unique()


def get_attr_idx(content: t.List[t.Dict]) -> t.List:
    return [i if i != "nan" else str(i).replace("nan", "*") for i in content]


def get_product_description(table: pd.DataFrame, idx: int) -> str:
    def get_product_name_and_table(df: pd.DataFrame, idx: int):
        product_table = df.loc[df[config.IDX_COLUMN] == idx]
        product_name = product_table["product_name"].unique()[0]
        return product_table, product_name

    def format_product_size(product_table: pd.DataFrame) -> str:
        attribute_list = get_attr_name(product_table, config.SIZE_VAL)
        _idx = [config.SIZE.index(j) for j in attribute_list]
        sorted_size = [
            x for _, x in sorted(zip(_idx, attribute_list), key=lambda p: p[0])
        ]
        formatted = ""
        if len(sorted_size) > 1:
            formatted = f" ({sorted_size[0]}-{sorted_size[-1]})"
        elif len(sorted_size) == 1:
            formatted = f" ({sorted_size[0]})"
        return formatted

    def format_colour(product_table: pd.DataFrame) -> str:
        attribute_list = get_attr_name(product_table, config.COLOUR_VAL)
        return f" {len(attribute_list)} colours"

    product_table, formatted = get_product_name_and_table(table, idx)
    sizes = format_product_size(product_table)
    try:
        colors = format_colour(product_table)
    except Exception:
        colors = ""

    _attr_idx = product_table["attribute_id"].unique()
    for i in _attr_idx:
        if i == config.SIZE_VAL:
            formatted += sizes
        elif i == config.COLOUR_VAL:
            formatted += colors
        else:
            for name in product_table.loc[product_table["attribute_id"] == i][
                "attribute_value_name"
            ]:
                formatted += f" {name}"
    return formatted


def convert_to_dataframe(content: t.List[t.Dict], order: list) -> pd.DataFrame:
    # drop value that is null since it is useless anyway
    df = pd.DataFrame.from_records(
        null_handler(content), columns=get_columns(ProductsRepository)
    ).dropna()
    df = df[df["attribute_id"].isin(order)]
    sorter = dict(zip(order, range(len(order))))
    df["attribute_id_rank"] = df["attribute_id"].map(sorter)
    df.sort_values(by=["attribute_id_rank"], inplace=True)
    df.drop(columns=["attribute_id_rank"], inplace=True)
    return df


def prepare(body: t.List[t.Dict], ord_body: t.List[t.Dict] = None) -> t.List[t.Dict]:
    # do the sorting
    attr_idx = get_attr_idx(content=ord_body)
    df = convert_to_dataframe(content=body, order=attr_idx)
    log.debug(attr_idx)
    return df


def gen_corpus(**kwargs) -> t.Dict[str, int]:
    """Generate corpus from requests"""
    sorted_df = prepare(body=kwargs.get("body"), ord_body=kwargs.get("ord_body"))
    res = {}
    for idx in sorted(list(sorted_df["product_id"].unique())):
        res[get_product_description(sorted_df, int(idx))] = int(idx)
    return [{"description": k, "product_id": str(v)} for k, v in res.items()]
