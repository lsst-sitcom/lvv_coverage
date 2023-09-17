# source jira_python/bin/activate

# verification_elements[3].fields.customfield_15106)

import requests
import jira
from jira import JIRA
import numpy as np
from collections import OrderedDict

"""
jira = JIRA("https://jira.lsstcorp.org")

query = 'issuetype = Verification AND project = "LSST Verification and Validation" AND labels = "CommissioningSV" AND "Requirement ID" ~ OSS ORDER BY  "Requirement ID"'
issues = jira.search_issues(query, 
                            maxResults=10000)
"""

#parser.feed(issues[3].fields.customfield_15106)

#base_url = "https://jira.lsstcorp.org"
#api_endpoint = "/rest/atm/1.0"

#username='kbechtol'
#password='something'

"""
#url = f"{base_url}{api_endpoint}/testrun/{test_cycle_key}/testcase/{test_case_key}/testresult"
#url = 'https://jira.lsstcorp.org/rest/atm/1.0/testplan/search/?query=projectKey = "LVV" AND folder = "/Project Systems Engineering/Archive Commissioning Science Verification"'

# Test Cases


# Test Cycles
#url = 'https://jira.lsstcorp.org/rest/atm/1.0/testrun/search/?query=projectKey%20=%20%22LVV%22%20AND%20folder%20=%20%22/Project%20Systems%20Engineering/Commissioning%20Science%20Verification%22'

# Test Plans
#url = 'https://jira.lsstcorp.org/rest/atm/1.0/testplan/search/?query=projectKey%20=%20%22LVV%22%20AND%20folder%20=%20%22/Project%20Systems%20Engineering/Archive%20Commissioning%20Science%20Verification%22'

# Set the request headers
headers = {
    "Content-Type": "application/json",
}

# Make the API request
response = requests.get(
    url,
    auth=(username, password),
    headers=headers,
)

results = response.json()
"""

#def searchInLists(x, search):
    
# Precompute step
#test_case_search = {}
#for key in test_cases.keys()
#    test_case_search[key] = test_cases[key].getVerificationElementKeys()

#results = {}
#for key in verification_elements.keys()
#    results[key] = [k for ]


#search = [test_cases[key].getVerificationElementKeys() for key in test_cases]
#np.array([key for key in test_cases.keys()])

#for verification_element_key in verification_elements.keys():
#    for test_case_key in test_cases.keys():
 
# Goal: return the test case keys         
    

def getVerificationElements():
    jira_client = JIRA("https://jira.lsstcorp.org")

    query = 'issuetype = Verification AND project = "LSST Verification and Validation" AND labels = "CommissioningSV" AND "Requirement ID" ~ OSS ORDER BY  "Requirement ID"'
    verification_elements_raw = jira_client.search_issues(query, 
                                                          maxResults=10000)

    verification_elements = OrderedDict()
    for item in verification_elements_raw: 
        verification_elements[item.key] = VerificationElement(item.fields.__dict__)
        verification_elements[item.key]['key'] = item.key
        #verification_elements[item.key] = item
    
    return verification_elements


def zephyrAPIRequest(url, auth):
    """Get response from """
    
    # Set the request headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Make the API request
    response = requests.get(
        url,
        auth=auth,
        headers=headers,
    )
    
    if response.status_code == 200:
        results = response.json()
    else:
        print("Failed to retrieve test execution steps. Error:", response.text)
    
    return results
    
    
def getTestCases(auth):
    url = 'https://jira.lsstcorp.org/rest/atm/1.0/testcase/search/?query=projectKey%20=%20%22LVV%22%20AND%20component%20=%20%22PSE%22%20&maxResults=1000'
    test_cases_raw = zephyrAPIRequest(url, auth)
    
    test_cases = OrderedDict()
    for item in test_cases_raw:
        test_cases[item['key']] = TestCase(item)
    
    return test_cases


def getTestCycles(auth):
    url = 'https://jira.lsstcorp.org/rest/atm/1.0/testrun/search/?query=projectKey%20=%20%22LVV%22%20AND%20folder%20=%20%22/Project%20Systems%20Engineering/Commissioning%20Science%20Verification%22'
    test_cycles_raw = zephyrAPIRequest(url, auth)
    
    test_cycles = OrderedDict()
    for item in test_cycles_raw:
        test_cycles[item['key']] = TestCycle(item)
    
    return test_cycles


