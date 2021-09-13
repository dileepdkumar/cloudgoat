import boto3
from sqlite_utils import Database

db = Database("my_database.db")
iam_client = boto3.client('iam')

# db["policies"].insert_all([
#     {"policy_name": "AmazonSNSReadOnlyAccess", "public": 'True'}, 
#     {"policy_name": "AmazonRDSReadOnlyAccess", "public": 'True'},
#     {"policy_name": "AWSLambda_ReadOnlyAccess", "public": 'True'},
#     {"policy_name": "AmazonS3ReadOnlyAccess", "public": 'True'},
#     {"policy_name": "AmazonGlacierReadOnlyAccess", "public": 'True'},
#     {"policy_name": "AmazonRoute53DomainsReadOnlyAccess", "public": 'True'},
#     {"policy_name": "AdministratorAccess", "public": 'False'}
# ])


def handler(event, context): 
    target_policys = event['policy_names']
    user_name = event['user_name']
    print(f"username is : {user_name}")
    print(f"target policys are : {target_policys}")

    for policy in target_policys:
        statement = f"select policy_name from policies where policy_name='{policy}' and public='True'"
        for row in db.query(statement):
            print(f"applying {row['policy_name']} to {user_name}")
            
            response = iam_client.attach_user_policy(
                UserName= user_name,
                PolicyArn=f"arn:aws:iam::aws:policy/{row['policy_name']}"
                )
            print(response)
            

    return "All managed policies were applied as expected."
    
    
if __name__ == "__main__":
    payload = {
        "policy_names": [
            "AmazonSNSReadOnlyAccess",
            "AdministratorAccess"
        ],
        "user_name": "cg-bilbo-lambda_injection_privesc_cgid2nnywbtb4n"
        }
    print(handler(payload,'uselessinfo'))