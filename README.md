# kaon
A database you can put almost anything in, because its actually a portal. 

Simple Example:

```python
import kaon
ctx = kaon.Context({ 'file': kaon.FileCtx('example.txt') })
def hello_world(ctx):
    return 'file', 'Hello, world!'
ctx.start_reality()
with ctx.complete() as concept:
    concept.merge([hello_world])
```
