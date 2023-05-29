
import time
import lob_python
from pprint import pprint
from lob_python.api import addresses_api
from lob_python.model.address import Address
from lob_python.model.address_deletion import AddressDeletion
from lob_python.model.address_editable import AddressEditable
from lob_python.model.address_list import AddressList
from lob_python.model.adr_id import AdrId
from lob_python.model.include_model import IncludeModel
from lob_python.model.lob_error import LobError
from lob_python.model.metadata_model import MetadataModel
from creds import LOB_TEST_KEY, LOB_PROD_KEY
from lob_python.model.country_extended import CountryExtended
from lob_python.model.resource_description import ResourceDescription
from lob_python.model.company import Company
from lob_python import SelfMailerEditable

# Defining the host is optional and defaults to https://api.lob.com/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = lob_python.Configuration(
    host = "https://api.lob.com/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = lob_python.Configuration(
    username = LOB_TEST_KEY,
)

api_client = lob_python.ApiClient(configuration)

def add_address(address_line1, address_line2, address_city, address_state, address_zip,name, phone, email, api_client=api_client):
    # Enter a context with an instance of the API client
    with api_client:
        # Create an instance of the API class
        api_instance = addresses_api.AddressesApi(api_client)
        print(address_line1)
        address_editable = AddressEditable(
            address_line1=address_line1,
            address_line2=address_line2,
            address_city=address_city,
            address_state=address_state,
            address_zip=address_zip,
            address_country=CountryExtended("US"),
            # description=ResourceDescription("Home"),
            name=name,
            # company="RingleDingle",
            phone=phone,
            email=email,
            metadata=MetadataModel(
                key="key_example",
            ),
        )

        try:
            # create
            api_response = api_instance.create(address_editable)
            pprint(api_response)
            # return api_response[]
        except lob_python.ApiException as e:
            print("Exception when calling AddressesApi->create: %s\n" % e)



address_line1="3 Briarwood Lane",
address_line2="",
address_city="Winchester",
address_state="Massachusetts",
address_zip="01890",
address_country=CountryExtended("US"),
# description=ResourceDescription("Home"),
name="Drew Piispanen",
company="RingleDingle",
phone="781-799-5731",
email="drew@ringledingle.com"

add_address(address_line1, address_line2, address_city, address_state, address_zip,name, phone, email)


def make_mailer(api_client = api_client):
    self_mailer_editable = SelfMailerEditable(
    description = "Demo Self Mailer job",
    _from = "adr_210a8d4b0b76d77b",
    inside = "<html style='padding: 1in; font-size: 50;'>Inside HTML for {{name}}</html>",
    outside = "<html style='padding: 1in; font-size: 20;'>Outside HTML for {{name}}</html>",
    to = AddressEditable(
        name = "Harry Zhang",
        address_line1 = "210 King St",
        address_line2 = "# 6100",
        address_city = "San Francisco",
        address_state = "CA",
        address_zip = "94107",
    ),
   
    )

    api = SelfMailersApi(api_client)
    
    try:
        created_self_mailer = api.create(self_mailer_editable)
    except ApiException as e:
        print(e)