def getTestPlans(auth):
    url = 'https://jira.lsstcorp.org/rest/atm/1.0/testplan/search/?query=projectKey%20=%20%22LVV%22%20AND%20folder%20=%20%22/Project%20Systems%20Engineering/Archive%20Commissioning%20Science%20Verification%22'
    test_plans_raw = zephyrAPIRequest(url, auth)
    
    test_plans = OrderedDict()
    for item in test_plans_raw:
        test_plans[item['key']] = TestPlan(item)
    
    return test_plans


def convertToList(x):
    if isinstance(x, list):
        return x
    else:
        return []
    

def convertToUniqueList(x):
    x = convertToList(x)
    if x == []:
        return x
    else:
        return np.unique(np.concatenate(x)).tolist()


class VerificationElement(dict):
    """Hold information relevant to a verification element"""

    #def getTestCaseKeys(self, test_cases):
    #    search = [np.isin(self.get('key'), test_cases[key].getVerificationElementKeys())[0] for key in test_cases]
    #    # [test_cases[key].getVerificationElementKeys() for key in test_cases]
    #    return np.array(test_cases.keys())[search].tolist()

    #def getTestCycles(test_cycles):
    #    pass
        
    #def getTestPlans(test_plans):
    #    pass
    
    def __init__(self, *args, **kwargs):
        super(VerificationElement, self).__init__(*args, **kwargs)
        self.testCaseKeys = []
    
    def addTestCaseKey(self, key):
        if key not in self.testCaseKeys:
            self.testCaseKeys.append(key)
    
    def getTestCaseKeys(self):
        return self.testCaseKeys

    def getTestCycleKeys(self, test_cases):
        test_cycle_keys = []
        for key in self.getTestCaseKeys():
            try:
                test_cycle_keys.append(test_cases[key].getTestCycleKeys())
            except KeyError:
                print('WARNING: no test case %s'%(key))
            
        return convertToUniqueList(test_cycle_keys)
    
    def getTestPlanKeys(self, test_cases, test_cycles):
        test_case_keys = self.getTestCaseKeys()
        
        test_plan_keys = []
        for key in test_case_keys:
            try:
                test_plan_keys.append(test_cases[key].getTestPlanKeys(test_cycles))
            except KeyError:
                print('WARNING: no test cycle %s'%(key))
            
        return convertToUniqueList(test_plan_keys)


class TestCase(dict):
    """Hold information relevant to a Test Case"""
    
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.testCycleKeys = []
    
    def addTestCycleKey(self, key):
        if key not in self.testCycleKeys:
            self.testCycleKeys.append(key)
    
    def getVerificationElementKeys(self):
        verification_element_keys = self.get('issueLinks')
        return convertToList(verification_element_keys)
    
    def setVerificationElementCoverage(self, verification_elements):
        verification_element_keys = self.getVerificationElementKeys()
        for key in verification_element_keys:
            try:
                verification_elements[key].addTestCaseKey(self.get('key'))
            except KeyError:
                print('WARNING: no verification element %s'%(key))
        return verification_elements

    def getTestCycleKeys(self):
        return self.testCycleKeys
    
    def getTestPlanKeys(self, test_cycles):
        test_plan_keys = []
        for key in self.getTestCycleKeys():
            try:
                test_plan_keys.append(test_cycles[key].getTestPlanKeys())
            except KeyError:
                print('WARNING: no test cycle %s'%(key))
            
        return convertToUniqueList(test_plan_keys)


class TestCycle(dict):
    """Hold information relevant to a Test Cycle"""
    
    def __init__(self, *args, **kwargs):
        super(TestCycle, self).__init__(*args, **kwargs)
        self.testPlanKeys = []
    
    def addTestPlanKey(self, key):
        if key not in self.testPlanKeys:
            self.testPlanKeys.append(key)
    
    def getTestCaseKeys(self):
        test_case_keys = []
        for item in self.get('items'):
            test_case_keys.append(item['testCaseKey'])
            
        return convertToList(test_case_keys)
    
    def getVerificationElementKeys(self, test_cases):
        test_case_keys = self.getTestCaseKeys()
        
        verification_element_keys = []
        for key in test_case_keys:
            try:
                verification_element_keys.append(test_cases[key].getVerificationElementKeys())
            except KeyError:
                print('WARNING: no test case %s'%(key))
        
        return convertToUniqueList(verification_element_keys)
    
    def setTestCaseCoverage(self, test_cases):
        test_case_keys = self.getTestCaseKeys()
        for key in test_case_keys:
            try:
                test_cases[key].addTestCycleKey(self.get('key'))
            except KeyError:
                print('WARNING: no test case %s'%(key))
        return test_cases
    
    def getTestPlanKeys(self):
        return self.testPlanKeys
        
    
