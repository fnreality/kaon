from abc import ABC, abstractmethod
from collections import deque, Mapping
import multiprocessing
import threading

class Context(Mapping):
    def __init__(self, access):
        super(Context, self).__init__()
        self.access = access
        self.pushed = deque([])

    def poll(self):
        while len(self.pushed) != 0:
            curr = self.pushed.popleft()
            for k, v in curr.items():
                self[k] = v

    def start_reality(self):
        ContextRealityThread(self).start()

    def complete(self, *args, **kwargs):
        return Concept(self, args, kwargs)

    def render(self, file= None, html= None):
        assert (file == None) or (html == None)
        if file != None:
            with open(file, 'r') as f:
                html = f.read()
            return self.render_html(html)
        elif html != None:
            return self.render_html(html)
        else:
            assert False

    def render_html(self, html):
        [head, *tail] = html.split('#[')
        split_tail = map(
            lambda x: x.split(']#'),
            tail
        )
        reassembled_tail = ''.join(
            list(map(
                lambda x: self[x[0]] + x[1],
                split_tail
            ))
        )
        return head + reassembled_tail

    def __getitem__(self, key):
        return self.access[key].get()

    def __setitem__(self, key, val):
        self.access[key].set(val)

    def __iter__(self):
        return context_iterator(self)

    def __len__(self):
        return len(self.access)

class Concept(object):
    def __init__(self, ctx, args, kwargs):
        super(Concept, self).__init__()
        self.ctx = ctx
        self.args = args
        self.kwargs = kwargs

    def merge(self, instants):
        with multiprocessing.Pool() as pool:
            instant_dict = dict(list(pool.map(
                self.process_instant,
                instants
            )))
        self.ctx.pushed.append(instant_dict)

    def process_instant(self, instant):
        return instant(self.ctx, *self.args, **self.kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *_args, **_kwargs):
        pass

class ContextRealityThread(threading.Thread):
    def __init__(self, ioc_context):
        super(ContextRealityThread, self).__init__()
        self.ctx = ioc_context

    def run(self):
        while True:
            self.ctx.poll()

def context_iterator(ctx):
    for _, i in ctx.access.items():
        yield i.get()

class AbstractCtx(ABC):
    @abstractmethod
    def __init__(self, given_value):
        raise NotImplementedError
        return NotImplemented

    @abstractmethod
    def get(self):
        raise NotImplementedError
        return NotImplemented

    @abstractmethod
    def set(self, value):
        raise NotImplementedError
        return NotImplemented

    def __eq__(self, other):
        classname = lambda x: type(x).__class__.__name__
        return (
            other.__hash__() == self.__hash__()
        ) and classname(self) == classname(other)

    def __hash__(self):
        return self.given_value.__hash__()

class FileCtx(AbstractCtx):
    def __init__(self, given_value):
        self.filename = given_value

    def get(self):
        with open(self.filename, 'r') as f:
            contents = f.read()
        return contents

    def set(self, value):
        with open(self.filename, 'w') as f:
            f.write(value)

def identity(x):
    return x
