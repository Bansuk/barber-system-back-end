"""
Service module for phone number validation.
"""

import requests
from settings import API_KEY, URL, PRETTIFY_JSON_RESPONSE


class NumVerify:
    """
    A helper class for interacting with the NumVerify phone number
    validation API.

    This class provides methods to send validation requests and
    retrieve structured information about a given phone number.
    """

    @staticmethod
    def _get_number_validation(params: object) -> dict:
        """
        Send a request to the NumVerify API to validate a phone number.

        This internal helper method performs the HTTP GET request using the
        provided parameters and returns the JSON response if successful.

        Args:
            params (object): A dictionary of query parameters to include
                           in the API request.

        Returns:
            dict: The parsed JSON response from the API if the
                         HTTP request succeeds (status 200).

        Raises:
            requests.HTTPError: If the API returns a non-200 status code.
        """

        response = requests.get(URL, params=params, timeout=10)

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"NumVerify API request failed: {response.status_code} - {response.text}"
            ) from exc

        return response.json()

    @staticmethod
    def validate_phone_number(phone_number: str) -> dict:
        """
        Validate a phone number using the NumVerify API.

        This method formats the required query parameters and delegates
        the API call to `_get_number_validation`.

        Args:
            phone_number (str): The phone number to validate. It should
                                be a numeric string.

        Returns:
            dict: The validation result returned by the NumVerify API.
        """

        params = {
            "access_key": API_KEY,
            "number": phone_number,
            "format": PRETTIFY_JSON_RESPONSE,
            "country_code": 'BR'
        }

        return NumVerify._get_number_validation(params)
