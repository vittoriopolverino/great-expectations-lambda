#!/usr/bin/env bash

CMD_ARGS=$1
DEFAULT_PATH=C:/great_expectations_data_docs/
FOLDER_PATH="${CMD_ARGS:=$DEFAULT_PATH}"

export_ge_data_docs() {
  echo "Exporting the great expectations data docs in $FOLDER_PATH . . ."
  docker cp lambda-container:/var/task/great_expectations/uncommitted/data_docs/ $FOLDER_PATH
}

export_ge_data_docs

$SHELL
