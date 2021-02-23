# kaon
An asynchronous database that holds portals instead of data. (Technically, an STM for coordinated but asynchronous abstract state managment)

Simple Example:

```python
import kaon
ctx = kaon.Context({ 'file': kaon.FileEntity('example.txt') })

def hello_world(ctx):
    return 'file', 'Hello, world!'

ctx.start_reality()

with ctx.complete() as concept:
    concept.merge([hello_world])
```
