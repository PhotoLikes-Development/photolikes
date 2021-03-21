import os
import sys

import tensorflow as tf
from tensorflow.keras.models import Model

from common.utils.cached_object import CachedObject
from config import Config
from model.model_loader import ModelLoader


class FilesystemModelLoader(ModelLoader):
    class CachedModel(CachedObject[Model]):
        _model_path = Config.MODEL_DIR
        _last_modified_time: float = None

        def load(self) -> Model:
            model = tf.keras.models.load_model(self._model_path)
            self._last_modified_time = os.path.getmtime(self._model_path)
            return model

        def is_reload_needed(self) -> bool:
            return abs(self._last_modified_time - os.path.getmtime(self._model_path)) > sys.float_info.epsilon

    _cached_model = CachedModel()

    def get_instance(self) -> Model:
        return self._cached_model.instance

    def tensorflow_warmup(self):
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')
        for device in gpu_devices:
            tf.config.experimental.set_memory_growth(device, True)

        self._cached_model.load()
