import os
import importlib.util
from typing import Any, TypedDict
from .enums.WrapperTypes import WrapperTypes
from .base.Target import BaseTarget
from .base.Source import BaseSource
from storage.storages import WrapperControllerStorage


class Wrappers(TypedDict):
    source: list[str]
    target: list[str]


class WrapperController:
    def __init__(self, wcs: WrapperControllerStorage):
        self.__wcs = wcs
        self.__ignored_names = ["__init__.py"]
        self.__wrapper_dir = "wrappers"
        self.__wrappers_target = {}
        self.__wrappers_source = {}
        self.__load_wrappers()

    def __load_wrappers(self) -> None:
        wrapper_dir_current = os.path.join(self.__wrapper_dir, "source")
        for wrapper_name in os.listdir(wrapper_dir_current):
            if wrapper_name in self.__ignored_names:
                continue
            wrapper_obj = self.__get_wrapper_object(os.path.join(wrapper_dir_current, wrapper_name, f"{wrapper_name}.py"), wrapper_name)
            self.__wcs.register_wrapper(wrapper_obj.wrapper_name, WrapperTypes.Source)
            self.__wrappers_source |= {wrapper_obj.wrapper_name: wrapper_obj}

        wrapper_dir_current = os.path.join(self.__wrapper_dir, "target")
        for wrapper_name in os.listdir(wrapper_dir_current):
            if wrapper_name in self.__ignored_names:
                continue
            wrapper_obj = self.__get_wrapper_object(
                os.path.join(
                    wrapper_dir_current,
                    wrapper_name,
                    f"{wrapper_name}.py"
                ), wrapper_name)
            self.__wcs.register_wrapper(wrapper_obj.wrapper_name, WrapperTypes.Target)
            self.__wrappers_target |= {wrapper_obj.wrapper_name: wrapper_obj}

        self.__wcs.set_delete_wrapper_not_from_list(
            [{"name": i, "type": WrapperTypes.Target} for i in self.__wrappers_target] +
            [{"name": i, "type": WrapperTypes.Source} for i in self.__wrappers_source]
        )

    def get_wrapper_name_list(self) -> Wrappers:
        return {
            "source": [i for i in self.__wrappers_source],
            "target": [i for i in self.__wrappers_target]
        }

    def get_wrapper(self, wrapper_name: str, wrapper_type: WrapperTypes) -> BaseTarget | BaseSource | None:
        if wrapper_type == WrapperTypes.Target and wrapper_name in self.__wrappers_target:
            return self.__wrappers_target[wrapper_name]
        elif wrapper_type == WrapperTypes.Source and wrapper_name in self.__wrappers_source:
            return self.__wrappers_source[wrapper_name]
        return None

    def get_required_config(self, wrapper_name: str, wrapper_type: WrapperTypes) -> dict[str: str | None]:
        return self.get_wrapper(wrapper_name, wrapper_type).required_configs

    def check_required_config(self, wrapper_name: str, wrapper_type: WrapperTypes) -> bool:
        loaded_config = self.__wcs.get_all_config(wrapper_name, wrapper_type)
        loaded_config_keys = [i[0] for i in loaded_config]
        required_config = self.get_required_config(wrapper_name, wrapper_type)

        if required_config is None:
            return True

        for key, value in required_config.items():
            if key not in loaded_config_keys and value is None:
                return False

        return True

    def get_unloaded_config(self, wrapper_name: str, wrapper_type: WrapperTypes) -> list[str]:
        unloaded_config_keys = []

        if self.check_required_config(wrapper_name, wrapper_type):
            return unloaded_config_keys

        loaded_config = self.__wcs.get_all_config(wrapper_name, wrapper_type)
        loaded_config_keys = [i[0] for i in loaded_config]
        required_config = self.get_required_config(wrapper_name, wrapper_type)

        for key, value in required_config.items():
            if key not in loaded_config_keys and value is None:
                unloaded_config_keys.append(key)

        return unloaded_config_keys

    def update_wrapper(self):
        self.__wrappers_target = {}
        self.__wrappers_source = {}
        self.__load_wrappers()

    @staticmethod
    def __get_wrapper_object(wrapper_path: str, wrapper_name: str) -> Any:
        spec = importlib.util.spec_from_file_location(wrapper_name, wrapper_path)
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        return getattr(plugin_module, wrapper_name)
