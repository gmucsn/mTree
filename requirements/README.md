uv pip compile requirements/requirements.in -o requirements/requirements.txt

uv pip install -r requirements/requirements.txt

uv add -r requirements/base.in -c requirements/base.txt