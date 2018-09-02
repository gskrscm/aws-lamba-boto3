import json
import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def hello(event, context):
    ecl = {}
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            ecid = instance["InstanceId"]
            tagl = get_instance_tags(ecid)
            ecl.update({ecid:tagl})
    return ecl

def get_instance_tags(ecid):
    '''Get ec2 instance tags as list'''
    ec2instance = ec2_resource.Instance(ecid)
    tagl = ec2instance.tags
    return tagl
