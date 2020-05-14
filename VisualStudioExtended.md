# Setting up Visual Studio as a text editor for running Tasks (PML/SML processors)
(c) Craig Duncan 2019-2020

22.12.2019.

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
} 
```

# Alternatives

This description suggests you can make tasks that are not 'builds'

"File -> Open Folder. The do Ctrl+Shift+P, then Configure Task and press Enter. This will create a folder called .settings and a file called tasks.json where you will configure your task. Comment out the first example task and put the following Python task at the top of the file and save it."

https://stevenwooding.com/how-to-run-python-in-visual-studio-code/

There's also a suggestion you can open your output window on the RHS of VS Code.

# Markdown view in Visual Studio?

(cf where Markdown is involved and you want a 'markdown' view)
i.e. if my programs export a file that is markdown back as output it could 'preview'?

## Some other things to note.

If you prepare a file with a .md file extension, visual studio will process it and provide an outline view in the Explorer panel on the left, using the # and ## hashtags used for headings.

Preview your markdown in VisualStudio with:
"To switch between views, press ⇧⌘V in the editor. You can view the preview side-by-side (⌘K V) with the file you are editing and see changes reflected in real-time as you edit."
https://code.visualstudio.com/Docs/languages/markdown#_markdown-preview

This means:
1. Shift-CMD-V to get into preview mode
2. Create another window using CTRL-K commands (you can press the split window icon at top to do the same)

# Lawcoder v markdown

NB: 
1. LawCoder is my generic name for my python translater/markdown interpretre program.
2. If the 'legal' document:
(a) uses markdown for most of the file, then
(b) has some additional parsing for docx conversion, 

then it combines all the power of a text editor with the additional 'legal output' function?  
i.e. leverages off existing tools, but supplements them.
