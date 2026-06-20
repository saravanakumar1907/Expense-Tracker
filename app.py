from flask import Flask, request, render_template
import boto3
from datetime import datetime
from decimal import Decimal
import uuid
import logging
app = Flask(__name__)
# Configure Logging
logging.basicConfig(
    filename='/var/log/expense.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Expenses')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item = {
            'id': str(uuid.uuid4()),
            'category': request.form['category'],
            'amount': Decimal(request.form['amount']),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        table.put_item(Item=item)
        # Log expense submission
        logging.info(
            f"Expense added: {item['category']} - ₹{item['amount']} - ID: {item['id']}"
        )
        return "Expense recorded!"
    return render_template('form.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
