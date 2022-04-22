from aws_cdk import (
    Stack,
)
from constructs import Construct
import aws_cdk as cdk
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_appsync_alpha as appsync
from aws_lambda_powertools.event_handler import AppSyncResolver

#================================================
# Referenced links
#================================================
# Your first AWS CDK app:
#       https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html

# Building Scalable GraphQL APIs on AWS with CDK, TypeScript, AWS AppSync, Amazon DynamoDB, and AWS Lambda:
#       https://aws.amazon.com/blogs/mobile/building-scalable-graphql-apis-on-aws-with-cdk-and-aws-appsync/

# Working with the AWS CDK in Python:
#       https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html

# Migrating to AWS CDK v2:
#       https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html

# Translating TypeScript AWS CDK code to other languages:
#       https://docs.aws.amazon.com/cdk/v2/guide/multiple_languages.html

# Build a GraphQL API on AWS with CDK, Python, AppSync, and DynamoDB(Part 1):
#       https://aws.newbie.tips/rosius/build-a-graphql-api-on-aws-with-cdk-python-appsync-and-dynamodb-part-1-1pjl

# Lambda Powertools Python GraphQL API
#       https://awslabs.github.io/aws-lambda-powertools-python/latest/core/event_handler/appsync/#resolver-decorator

app = AppSyncResolver()

test_lambdas= [
    {
        "name": "test_appsync_resolver",
        "asset" : "lambda_fns",             # folder that contains lambda functions
        "fields": [
            ("Mutation", "createNote"),     # (type_name, field_name)
            ("Mutation", "updateNote"),
            ("Query", "listNotes"),
        ]
    }
]

class SetUpGraphqlApi(appsync.GraphqlApi):
    def __init__(self, scope, id: str, name: str, schema: appsync.Schema, authorization_config: appsync.AuthorizationConfig, xray_enabled: bool):
        super().__init__(scope, id, name=name, schema=schema, authorization_config=authorization_config, xray_enabled=xray_enabled)
    
    def create_lambdas(self, scope, lambda_list:list):
        for lambda_dict in lambda_list:
            #create lambda
            new_lambda = aws_lambda.Function(scope, lambda_dict["name"] + 'Handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                handler='main.app',
                code=aws_lambda.Code.from_asset(lambda_dict["asset"]),
                memory_size=1024
                )
        
            # create datasource 
            lambda_ds = self.add_lambda_data_source(lambda_dict["name"] + 'dataSource', new_lambda)

            # create resolvers
            for field in lambda_dict["fields"]:
                lambda_ds.create_resolver(
                    type_name= field[0],
                    field_name= field[1]
                )


class AppsyncAppStack(Stack):

    def __init__(self, scope= Construct, construct_id= str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = SetUpGraphqlApi(
            self,
            "Api",
            name="cdk-notes-appsync-api",
            schema=appsync.Schema.from_asset("graphql/schema.graphql"),
            authorization_config=appsync.AuthorizationConfig(
                default_authorization=appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.API_KEY,
                    api_key_config=appsync.ApiKeyConfig(expires=cdk.Expiration.after(cdk.Duration.days(365)))
                )
            ),
            xray_enabled=True
        )

        cdk.CfnOutput(self, "GraphQLAPIURL", value=api.graphql_url)        
        cdk.CfnOutput(self, "GRAPHQLAPIKey", value=(api.api_key or ''))
        cdk.CfnOutput(self, "Stack Region", value=self.region)

        api.create_lambdas(self, test_lambdas)
