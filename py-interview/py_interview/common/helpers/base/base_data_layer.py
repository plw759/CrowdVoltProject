import abc
from typing import Union, List, Optional, Dict, Any, TypeVar, Tuple

from py_interview.common.helpers.base.base import Base

T = TypeVar('T', bound=Base)


class BaseDataLayer(abc.ABC):

    @abc.abstractmethod
    def create(self, obj: Union[T, List[T]]) -> Union[T, List[T]]:
        """
        Saves

        """

    @abc.abstractmethod
    def get(self, uqid: str = None, **kwargs) -> Optional[T]:
        """

        """

    @abc.abstractmethod
    def list(self, uqid: str | List[str] = None, offset: int = 0, limit: int = None, **kwargs) -> List[T]:
        """

        """

    @abc.abstractmethod
    def update(self, uqid: str, attr: Dict[str, Any], user: str = 'unknown') -> Optional[T]:
        """

        """

    @abc.abstractmethod
    def delete(self, uqid: str) -> Optional[T]:
        """

        """
