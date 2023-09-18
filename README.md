# lvv_coverage

Tools for exploring traceability and coverage in the Rubin Observatory Jira LVV project

## Setup

Working on lsst-devl note on S3DF cluster at USDF.

Suggest to set up a virtual environment following the Jira REST API documentation

https://jira.readthedocs.io/installation.html

in particular

```
python -m venv jira_python
source jira_python/bin/activate
pip install 'jira[cli]'
pip install numpy
```

Also, for authentication, create a `$HOME/.netrc` file with the following contents

```
machine jira.lsstcorp.org
login yourusername
password something
```

## Usage

The code examples here use both the Jira REST API 

https://jira.readthedocs.io/ 

and Zephyr Scale REST API

https://support.smartbear.com/zephyr-scale-server/api-docs/v1/

The Jira API is implemented as a python library and allows access to the verification elements.

The Zephyr Scale REST API involves creating a URL to access data regarding test cases, test cycles, and test plans.

The query results are converted to dictionaries indexed by the key of the respective verification element, test case, test cycle, or test plan.

Currently, the queries have been hardcoded for system-level science performance use case. A TODO is adding generality to the query construction.

See example_lvv_coverage.py for example usage.