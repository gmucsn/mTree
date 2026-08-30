# Using mTree CLI (Command Line Interface) Utilities 

This guide shows you how to use the `mTree_cli` command to perform various operations.

## Assumptions

This guide assumes you have a working mTree environment where you have either directly installed the mTree Python package or are running inside of an mTree configured Docker container.

## The mTree_cli command

The mTree_cli command is installed and should become available when you install mTree. At any point, you can type in `mTree_cli --help` to get a list of the current options and parameters for the command.

## mTree_cli capabilities

Currently, the mtree_cli command provides the following actions

- Running a simulation
- Launching the developer server where you can test your code associated with a human subject experience
- Generating a new mTree project folder


## Running a simulation

To run an mTree simulation from the command line, you will first need to navigate to a directory that contains an mTree project.

1. Once you have navigated to an mTree proejct folder you can then type `mTree_cli simulation`.
1. You will then be asked to ask which MES you would like to run. The CLI will display a list of mTree project folders the utility can see. Navigate with the arrows keys to select which one you would want to run.
1. The CLI will then ask you which configuration file or files you would like to run in your simulation. This will be drawn from the files in the /config folder of the mTree project. You can use the space bar to select which simulations to run. After you have made your selection you can hit the enter key and then your simulation run will begin to start.
1. You will then be present a screen that shows the status of the individual actors. 
1. When your simulation is completed you can then hit the ctrl-d key combination to exit the screen
    
## Running the developer server

The mTree developer server is useful for things like testing a human subject experiment and examining parts of your codebase.

To run the mTree developer server 

1. Once you have navigated to an mTree proejct folder you can then type `mTree_cli developer-server`.
1. You will then be moved into a new interface. At the bottom of the screen you will see a list of actions. Hit the `1` key to start the web server.
1. You can then visit http://127.0.0.1:8000 to browse the controls for your experiment.