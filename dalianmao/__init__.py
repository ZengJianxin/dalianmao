from concurrent.futures import ProcessPoolExecutor as Executor

from dalianmao.app import DaLianMao
from dalianmao.options import Options

__version__ = '0.06dev'
__all__ = [Executor, DaLianMao, Options]
