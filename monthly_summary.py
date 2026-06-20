import boto3
from datetime import datetime, timedelta
 
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('Expenses')
 
today = datetime.now()
month_start = today.replace(day=1)
 
response = table.scan()
total = sum(
    float(item['amount']) for item in response['Items']
    if datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S') >= month_start
)
 
sns.publish(
    TopicArn='arn:aws:sns:region:account-id:monthly-expense-summary',
    Subject='Monthly Expense Summary',
    Message=f'Total expenses this month: ₹{total}'
)
