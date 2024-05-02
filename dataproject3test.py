#!/usr/bin/python3

import boto3
import os 
import logging

sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/440848399208/jmh8fr'

messages_data = {}
receipt_handles = []

def delete_messages(receipt_handles):
    for receipt_handle in receipt_handles:
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print(f"Deleted message with ReceiptHandle: {receipt_handle}")

def assemble_phrase(messages_data):
    sorted_keys = sorted(messages_data.keys(), key=int)
    phrase = ' '.join(messages_data[key] for key in sorted_keys)
    return phrase

def retrieve_and_process_messages():
    

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10  
        )
        
        if 'Messages' not in response:
            break  

        for message in response['Messages']:
            order = message['MessageAttributes']['order']['StringValue']
            word = message['MessageAttributes']['word']['StringValue']
            receipt_handle = message['ReceiptHandle']
            messages_data[order] = word
            receipt_handles.append(receipt_handle)
            print(f"Retrieved message - Order: {order}, Word: {word}")

    return messages_data, receipt_handles


def print_messages_data(messages_data):
    print("Fetching values from dictionary:")
    for order in sorted(messages_data, key=int): 
        word = messages_data[order]
        print(f"Order {order}: Word {word}")

def main():
    messages_data, receipt_handles = retrieve_and_process_messages()

    if messages_data:
        phrase = assemble_phrase(messages_data)
        print(f"Phrase assembled: {phrase}")
    else:
        print("No messages retrieved.")

    delete_messages(receipt_handles)

if __name__ == '__main__':
    main()
