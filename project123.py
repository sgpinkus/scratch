import fsspec
import json

with open('./project123.json', 'r') as f:
    fo = json.load(f)

fs = fsspec.filesystem(
    "reference",
    fo=fo,
    simple_templates=False,
    fs={
      "https": {
        "client_kwargs": {"headers": {"Accept-Encoding": "identity"}},
      },
    }
)

with fs.open("test", "r") as f:
    print(len(f.read()))
with fs.open("train", "r") as f:
    print(len(f.read()))