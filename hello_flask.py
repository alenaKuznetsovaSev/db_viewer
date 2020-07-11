from flask import Flask, render_template, request
from saver import Saver

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def select_table() -> 'str':
    saver = Saver('vsearchlogDB')
    tables = saver.get_tables()
    return render_template('select_table.html', title='select_table', tables=tables)


@app.route('/view_table', methods=['POST'])
def view_table() -> 'str':
    table = request.form['table']
    saver = Saver('vsearchlogDB')
    the_data = saver.get_table(table)
    table_headers = saver.get_table_header(table)
    print(table_headers)
    # breakpoint()
    # print(type(res), "\n\n\n")
    return render_template('view_table.html', title=table, table_headers=table_headers,
                           the_data=the_data)


app.run()
