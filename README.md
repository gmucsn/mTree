# mTree

A Python library for experimental and computational economics.


## Documentation

mTree's basic documentation is available inside the docs folder. [View Documentation](./docs/README.md)

mTree uses pdoc to help document its codebase.


## Developer Documentation

mTree makes use of pdoc to document the code inside this repository. Assuming you have mTree installed you should be able to type `pdoc mTree` and the pdoc webserver will start and be available at http://localhost:8080

Killing unnecessary processes: kill $(ps aux | grep 'cto' | awk '{print $2}')

## Basic Installation

mTree can be installed using the `pip` installer.

```
pip3 install mTree
```

Once installed, mTree is imported in the standard fashion.

```python
import mTree
```

## UV Commands

uv version --bump patch --bump beta
uv run ...
uv pip install -e .