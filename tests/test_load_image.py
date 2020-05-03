from covidxpert.utils import load_image
from tqdm.auto import tqdm
from glob import glob


def test_load_image():
    for path in tqdm(glob("sample_dataset/*")):
        load_image(path)