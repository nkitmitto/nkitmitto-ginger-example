import boto3
import json
import base64
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from botocore.exceptions import ClientError

app = Flask(__name__)

def get_database_secrets():
    secret_name = "prod/ginger-example/mysql"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            str_secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(str_secret)

secret = get_database_secrets()

app.config['MYSQL_HOST'] = secret['host']
app.config['MYSQL_USER'] = secret['username']
app.config['MYSQL_PASSWORD'] = secret['password']
app.config['MYSQL_DB'] = 'ginger'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
      details = request.form
      firstName = details['fname']
      print(f"INSERT INTO users(firstName) VALUES ({firstName})")
      cur = mysql.connection.cursor()
      cur.execute(f"INSERT INTO users(firstName) VALUES (\"{firstName}\")")
      results = cur.execute(f"SELECT * FROM users WHERE firstName = {firstName}")
      mysql.connection.commit()
      cur.close()
      return render_template('success.html', fname=firstName, results=results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()