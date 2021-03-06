import importlib
import inspect
import os
import glob


def import_plugins(plugins_package_directory_path, base_class=None, create_instance=True, filter_abstract=True):


    print("ATTEMPTING TO LOOK AT THINGS...")
    plugins_package_name = os.path.basename(plugins_package_directory_path)
    print(plugins_package_name)

    # -----------------------------
    # Iterate all python files within that directory
    plugin_file_paths = glob.glob(os.path.join(plugins_package_directory_path, "*.py"))
    for plugin_file_path in plugin_file_paths:
        print("Examining a file...: " + plugin_file_path)
        plugin_file_name = os.path.basename(plugin_file_path)

        module_name = os.path.splitext(plugin_file_name)[0]

        if module_name.startswith("__"):
            continue

        # -----------------------------
        # Import python file

        module = importlib.import_module("." + module_name, package=plugins_package_name)

        # -----------------------------
        # Iterate items inside imported python file

        for item in dir(module):
            value = getattr(module, item)
            if not value:
                continue

            if not inspect.isclass(value):
                continue

            if filter_abstract and inspect.isabstract(value):
                continue

            if base_class is not None:
                if type(value) != type(base_class):
                    continue

            # -----------------------------
            # Instantiate / return type (depends on create_instance)

            yield value() if create_instance else value