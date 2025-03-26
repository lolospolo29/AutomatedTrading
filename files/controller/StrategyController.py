from logging import Logger
from typing import Dict, Any

from files.models.strategy.StrategyDTO import StrategyDTO
from files.helper.manager.StrategyManager import StrategyManager


class StrategyController:

    # region Initializing
    def __init__(self, logger:Logger, strategy_manager:StrategyManager):
        self._StrategyManager = strategy_manager
        self._logger = logger
    # endregion

    def create_strategy(self, json_data:Dict[str,Any] = None):
        try:
            self._StrategyManager.create_strategy(StrategyDTO.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Add Asset failed,Error: {e}".format(e=e))

    def get_strategies(self):
        strategies = self._StrategyManager.get_strategies()
        dict_strategy = []
        for strategy in strategies:
            try:
                asset_dict: dict = strategy.dict(exclude={'_id'})
                dict_strategy.append(asset_dict)
            except Exception as e:
                self._logger.error(
                    "Error appending asset to list Name: {name},Error:{e}".format(name=strategy.name, e=e))
                continue
        return dict_strategy

    def get_entry_exit_strategies(self):
        strategies = self._StrategyManager.get_entry_exit_strategies()
        dict_strategy = []
        for strategy in strategies:
            try:
                asset_dict: dict = strategy.dict(exclude={'_id'})
                dict_strategy.append(asset_dict)
            except Exception as e:
                self._logger.error(
                    "Error appending asset to list Name: {name},Error:{e}".format(name=strategy._name, e=e))
                continue
        return dict_strategy

    def update_strategy(self,json_data:Dict[str,Any] = None):
        try:
            self._StrategyManager.update_strategy(StrategyDTO.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Add Asset failed,Error: {e}".format(e=e))

    def delete_strategy(self,json_data:Dict[str,Any] = None):
        try:
            self._StrategyManager.delete_strategy(StrategyDTO.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Add Asset failed,Error: {e}".format(e=e))