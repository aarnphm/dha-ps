"""helpers for net.py"""
import os
import shutil
from zipfile import ZipFile

import requests
import torch
from loguru import logger as log
from torch import Tensor
from tqdm import tqdm

MODELS = "distilbert-base-nli-stsb-mean-tokens"
DOWNLOAD_URL = (
    "https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/"
)


def get_default_cache_path(model_name_or_path: str = MODELS):
    try:
        from torch.hub import _get_torch_home

        torch_cache_home = _get_torch_home()
    except ImportError:
        torch_cache_home = os.path.expanduser(
            os.getenv(
                "TORCH_HOME",
                os.path.join(os.getenv("XDG_CACHE_HOME", "~/.cache"), "torch"),
            )
        )
    default_model_path = os.path.join(torch_cache_home, MODELS)

    if not os.path.exists(model_name_or_path) or not os.path.exists(default_model_path):
        log.info("Downloading model from server...")
        model_url = DOWNLOAD_URL + model_name_or_path + ".zip"

        model_path = default_model_path
        os.makedirs(model_path, exist_ok=True)
        log.info(
            "Downloading sentence transformer model from {} and saving it at {}".format(
                model_url, model_path
            )
        )
        try:
            zip_save_path = os.path.join(model_path, "model.zip")
            http_get(model_url, zip_save_path)
            with ZipFile(zip_save_path, "r") as zipFile:
                zipFile.extractall(model_path)
                os.remove(zip_save_path)
        except Exception as e:
            shutil.rmtree(model_path)
            raise e
    else:
        log.info("Model is already downloaded, continue...")
        model_path = default_model_path
    return model_path


def pytorch_cdist(a: Tensor, b: Tensor) -> Tensor:
    """
    Compute cosine similarity (a[i], b[j]) for all i,j
    faster replacement for `1 - scipy.spatial.distance.cdist(a,b)`

    :param a,b: input tensor
    :return: tensor[i][j] = cos_sim(a[i],b[j])
    """
    if len(a.shape) == 1:
        a = a.unsqueeze(0)
    if len(b.shape) == 1:
        b = b.unsqueeze(0)
    a_norm = a / a.norm(dim=1)[:, None]
    b_norm = b / b.norm(dim=1)[:, None]
    return torch.mm(a_norm, b_norm.transpose(0, 1))


def http_get(url: str, path: str):
    """Download given path"""
    req = requests.get(url, stream=True)
    if req.status_code != 200:
        log.info(
            "Exeception when downloading {}. Response: {}".format(url, req.status_code)
        )
        req.raise_for_status()
        return
    download_path = path + "_part"
    with open(download_path, "wb") as fb:
        content_length = req.headers.get("Content-Length")
        total = int(content_length) if content_length is not None else None
        progress = tqdm(unit="B", total=total, unit_scale=True)
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                progress.update(len(chunk))
                fb.write(chunk)

    os.rename(download_path, path)
    progress.close()


def import_from_string(mpath: str, API=False):
    """
    import a module path from config file and return the attribute/class designated by the last name of the path
    raises ImportError if import failed.
    """
    try:
        import importlib

        # import from `models`
        module_path, class_name = mpath.split(".")[1:]
        if API:
            parent = ".".join(
                os.path.dirname(os.path.abspath(__file__)).split("/")[-2:]
            )
            module_path = f"{parent}.{module_path}"
        module = importlib.import_module(module_path)
    except ValueError:
        raise ImportError(f"{mpath} doesn't look like a module path")

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            f"Module `{module_path}` doesn't define a `{class_name}` attribute/class"
        )
