Build 

```
python3 -m build
```

Local install

```
pip3 install -U dist/mdev-<x.y.z>-py3-none-any.whl --force-reinstall
```

Upload to pypi

```
twine upload dist/mdev-<x.y.z>-py3-none-any.whl
```
