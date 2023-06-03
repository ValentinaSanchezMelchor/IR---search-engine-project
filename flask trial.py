from flask import Flask, request, render_template_string

app = Flask(__name__)

TABLE_TEMPLATE = """
<style>
   table, th, td {
   border: 1px solid black;
   }
</style>
<table style="width: 100%">
   <thead>
      <th>Client</th>
      <th>IP</th>
      <th>Status</th>
   </thead>
   <tbody>
      {% for row in data %}
      <tr>
         <td>{{ row.client }}</td>
         <td>{{ row.ip }}</td>
         <td>{{ row.status }}</td>
      </tr>
      {% endfor %}
   </tbody>
</table>
"""


@app.route("/device_add", methods=['POST'])
def device_add():
    name = request.args.get('name')
    with open('logs.log', 'a') as f:
        f.write(f'{name} Connected USB from IP: {request.remote_addr}\n')
    return 'ok'


@app.route("/device_remove", methods=['POST'])
def device_remove():
    name = request.args.get('name')
    with open('logs.log', 'a') as f:
        f.write(f'{name} Disconnected USB from IP: {request.remote_addr}\n')

    return 'ok'


@app.route("/", methods=['GET'])
def device_list():
    keys = ['client', 'ip', 'status']
    data = []
    with open('logs.log', 'r') as f:
        for line in f:
            row = line.split()
            data.append(dict(zip(keys, [row[0], row[-1], row[1]])))

    return render_template_string(TABLE_TEMPLATE,
                                  data=data)