class TestPlan(dict):
    """Hold information relevant to a Test Plan"""
    
    def getTestCycleKeys(self):
        test_cycle_keys = []
        for item in self.get('testRuns'):
            test_cycle_keys.append(item['key'])
            
        return convertToList(test_cycle_keys)
    
    def getTestCaseKeys(self, test_cycles):
        test_cycle_keys = self.getTestCycleKeys()
        
        test_case_keys = []
        for key in test_cycle_keys:
            try:
                test_case_keys.append(test_cycles[key].getTestCaseKeys())
            except KeyError:
                print('WARNING: no test case %s'%(key))
            
        return convertToUniqueList(test_case_keys)
    
    def getVerificationElementKeys(self, test_cycles, test_cases):
        test_cycle_keys = self.getTestCycleKeys()
        
        verification_element_keys = []
        for key in test_cycle_keys:
            try:
                verification_element_keys.append(test_cycles[key].getVerificationElementKeys(test_cases))
            except KeyError:
                print('WARNING: no test cycle %s'%(key))
            
        return convertToUniqueList(verification_element_keys)
    
    def setTestCycleCoverage(self, test_cycles):
        test_cycle_keys = self.getTestCycleKeys()
        for key in test_cycle_keys:
            try:
                test_cycles[key].addTestPlanKey(self.get('key'))
            except KeyError:
                print('WARNING: no test cycle %s'%(key))
        return test_cycles
        

        


# Test cases
# 'key': 'LVV-T259',
# Links to verification elements
# 'issueLinks': ['LVV-11302', 'LVV-11300']

# Test cycles
# 'key': 'LVV-C66',
# Links to test cases
# 'items': [{'executedBy': None,
#   'actualEndDate': None,
#   'testCaseKey': 'LVV-T546',
#   'id': 526,
#   'assignedTo': 'danielsf',
#   'status': 'Not Executed'},
#  {'executedBy': None,
#   'actualEndDate': None,
#   'testCaseKey': 'LVV-T543',
#   'id': 519,
#   'assignedTo': 'danielsf',
#   'status': 'Not Executed'}],

# Test plans
# key': 'LVV-P2',
# Links to test cycles
# 'testRuns': [{'estimatedTime': 0,
#   'updatedBy': 'kbechtol',
#   'issueKey': 'LVV-1544',
#   'description': 'Initial verification of the single-visit performance of ComCam with respect to<ol><li>Delivered image quality</li><li>Photometric performance</li><li>Astrometric performance</li><li>Image depth</li></ol><br>The nominal planned on-sky observations for this test are 20 fields x 5 epochs x 5 visits x 6 filters = 3K visits (~4 nights of observations)<ul><li>Several of the fields should contain absolute spectrophotometric calibration standards.</li><li>The fields should cover a range of airmasses and source densities.</li></ul><br>These same observations are planned to be <a href="https://jira.lsstcorp.org/secure/Tests.jspa#/testCycle/LVV-C6">repeated with LSSTCam</a> to enable verification tests across the full focal plane.',
#   'updatedOn': '2019-05-21T18:32:13.000Z',
#   'createdOn': '2018-08-29T06:26:41.000Z',
#   'issueCount': 0,
#   'plannedEndDate': '2018-08-29T06:26:30.000Z',
#   'executionTime': 0,
#   'projectKey': 'LVV',
#   'testCaseCount': 25,
#   'folder': '/Project Systems Engineering/Commissioning Science Verification',
#   'plannedStartDate': '2018-08-29T06:26:30.000Z',
#   'createdBy': 'kbechtol',
#   'name': 'Commissioning SV: Single-visit Performance w/ ComCam',
#   'key': 'LVV-C4',
#   'status': 'Not Executed'},