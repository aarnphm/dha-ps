import datetime
import typing as t

from pydantic.main import BaseConfig, BaseModel


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        w if idx == 0 else w.capitalize() for idx, w in enumerate(string.split("_"))
    )


# returns key or in this case columns given value
def get_columns(repo: BaseModel) -> t.List[str]:
    return list(repo.__field_defaults__.keys())


class Repository(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        alias_generator = convert_field_to_camel_case
