from abc import ABC, abstractmethod


class BaseRatingTracker(ABC):

    @abstractmethod
    def update(self, match):
        """
        Обновить состояние после матча.
        """
        raise NotImplementedError

    @abstractmethod
    def get_team(self, team):
        """
        Вернуть рейтинг команды.
        """
        raise NotImplementedError

    @abstractmethod
    def has_team(self, team):
        """
        Есть ли достаточно информации о команде.
        """
        raise NotImplementedError