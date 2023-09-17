import os
import numpy as np

import lvv_coverage

import importlib
#importlib.reload(lvv_coverage)

auth_fname = os.path.expanduser("~/.netrc")
with open(auth_fname) as f:
    f.readline()
    username = f.readline().split()[-1].strip()
    password = f.readline().split()[-1].strip()
auth = (username, password)


verification_elements = lvv_coverage.getVerificationElements()
test_cases = lvv_coverage.getTestCases(auth)
test_cycles = lvv_coverage.getTestCycles(auth)
test_plans = lvv_coverage.getTestPlans(auth)


# One layer deep
for key in test_cases: 
    print(test_cases[key].getVerificationElementKeys())
for key in test_cycles:
    print(test_cycles[key].getTestCaseKeys())
for key in test_plans:
    print(test_plans[key].getTestCycleKeys())

# Two layers deep
for key in test_cycles:
    print(test_cycles[key].getVerificationElementKeys(test_cases))

for key in test_plans:
    print(test_plans[key].getTestCaseKeys(test_cycles))
    
# Three layers deep
for key in test_plans:
    print(test_plans[key].getVerificationElementKeys(test_cycles, test_cases))

for key in test_plans:
    print(key)
    verification_elements_keys = test_plans[key].getVerificationElementKeys(test_cycles, test_cases)
    for verification_element_key in verification_elements_keys:
        try:
            print('\t' + verification_elements[verification_element_key]['summary'])
        except KeyError:
            print('\tWARNING: no verification element %s'%(verification_element_key))


# Walk the hierarchy to fill in coverage
for key in test_cases:
    verification_elements = test_cases[key].setVerificationElementCoverage(verification_elements)
for key in test_cycles:
    test_cases = test_cycles[key].setTestCaseCoverage(test_cases)
for key in test_plans:
    test_cycles = test_plans[key].setTestCycleCoverage(test_cycles)


# One layer deep
for key in verification_elements.keys():
    print(key)
    print(verification_elements[key].getTestCaseKeys())
for key in test_cases.keys():
    print(key)
    print(test_cases[key].getTestCycleKeys())
for key in test_cycles.keys():
    print(key)
    print(test_cycles[key].getTestPlanKeys())

# Two layer deep
for key in verification_elements.keys():
    print(key)
    print(verification_elements[key].getTestCycleKeys(test_cases))
for key in test_cases.keys():
    print(key)
    print(test_cases[key].getTestPlanKeys(test_cycles))

# Three layer deep
for key in verification_elements.keys():
    print(key)
    print(verification_elements[key].getTestPlanKeys(test_cases, test_cycles))

for key in verification_elements:
    print(key)
    test_plan_keys = verification_elements[key].getTestPlanKeys(test_cases, test_cycles)
    for test_plan_key in test_plan_keys:
        try:
            print('\t' + test_plans[test_plan_key]['name'])
        except KeyError:
            print('\tWARNING: no test plan %s'%(test_plan_key))
