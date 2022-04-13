from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as cdk
import aws_cdk.aws_dynamodb as ddb
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_appsync_alpha as appsync

class AppsyncAppStack(Stack):

    def __init__(self, scope= Construct, construct_id= str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = appsync.GraphqlApi(
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
        
        notes_lambda = aws_lambda.Function(self, 'AppSyncNotesHandler',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler='main.lambda_handler',
            code=aws_lambda.Code.from_asset('lambda_fns'),
            memory_size=1024
            )

        # Set the new Lambda function as a data source for the AppSync API
        lambda_ds = api.add_lambda_data_source('lambdaDatasource', notes_lambda)

        # lambda_ds.create_resolver(
        #     type_name="Query",
        #     field_name="getNoteById"
        #     )

        # lambda_ds.create_resolver(
        #     type_name="Query",
        #     field_name="listNotes"
        # )

        lambda_ds.create_resolver(
            type_name= "Mutation",
            field_name= "createNote"
        )

        # lambda_ds.create_resolver(
        #     type_name= "Mutation",
        #     field_name= "deleteNote"
        # )

        # lambda_ds.create_resolver(
        #     type_name="Mutation",
        #     field_name= "updateNote"
        #     )

