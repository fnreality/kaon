import kaon
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def page_root():
    return ctx.render(file= 'index.kaon.html')

@app.route('/update', methods= ['POST'])
def page_root_update():
    with ctx.complete(request.form) as concept:
        concept.merge([update_name])
    return ctx.render(file= 'index.kaon.html')

ctx = kaon.Context({
    'name': kaon.FileEntity('name.txt')
})

def update_name(ctx, req):
    return 'name', req['name']

if __name__ == '__main__':
    ctx.start_reality()
    app.run(port= 8080)
