from great_expectations.core.batch import RuntimeBatchRequest
from pandas import DataFrame

import great_expectations as ge

DATA_ASSET_NAME = "my_data_asset"
EXPECTATION_SUITE_NAME = "my_expectation_suite"
CHECKPOINT_NAME = "my_checkpoint"


def init_runtime_batch_request(data_frame: DataFrame) -> dict:
    return RuntimeBatchRequest(
        datasource_name="example_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=DATA_ASSET_NAME,
        runtime_parameters={"batch_data": data_frame},
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )


def run(data_frame: DataFrame) -> None:
    context = ge.get_context()
    # RuntimeBatchRequest that takes in the dataframe as batch_data
    batch_request = init_runtime_batch_request(data_frame=data_frame)
    context.run_checkpoint(
        checkpoint_name=CHECKPOINT_NAME,
        validations=[{"batch_request": batch_request}],
    )
