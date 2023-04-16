# ME397 Too Big To Excel HWK3 Git Repo

## Files:
* opt_model_data: Directory that contains .csv data for optimization question.
* .gitignore: Files to be ignored and untracked.
* ROWLAND_HWK_3_OPT.py: Python script that solves the optimization question in task 1.
* README: Provides a description of this repo. 

## Homework Tasks:
1. Update optimization script used in class on 3/29/2023 to include wind generation and non-constant demand. Also update it to become the estimate for the lowest cost mix of solar, wind, and energy storage that would be required to run all of ERCOT in 2022.
2. Create a public GitHub repo to keep track of changes. We need to at least have 3 pushes to our main branch for work done on Task 1. After it's completed then we will send a collaborate link to the professor. 

## Work Done:
1. Task 1
    + Created a copy of the L19 pyomo script mentioned and changed the name to the desired file name "(LASTNAME)_HWK_3_OPT.py".
    + Ran the script without any changes to confirm pyomo was working correctly.
    + Updated that script to match my style of naming for variables (easier for me to read).
    + Added variables and sections needed to wind and demand to be added to the optimization problem.
    + Ran the script and confirmed my output with the expected values from the Task 1 description.

2. Task 2
   - Using the command line I started a repo in the ROWLAND_ME397_HWK3 directory.
   - Then I added the new git repo to my GitHub account.
   - My first push to "origin" was just a .gitignore and the opt_model_data directory.
   - The second commit was adding more info to the ignore file and creating an empty python script for Task 1.
   - The third was adding again updating the .gitignore to exclude the files/directory that are created whenever pyomo is ran. Also filled in the "template" code which is the code from L19.
   - Forth is adding the update script that includes the wind and demand in the optimization problem. Also added a README for extra practice. 


## Calling the Script:
* First install pyomo and glpk into virtual enviroment
* To run the optimization script use this in the command line:
    ```bash
    pyomo solve ROWLAND_HWK_3_OPT.py --solver=glpk
    ```