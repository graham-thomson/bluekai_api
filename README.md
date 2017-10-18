### Unofficial Bluekai Python API

**<a href="https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCDA/Developers/api_getting_started.html">Bluekai APIs</a> Supported**
* <a href="https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCDA/Developers/reference/categories_rest_api.html">Categories</a>
    * Supported Methods:
        * [GET] List categories
        * [GET] Read a category
        * [POST] Create a category
        * [PUT] Update a category
* <a href="https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCDA/Developers/reference/self_classification_rule_api.html">Self Classification Rule</a>
    * Supported Methods:
        * [GET] List rules
        * [GET] Read a rule
        * [POST] Create a rule
        * [PUT] Update a rule

#### Usage
 
```python
from pprint import pprint
from bluekaiapi.categories import Categories
api = Categories(user_key="abcd", private_key="1234")
api.read_category("3141579")
print(resp[0])
pprint(resp[1])
```
#### Returns:
```
200
{u'categoryType': u'selfClassification',
 u'id': 3141579,
 u'isCountableFlag': True,
 u'isExplicitPriceFloorFlag': False,
 u'isForNavigationOnlyFlag': False,
 u'isIncludeForAnalyticsFlag': True,
 u'isLeafFlag': True,
 u'isMutuallyExclusiveChildrenFlag': False,
 u'isPublicFlag': False,
 u'links': [],
 u'name': u'Some-Bluekai-Category-Name',
 u'ownershipType': u'firstParty',
 u'parentCategory': {u'id': 999999},
 u'partner': {u'id': 3097},
 u'pathFromRoot': {u'ids': [300, 493135, 3141579],
                   u'names': [u'ROOT',
                              u'Self-Classification',
                              u'Some-Bluekai-Category-Name']},
 u'sortOrder': 9999,
 u'status': u'active',
 u'vertical': {u'name': u'My DMP'},
 u'visibilityStatus': u'notHidden'}
```