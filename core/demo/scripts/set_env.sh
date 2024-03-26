#!/bin/bash

# Get the root path of the git repository
path_git_root=$(git rev-parse --show-toplevel)
path_core="$path_git_root/core"
path_demo=$(dirname "$0")

echo "Update PYTHONPATH environment variable"
export PYTHONPATH="$path_git_root:$path_core:$path_demo:$PYTHONPATH"
echo "PYTHONPATH updated to $PYTHONPATH."

echo "Set environment variable for workflow configuration"
export WORKFLOW_CONFIG="demo.workflows.__tpl_workflow_builder.config"
echo "Environment variable WORKFLOW_CONFIG set to $WORKFLOW_CONFIG."
