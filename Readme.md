# Hierarchical Process Discovery

It is a methodology which allows abstraction of certain patterns, based on some criterion (tandem arrays, maximal repeats) and filtering event log in order to make its simplified version. The abstraction may repeatedly perform and hierarchical structures can be made in tree-like shape.

## Usage

```bash
python main.py --path "example.xes" [--userPatterns] [--downloadLog] [--downloadModel]

python discover.py --path "example.xes"

python abstraction.py --path "./example.xes" --pattern 1 2 3

python transformation.py --path "./example.xes" [--downloadLog] [--downloadModel] --pattern 1 2 3 
```

## Instructions
##### Step 1: 
discover.py executes discovery step
##### Step 2: 
abstraction.py executes abstraction step, provided that step 1 must be executed before
##### Step 3: 
transformation.py transformation of log file, provided that step 1 must be executed before. There is no need to execute Step 2 because it is executing internally

If anyone would like to execute all steps at once then main.py executes all above steps sequentially


## Authors and acknowledgment
This project is supervised by the Process and Data Science (pads) Chair from RWTH Aachen University

## Workflow Diagram

https://git.rwth-aachen.de/sezin.maden/hirarchical-pd/-/blob/master/FunctionModel.PNG
