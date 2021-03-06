import numpy as np
from BayesianNetwork import BayesianNetwork
from utils import *

     
joint_probs = [i.strip().split('\t') for i in open('joint.dat')]
data = np.array([complete_bin(int(i.strip())) for i in open('dataset.dat')])
joint_probs = np.array(map(lambda x: (complete_bin(int(x[0])), float(x[1])), joint_probs))

baseline_settings = {
    'IsSummer': [],
    'HasFlu': [],
    'HasFoodPoisoning': [],
    'HasHayFever': [],
    'HasPneumonia': [],
    'HasRespiratoryProblems': [],
    'HasGastricProblems': [],
    'HasRash': [],
    'Coughs': [],
    'IsFatigues': [],
    'Vomits': [],
    'HasFever': []
    }

settings = {
    'IsSummer': [],
    'HasFlu': ['IsSummer'],
    'HasFoodPoisoning': [],
    'HasHayFever': ['IsSummer'],
    'HasPneumonia': ['IsSummer'],
    'HasRespiratoryProblems': ['HasFlu', 'HasHayFever', 'HasPneumonia'],
    'HasGastricProblems': ['HasFoodPoisoning'],
    'HasRash': ['HasFlu', 'HasHayFever'],
    'Coughs': ['HasFlu', 'HasHayFever', 'HasPneumonia'],
    'IsFatigues': ['HasFlu', 'HasHayFever', 'HasPneumonia'],
    'Vomits': ['HasFlu', 'HasFoodPoisoning', 'HasGastricProblems'],
    'HasFever': ['HasFlu', 'HasPneumonia']
    }

settings2 = {
    'IsSummer': [],
    'HasFlu': ['IsSummer'],
    'HasFoodPoisoning': [],
    'HasHayFever': [],
    'HasPneumonia': ['IsSummer'],
    'HasRespiratoryProblems': ['HasFlu', 'HasHayFever', 'HasPneumonia', 'HasFoodPoisoning'],
    'HasGastricProblems': ['HasFlu', 'HasFoodPoisoning'],
    'HasRash': ['HasFoodPoisoning', 'HasHayFever'],
    'Coughs': ['HasFlu', 'HasPneumonia', 'HasRespiratoryProblems'],
    'IsFatigues': ['HasFlu', 'HasHayFever', 'HasPneumonia'],
    'Vomits': ['HasFoodPoisoning', 'HasGastricProblems'],
    'HasFever': ['HasFlu', 'HasPneumonia']
    }

feature_list = ['HasFever', 'Vomits', 'IsFatigues', 'Coughs', 'HasRash',
                'HasGastricProblems', 'HasRespiratoryProblems', 'HasPneumonia',
                'HasHayFever', 'HasFoodPoisoning', 'HasFlu', 'IsSummer']

model = BayesianNetwork(settings2, feature_list)
model.fit(data)
pred_table = model.predict(joint_probs)
score = compute_accuracy(pred_table, joint_probs)

query1 = query_from_table('HasFlu', feature_list, joint_probs, ('HasFever', True), ('Coughs', True))
pred_query1 = query_from_table('HasFlu', feature_list, pred_table, ('HasFever', True), ('Coughs', True))
query2 = query_from_table('Vomits', feature_list, joint_probs, ('IsSummer', True))
pred_query2 = query_from_table('Vomits', feature_list, pred_table, ('IsSummer', True))
