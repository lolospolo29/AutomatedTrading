from abc import ABC, abstractmethod


class IDBService(ABC):
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def deleteByQuery(self):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def find(self):
        pass

    @abstractmethod
    def buildQuery(self):
        pass
