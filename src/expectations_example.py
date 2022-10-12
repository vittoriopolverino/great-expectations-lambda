from time import gmtime, strftime

from pandas import DataFrame
from great_expectations.core.batch import RuntimeBatchRequest
from ruamel import yaml

import great_expectations as ge


DATA_ASSET_NAME = "my_data_asset"
EXPECTATION_SUITE_NAME = "my_expectation_suite"
CHECKPOINT_NAME = "my_checkpoint"


def init_datasource() -> dict:
    return {
        "name": "example_datasource",
        "class_name": "Datasource",
        "module_name": "great_expectations.datasource",
        "execution_engine": {
            "module_name": "great_expectations.execution_engine",
            "class_name": "PandasExecutionEngine",
        },
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"],
            },
        },
    }


def init_runtime_batch_request(dataframe: DataFrame) -> dict:
    return RuntimeBatchRequest(
        datasource_name="example_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=DATA_ASSET_NAME,
        runtime_parameters={"batch_data": dataframe},
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )


def init_checkpoint() -> dict:
    return {
        "name": CHECKPOINT_NAME,
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "expectation_suite_name": EXPECTATION_SUITE_NAME,
        "run_name_template": f"test-run-{strftime('%Y-%m-%d-%H-%M-%S', gmtime())}",
    }


def run(dataframe: DataFrame) -> None:
    context = ge.get_context()

    datasource_config = init_datasource()
    context.test_yaml_config(yaml.dump(datasource_config))
    context.add_datasource(**datasource_config)

    # RuntimeBatchRequest that takes in the dataframe as batch_data
    batch_request = init_runtime_batch_request(dataframe=dataframe)

    # Define a new expectation suite
    context.create_expectation_suite(
        expectation_suite_name=EXPECTATION_SUITE_NAME,
        overwrite_existing=True
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=EXPECTATION_SUITE_NAME
    )

    validator.expect_table_row_count_to_be_between(min_value=1, max_value=4),
    validator.expect_column_values_to_be_unique(column="test_column"),
    validator.expect_column_values_to_not_be_null(column="test_column"),
    validator.save_expectation_suite(discard_failed_expectations=False)

    # Checkpoint
    checkpoint_config = init_checkpoint()
    context.add_checkpoint(**checkpoint_config)
    checkpoint_result = context.run_checkpoint(
        checkpoint_name=CHECKPOINT_NAME,
        validations=[{"batch_request": batch_request}],
    )

    validation_result_identifier = (
        checkpoint_result.list_validation_result_identifiers()[0]
    )

    # Generate data docs
    context.build_data_docs()
    context.open_data_docs(resource_identifier=validation_result_identifier)
