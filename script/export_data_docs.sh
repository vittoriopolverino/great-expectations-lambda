#!/usr/bin/env bash

CMD_ARGS=$1
DEFAULT_PATH=C:/great_expectations_data_docs/
FOLDER_PATH="${CMD_ARGS:=$DEFAULT_PATH}"

copy_ge_local_site() {
  echo "Copying the great expectations local site in $FOLDER_PATH . . ."
  docker cp lambda-container:/var/task/great_expectations/uncommitted/data_docs $FOLDER_PATH
}

copy_ge_local_site

$SHELL
