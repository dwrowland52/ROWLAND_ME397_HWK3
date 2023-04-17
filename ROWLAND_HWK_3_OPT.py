"""
Using code from Lecture 19 as a base since it already has the solar part completed.

Code edited and updated by Drake Rowland

Not adding EID b/c it's going to a public Github
"""
#%% Required imports section

from __future__ import division         # Unsure why this is here
from pyomo.environ import *             # Load pyomo module
from pyomo.opt import SolverFactory     # Loading OPT of pyomo


#%% Constants and assumptions section

# Costs for solar, wind, and energy storage systems
solarCapitalCost = 8*10**8       # $/GW
windCapitalCost  = 120*10**8     # $/GW
ESSpCapitalCost  = 2*10**8       # $/GW
ESSeCapitalCost  = 15*10**8      # $/GWh

# Energy storage operational assumptions
curtailment = 1000          # Curtailment penalty $/GWh
ESSmin = 0.20               # Minimum level of battery percentage
ESSChargeEff = 0.95         # ESS charging efficiency, looses 5% when charging
ESSDischargeEff = 0.9       # ESS discharging efficiency, looses 10% when discharging
ESSDischargeCost = 5000     # ESS discharge cost $/GWh


#%% Model creation section

# Create the model, keeping the same as in lecture code
model = AbstractModel(name = 'Solar-Wind-Demand-Storage Model')

# Create model sets
model.t = Set(initialize = [i for i in range(8760)], ordered=True)  
# Updated to add wind cap 
model.tech = Set(initialize =['SolarCap', 'WindCap', 'ESSPowerCap', 'ESSEnergyCap'], ordered=True)  

# Parameters for the model, added wind and demand
model.solar = Param(model.t)    # Setting solar up as a parameter
model.wind = Param(model.t)     # Setting wind up as a parameter
model.demand = Param(model.t)   # Setting demand up as a parameter

# Setting cost as a parameter and initializing values
model.costs = Param(model.tech, initialize={'SolarCap' : solarCapitalCost, 'WindCap' : windCapitalCost, 'ESSPowerCap' : ESSpCapitalCost, 'ESSEnergyCap' : ESSeCapitalCost})


#%% Load data section

## Get data imported into model using DataPortal()
data = DataPortal()
# Load solar data through the ERCOT data
data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'solar'), param = model.solar, index = model.t)
# Loading wind data through the ERCOT data, added
data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'wind'), param = model.wind, index = model.t)
# Loading demand data through the ERCOT data, added
data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'demand'), param = model.demand, index = model.t)


#%% Define variables section
model.cap = Var(model.tech, domain = NonNegativeReals)      # Defining variable cap and the range of possible numbers it can be
model.ESS_SOC = Var(model.t, domain = NonNegativeReals)     # Defining variable ESS_SOC and the range of possible numbers it can be
model.ESS_c = Var(model.t, domain = NonNegativeReals)       # Defining variable ESS_c and the range of possible numbers it can be
model.ESS_d = Var(model.t, domain = NonNegativeReals)       # Defining variable ESS_d and the range of possible numbers it can be
model.curt = Var(model.t, domain = NonNegativeReals)        # Defining variable curt and the range of possible numbers it can be


#%% Defining objective function and constraints of model

# Main objective
def obj_expression(model):
    return sum(model.cap[i] * model.costs[i] for i in model.tech) + sum(model.ESS_d[t] * ESSDischargeCost + model.curt[t] * curtailment for t in model.t) 

# Setting OBJ of model
model.OBJ = Objective(rule=obj_expression)

# Supply/demand match constraint, updated for wind and demand
def match_const(model, i):
    return model.solar[i]*model.cap['SolarCap'] + model.wind[i]*model.cap['WindCap'] + model.ESS_d[i] - model.ESS_c[i] - model.curt[i] - model.demand[i] == 0   

# Setting constraint of energy matching
model.match = Constraint(model.t, rule = match_const)

# ESS charge/discharge constraint
def ESS_charge_disc_const(model, i):
    return model.ESS_c[i] + model.ESS_d[i] <= model.cap['ESSPowerCap']   

# Setting constraint of charging
model.ESS_charge_disc_rate = Constraint(model.t, rule = ESS_charge_disc_const)

# ESS max constraint
def ESS_max_const(model, i):
    return model.ESS_SOC[i] <= model.cap['ESSEnergyCap']   

# Setting constraint of max charge
model.ESS_max = Constraint(model.t, rule = ESS_max_const) 

# ESS min constraint
def ESS_min_const(model, i):
    return model.ESS_SOC[i] >= ESSmin * model.cap['ESSEnergyCap']   

# Setting constraint of min charge
model.ESS_min = Constraint(model.t, rule = ESS_min_const)      

# SOC constraint
def SOC_const(model, i):
    if i == model.t.first(): 
        return model.ESS_SOC[i] == model.ESS_SOC[model.t.last()] + (model.ESS_c[i] * ESSChargeEff) - (model.ESS_d[i]/ESSDischargeEff) 
    return model.ESS_SOC[i] == model.ESS_SOC[i-1] + (model.ESS_c[i] * ESSChargeEff) - (model.ESS_d[i]/ESSDischargeEff) 

# Setting constraint of SOC
model.SOC_const = Constraint(model.t, rule = SOC_const)


#%% Setting model to be solved when ran through command line

# Create instance of the model (abstract only)
model = model.create_instance(data)

# Solve the model, use glpk b/c I don't wanna sign up for gurobi
opt = SolverFactory('glpk')
status = opt.solve(model) 

# write model outputs to a JSON file
model.solutions.store_to(status)
status.write(filename='ROWLAND_HWK3_OPT_OUTPUTS.json', format='json')

# pyomo solve ROWLAND_HWK_3_OPT.py --solver=glpk