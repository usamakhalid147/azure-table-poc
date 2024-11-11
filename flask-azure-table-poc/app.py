# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from azure.data.tables import TableServiceClient, UpdateMode
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key in production

# Retrieve the connection string from an environment variable
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")

table_name = "mytable"

# Create a TableServiceClient and TableClient
service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = service_client.get_table_client(table_name=table_name)

@app.route('/')
def list_entities():
    try:
        entities = table_client.list_entities()
        return render_template('list.html', entities=entities)
    except Exception as e:
        flash(f"An error occurred: {e}")
        return render_template('list.html', entities=[])

@app.route('/add', methods=['GET', 'POST'])
def add_entity():
    if request.method == 'POST':
        partition_key = request.form.get('partition_key')
        row_key = request.form.get('row_key')
        name = request.form.get('name')
        email = request.form.get('email')

        if not partition_key or not row_key:
            flash('Partition Key and Row Key are required.')
            return redirect(url_for('add_entity'))

        entity = {
            'PartitionKey': partition_key,
            'RowKey': row_key,
            'Name': name,
            'Email': email
        }

        try:
            table_client.create_entity(entity=entity)
            flash('Entity added successfully.')
            return redirect(url_for('list_entities'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('add_entity'))
    else:
        return render_template('add.html')

@app.route('/delete/<partition_key>/<row_key>', methods=['POST'])
def delete_entity(partition_key, row_key):
    try:
        table_client.delete_entity(partition_key=partition_key, row_key=row_key)
        flash('Entity deleted successfully.')
        return redirect(url_for('list_entities'))
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('list_entities'))

@app.route('/edit/<partition_key>/<row_key>', methods=['GET', 'POST'])
def edit_entity(partition_key, row_key):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        entity = {
            'PartitionKey': partition_key,
            'RowKey': row_key,
            'Name': name,
            'Email': email
        }

        try:
            table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
            flash('Entity updated successfully.')
            return redirect(url_for('list_entities'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('edit_entity', partition_key=partition_key, row_key=row_key))
    else:
        try:
            entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
            return render_template('edit.html', entity=entity)
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('list_entities'))

if __name__ == '__main__':
    app.run(debug=True)
