import pandas as pd
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
                "module_name": "great_expectations.datasource.data_connector",
                "batch_identifiers": ["default_identifier_name"],
            },
        },
    }


def run(data: dict[str, list[str]]) -> list[dict]:
    context = ge.get_context()

    datasource_config = init_datasource()

    context.test_yaml_config(yaml.dump(datasource_config))
    context.add_datasource(**datasource_config)

    df = pd.DataFrame(data)

    # Here is a RuntimeBatchRequest that takes in our df as batch_data
    batch_request = RuntimeBatchRequest(
        datasource_name="example_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="data_asset_test",
        runtime_parameters={"batch_data": df},  # df is your dataframe
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )

    context.create_expectation_suite(
        expectation_suite_name="test_suite", overwrite_existing=True
    )
    validator = context.get_validator(
        batch_request=batch_request, expectation_suite_name="test_suite"
    )

    print(validator.head())

    expectations_result = [
        validator.expect_table_row_count_to_be_between(min_value=4),
        validator.expect_column_values_to_be_unique(column="test_column"),
        validator.expect_column_values_to_not_be_null(column="test_column"),
    ]

    return expectations_result
