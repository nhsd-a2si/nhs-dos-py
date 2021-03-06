import requests
import logging

from .models import Service, ServiceList
from .exceptions import DosClientException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

uat_url = 'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0'


class RestApiClient:
    """
    Client object for performing requests against the DoS Rest API
    """
    def __init__(self, user, url=uat_url):

        self.user = user
        self.url = url
        self.s = requests.Session()
        self.s.auth = (user.username, user.password)

    def get_single_service(self, identifier, id_type):

        if id_type == 'dos':
            api_path = '/services/byServiceId/'
        elif id_type == 'ods':
            api_path = '/services/byOdsCode/'
        else:
            raise DosClientException("You haven't chosen a valid identifer type - it should be either dos or ods")

        url = '{0}{1}{2}'.format(self.url, api_path, identifier)

        response = self.s.get(url)

        service_count = int(response.json()['success']['serviceCount'])

        # Don't return different things based on an arbitrary scenario
        if service_count == 1:
            s1 = Service(response.json()['success']['services'][0])
            results = [s1]
            return results
        elif service_count == 0:
            return []
        else:
            raise DosClientException("Didn't get 0 or 1 services returned")

    def get_service_by_id(self, service_id):
        return self.get_single_service(service_id, 'dos')

    def get_service_by_ods(self, ods_code):
        return self.get_single_service(ods_code, 'ods')
