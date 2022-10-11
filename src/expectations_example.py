from time import gmtime, strftime
import pandas as pd
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.batch import RuntimeBatchRequest
from ruamel import yaml

import great_expectations as ge


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


def run(data: dict[str, list[str]]) -> None:
    context = ge.get_context()
    data_asset_name = "my_data_asset"
    expectation_suite_name = "my_expectation_suite"
    checkpoint_name = "my_checkpoint"
    df = pd.DataFrame(data)

    datasource_config = init_datasource()
    context.test_yaml_config(yaml.dump(datasource_config))
    context.add_datasource(**datasource_config)

    # Here is a RuntimeBatchRequest that takes in our df as batch_data
    batch_request = RuntimeBatchRequest(
        datasource_name="example_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=data_asset_name,
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )

    context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name,
        overwrite_existing=True
    )

    context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name, overwrite_existing=True
    )

    validator = context.get_validator(
        batch_request=batch_request, expectation_suite_name=expectation_suite_name
    )

    validator.expect_table_row_count_to_be_between(min_value=1, max_value=4),
    validator.expect_column_values_to_be_unique(column="test_column"),
    validator.expect_column_values_to_not_be_null(column="test_column"),
    validator.save_expectation_suite(discard_failed_expectations=False)

    checkpoint_config = {
        "name": checkpoint_name,
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "expectation_suite_name": expectation_suite_name,
        "run_name_template": f"test-run-{strftime('%Y-%m-%d-%H-%M-%S', gmtime())}"
    }
    context.add_checkpoint(**checkpoint_config)

    checkpoint_result = context.run_checkpoint(
        checkpoint_name=checkpoint_name,
        validations=[
            {"batch_request": batch_request}
        ],
    )

    validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]

    context.build_data_docs()
    context.open_data_docs(resource_identifier=validation_result_identifier)
