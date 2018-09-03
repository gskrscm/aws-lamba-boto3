import json
import boto3
import datetime

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
elb_client = boto3.client('elb')

ELB_ID = "nexus-nonprod"

def hello(event, context):

    # Get ec2 instance name from ELB
    # res = get_elb_instances(ELB_ID)
    # Check Health status 
    # Remove from elb
    # Add to elb
    
    res = ec2_list()
    return str(res)

def deregister_instance_elb(elb_id, instance_id):
    response = elb_client.deregister_instances_from_load_balancer(
    LoadBalancerName=elb_id,
    Instances=[
        {
            'InstanceId': instance_id
        }
    ]
    )
    return response

def register_instance_elb(elb_id, instance_id):
    response = elb_client.register_instances_with_load_balancer(
    LoadBalancerName=elb_id,
    Instances=[
        {
            'InstanceId': instance_id
        }
    ]
    )
    return response

def get_elb_instances(elb_id):
    '''To Get list of elb instances'''
    instance_id = []
    response = elb_client.describe_load_balancers(
        LoadBalancerNames=[
        elb_id
    ])
    for instance in response["LoadBalancerDescriptions"][0]["Instances"]:
        instance_id.append(instance["InstanceId"])
    return instance_id

def ec2_list():
    ecl = {}
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name':'tag-key', 
                'Values': ['nexus']
            }
        ]
    )
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
