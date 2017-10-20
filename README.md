# mTree

Running the set up:

Go to the directory and enter the following:

If you are using macOS:
```commandline
python3.6 setup.py bdist_egg
```

For Windows:
```commandline
python setup.py bdist_egg
```

After building this you will need to install locally:

```commandline
easy_install dist/mTree-x-py3.6.egg
```


To test this, open python3 in either Terminal or Command Prompt, and try importing mTree with:

```python
import mTree
```

If there are no error messages, the build was successful.
You can now access mTree as you would any other python package.
