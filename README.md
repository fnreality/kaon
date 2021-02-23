# kaon
An asynchronous database that holds portals instead of data

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
