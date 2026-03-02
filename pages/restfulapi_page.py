import requests
import json
from datetime import datetime, timedelta
import time
import logging
import os

# configure logger to write API responses to a log file in workspace root
LOG_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api_responses.log'))

logger = logging.getLogger('RestfulBookerAPI')
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


class RestfulBookerAPI:
    """
    Page Object for Restful Booker API
    Base URL: https://restful-booker.herokuapp.com/
    """

    BASE_URL = "https://restful-booker.herokuapp.com"
    TIMEOUT = 10

    def __init__(self):
        self.auth_token = None
        self.booking_id = None
        self.response_time = None
        self.last_response = None

    # ==================== AUTHENTICATION ====================

    def generate_auth_token(self, username="admin", password="password123"):
        """
        Generate authentication token
        Endpoint: POST /auth
        """
        url = f"{self.BASE_URL}/auth"
        payload = {
            "username": username,
            "password": password
        }
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        if response.status_code == 200:
            self.auth_token = response.json().get("token")
            return {
                "status_code": response.status_code,
                "token": self.auth_token,
                "response_time": self.response_time
            }
        return {
            "status_code": response.status_code,
            "error": response.text,
            "response_time": self.response_time
        }

    def negative_auth(self, username="invalid", password="invalid"):
        """
        Negative authentication scenario - invalid credentials
        Endpoint: POST /auth
        """
        url = f"{self.BASE_URL}/auth"
        payload = {
            "username": username,
            "password": password
        }
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "response": response.text,
            "response_time": self.response_time
        }

    # ==================== BOOKING OPERATIONS ====================

    def create_booking(self, firstname="John", lastname="Doe", totalprice=100,
                       depositpaid=True, checkin="2024-01-01", checkout="2024-01-05",
                       additionalneeds="Breakfast"):
        """
        Create a new booking
        Endpoint: POST /booking
        """
        url = f"{self.BASE_URL}/booking"
        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": checkin,
                "checkout": checkout
            },
            "additionalneeds": additionalneeds
        }
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        if response.status_code == 200:
            response_data = response.json()
            self.booking_id = response_data.get("bookingid")
            return {
                "status_code": response.status_code,
                "booking_id": self.booking_id,
                "booking": response_data.get("booking"),
                "response_time": self.response_time
            }
        return {
            "status_code": response.status_code,
            "error": response.text,
            "response_time": self.response_time
        }

    def retrieve_booking(self, booking_id=None):
        """
        Retrieve a specific booking by ID
        Endpoint: GET /booking/{id}
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "booking": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None,
            "response_time": self.response_time
        }

    def update_booking(self, booking_id=None, firstname="Jane", lastname="Smith",
                       totalprice=200, depositpaid=False, checkin="2024-02-01",
                       checkout="2024-02-05", additionalneeds="Lunch"):
        """
        Full update of a booking (PUT)
        Endpoint: PUT /booking/{id}
        Requires: Valid auth token
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": checkin,
                "checkout": checkout
            },
            "additionalneeds": additionalneeds
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if self.auth_token:
            headers["Cookie"] = f"token={self.auth_token}"

        start_time = time.time()
        response = requests.put(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "booking": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None,
            "response_time": self.response_time
        }

    def partial_update_booking(self, booking_id=None, firstname="Jack", totalprice=150):
        """
        Partial update of a booking (PATCH)
        Endpoint: PATCH /booking/{id}
        Requires: Valid auth token
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        payload = {
            "firstname": firstname,
            "totalprice": totalprice
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if self.auth_token:
            headers["Cookie"] = f"token={self.auth_token}"

        start_time = time.time()
        response = requests.patch(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "booking": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None,
            "response_time": self.response_time
        }

    def delete_booking(self, booking_id=None, token=None):
        """
        Delete a booking
        Endpoint: DELETE /booking/{id}
        Requires: Valid auth token
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        headers = {"Content-Type": "application/json"}

        if token:
            headers["Cookie"] = f"token={token}"
        elif self.auth_token:
            headers["Cookie"] = f"token={self.auth_token}"

        start_time = time.time()
        response = requests.delete(url, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "message": response.text if response.status_code == 201 else None,
            "error": response.text if response.status_code not in [201, 204] else None,
            "response_time": self.response_time
        }

    def verify_booking_deleted(self, booking_id=None):
        """
        Verify that a booking has been deleted by trying to retrieve it
        Endpoint: GET /booking/{id}
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "is_deleted": response.status_code == 404,
            "error": response.text if response.status_code == 404 else None,
            "response_time": self.response_time
        }

    # ==================== NEGATIVE SCENARIOS ====================

    def update_without_token(self, booking_id=None, firstname="Unauthorized"):
        """
        Attempt to update booking without authentication token
        Endpoint: PUT /booking/{id}
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        payload = {
            "firstname": firstname,
            "lastname": "Test",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-05"
            }
        }
        headers = {"Content-Type": "application/json"}

        start_time = time.time()
        response = requests.put(url, json=payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "error": response.text,
            "response_time": self.response_time
        }

    def delete_with_invalid_token(self, booking_id=None, invalid_token="invalid_token_xyz"):
        """
        Attempt to delete booking with invalid token
        Endpoint: DELETE /booking/{id}
        """
        if booking_id is None:
            booking_id = self.booking_id

        url = f"{self.BASE_URL}/booking/{booking_id}"
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={invalid_token}"
        }

        start_time = time.time()
        response = requests.delete(url, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "error": response.text,
            "response_time": self.response_time
        }

    def invalid_json_payload(self):
        """
        Send invalid JSON payload to create booking
        Endpoint: POST /booking
        """
        url = f"{self.BASE_URL}/booking"
        headers = {"Content-Type": "application/json"}

        # Intentionally invalid JSON structure
        invalid_payload = {
            "firstname": "John"
            # Missing required fields
        }

        start_time = time.time()
        response = requests.post(url, json=invalid_payload, headers=headers, timeout=self.TIMEOUT)
        self.response_time = time.time() - start_time

        self.last_response = response
        # log response details
        self._log_response(url, response)

        return {
            "status_code": response.status_code,
            "error": response.text,
            "response_time": self.response_time
        }

    def validate_status_code(self, expected_code):
        """
        Validate the status code of the last response
        """
        if self.last_response:
            return {
                "expected": expected_code,
                "actual": self.last_response.status_code,
                "is_valid": self.last_response.status_code == expected_code
            }
        return None

    def validate_response_time(self, max_time_ms=5000):
        """
        Validate response time is within acceptable limits
        """
        if self.response_time:
            response_ms = self.response_time * 1000
            return {
                "response_time_ms": response_ms,
                "max_time_ms": max_time_ms,
                "is_within_limit": response_ms <= max_time_ms
            }
        return None

    def get_last_response(self):
        """Get the last response object"""
        return self.last_response

    def get_response_json(self):
        """Get JSON from last response"""
        if self.last_response and self.last_response.status_code == 200:
            return self.last_response.json()
        return None

    def _log_response(self, url, response):
        """Internal helper to log request/response details to file"""
        try:
            body = response.text
        except Exception:
            body = '<unable to read body>'
        logger.debug(f"URL: {url} | Status: {response.status_code} | Body: {body}")

    def reset(self):
        """Reset the API client state"""
        self.auth_token = None
        self.booking_id = None
        self.response_time = None
        self.last_response = None
