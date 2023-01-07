# Library to make HTTP requests to eBay's API
import requests 

# Library to send mails through SMTP
import smtplib

# Library for working wiht JSON data
import json

# LIbrary for encoding and decoding dta in Base64
import base64

# Library that privides task scheduler for executing tasks at specified intervals or on a specific date/time
from apscheduler.schedulers.blocking import BlockingScheduler

# Set the API endpoint URL 
endpoint_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# Set the request headers
headers = {
    "Authorization": "Bearer YOUR_API_KEY", # eBay account pending approval, insert API_KEY once account is approved
    "Content-Type": "application/json",
}

params = {
    "q": "product name", # Replace with our product name (implement a dictionary with product name "key": ideal price "value" pair)
    "limit": "1" # Set the maximum number of results to return (I will start with with a number like 10 and increase it gradually and see if the scipts performance is affected)
}

# Send the HTTP request
response = requests.get(endpoint_url, headers=headers, params=params)

# Check the response status code
if response.status_code == 200:
    # If the request is successful, parse the response JSON
    response_json = response.json()
    
    # Extract the item data from the response
    items = response_json["itemSummaries"]

else:
    # If the request is not successful, print an error message
    print("An error occured:", response.status_code)

# Extract the first item in the list (since we set the limit to 1 in this case)
item = items[0]

# Extract the item's price and title
price = item["price"]["value"]
title = item["title"]

# Set the threshold price
threshold_price = 100 # Replace with desired threshold price

# Check if the price is below or equal to the threshold_price
if price <= threshold_price:
    # Set the SMTP server and port
    smtp_server = "smtp.gmail.com" # Replace with your SMTP server
    smtp_port = 587 # Replace with your SMTP port

    # Set the email address and password for the sender
    sender_email = "brandonmunda1@gmail.com" # Replace with your email address
    sender_password = "TwoGreen1," # Replace with your email password

    # Set the email address for the recipient
    recipient_email = "mundabrandon@outlook.com" # Replace with recipient's email address

    # Set the subject and body of the email
    subject = "eBay Price Alert"
    body = f"The price of {title} on eBay is now ${price}. It is at/below your threshold of ${threshold_price}."

    # Create the email message
    message= f"Subject: {subject}\n\n{body}"

    # Create an SMTP client
    client = smtplib.SMTP(smtp_server, smtp_port)

    # Start the TLS encryption for the connection
    client.starttls()

    # Log in to the SMTP server
    client.login(sender_email, sender_password)

    # Send the email
    client.sendmail(sender_email, recipient_email, message)

    # Disconnect from the SMTP server
    client.quit()

# Create a scheduler
scheduler = BlockingScheduler()

# Define the function that will be run as a job
def check_price ():
    # Replace with code from above lines such that to check the prices of multiple products we can simple call the function with appropriate arguments
    return "check_price function empty for now"

# Schedule the job to run every hour
scheduler.add_job(check_price, "interval", hours=1)

# Start the scheduler
scheduler.start()