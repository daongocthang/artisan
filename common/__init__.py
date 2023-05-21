import pkgutil
from subprocess import check_call


def require(module, pkg):
    if not pkgutil.find_loader(module):
        check_call(["python", "-m", "pip", "install", "-U", "pip"], shell=True)
        check_call(["pip", "install", pkg], shell=True)

    return __import__(module, globals=(), locals=())
