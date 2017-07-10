import inspect
from confobo.config import SEPARATOR


class Command:
    def __init__(self, handler, command_text: str, desc: str = None):
        self.handler = handler
        self.command_text = command_text
        self.desc = desc
        sig = inspect.signature(handler)
        self.max_args = len(sig.parameters)
        self.min_args = len([p for p in sig.parameters.values() if p.default is inspect._empty])
        self.args = list(sig.parameters.keys())
        self._needs_user_data = False

    @property
    def info(self):
        sep = SEPARATOR
        if sep != ' ':
            sep += ' '
        args = ' [{}]'.format(sep.join(self.args)) if self.args else ''
        return '{cmd}{args}: {desc}'.format(cmd=self.command_text, args=args, desc=self.desc)

    @property
    def needs_user_data(self):
        return self._needs_user_data

    @needs_user_data.setter
    def needs_user_data(self, value: bool):
        if not value:
            raise NotImplemented()
        if 'user_data' not in self.args:
            raise TypeError('{}() must take a parameter named \'user_data\''.format(self.handler.__name__))
        self.max_args -= 1
        self.min_args -= 1
        self.args.remove('user_data')
        self._needs_user_data = True

    def __str__(self):
        return '<Command \'{}\'>'.format(self.command_text)

    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)
