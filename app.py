from flask import Flask, request, jsonify
from selenium import webdriver
import boto3

app = Flask(__name__)

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TaskAutomationTable')

# Selenium Function for Task Automation
def automate_task(url):
    # Initialize Selenium WebDriver (You might need to adjust the path to your browser driver)
    driver = webdriver.Chrome(executable_path='path/to/chromedriver')
    driver.get(url)

    # Implement your Selenium automation logic here
    # For example: fill out forms, click buttons, extract data
    try:
        # Find form elements and fill them out
        name_field = driver.find_element_by_id('name')  # Assuming the input field has id='name'
        email_field = driver.find_element_by_id('email')  # Assuming the input field has id='email'

        # Fill out the form
        name_field.send_keys('John Doe')
        email_field.send_keys('johndoe@example.com')

        # Submit the form
        name_field.send_keys(Keys.RETURN)  # Pressing Enter in the last input field can simulate form submission

        # Wait for a few seconds to ensure the form is submitted successfully (you might need to adjust the time)
        driver.implicitly_wait(5)

        # You can perform additional actions after the form submission if needed

        print("Form submitted successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()    

# Flask Route for Task Submission
@app.route('/submit-task', methods=['POST'])
def submit_task():
    data = request.get_json()
    task_name = data.get('taskName')
    task_url = data.get('taskURL')

    # Automate the task using Selenium
    automate_task(task_url)

    # Store task data in DynamoDB
    table.put_item(Item={'TaskName': task_name, 'TaskURL': task_url})

    return jsonify({'message': 'Task submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
