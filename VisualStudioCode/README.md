# Setting up Visual Studio as a text editor for running Tasks (PML/SML processors)
(c) Craig Duncan 2019-2020
Created 22 December 2019.

Within Visual Studio, you can create your own extension to run a python processing file with the currently selected document.

1. You need to create a tasks.json file in the .vscode folder in the current Workspace.

If you haven't created a workspace, do this first.

2. Include both the python scripts and the markdown files in the workspace.

It may be possible to run the python script with the input file and the output files in different places.

## Tasks.json

Configure Default Build Task to set your tasks.json file initially.

The command option should only include the name of the program to be run in the shell.   Any filenames to be used have to be added as 'args' in the JSON used by Visual Studio.

Ultimately, if you want different build options (different flags) you can do this in your tasks.json:

```{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
      {
        "label": "lawcoder doc",
        "type": "shell",
        "command": [
          "python3"
        ],
        "args": [
          "plaineng.py",
          "${relativeFile}"
        ],
        "problemMatcher": []
      },
      {
        "label": "lawcode doc with notes",
        "type": "shell",
        "command": [
          "python3"
        ],
        "args": [
          "plaineng.py",
          "-n",
          "${relativeFile}"
        ],
        "problemMatcher": [],
        "group": {
          "kind": "build",
          "isDefault": true
        }
      }
    ]
} ```

Last updated 30 January 2020.
