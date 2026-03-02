# Restful Booker API Automation Tests

## Overview
This project contains comprehensive API automation tests for the **Restful Booker API** using Python, `requests` library, and `pytest`.

**API Endpoint:** https://restful-booker.herokuapp.com/

## Project Structure

```
pages/
├── restfulapi_page.py          # Page Object for API interactions
├── sauce_pages.py              # UI test pages (existing)
└── ...

tests/
├── test_restful_api.py         # API test cases
├── test_sauce.py               # UI test cases (existing)
└── ...
```

## Test Coverage

### 1. Authentication Tests (2 tests)
- **test_001_generate_auth_token**: Generate valid authentication token
- **test_002_negative_authentication_scenario**: Test with invalid credentials

### 2. Booking Lifecycle Tests (6 tests)
- **test_003_create_booking**: Create a new booking
- **test_004_retrieve_created_booking**: Retrieve booking by ID
- **test_005_update_booking_put**: Full booking update (PUT)
- **test_006_partial_update_booking_patch**: Partial booking update (PATCH)
- **test_007_delete_booking**: Delete a booking
- **test_008_verify_booking_deleted**: Verify booking deletion (404 response)

### 3. Negative Scenario Tests (3 tests)
- **test_009_update_without_token**: Attempt update without auth token
- **test_010_delete_with_invalid_token**: Attempt delete with invalid token
- **test_011_invalid_json_payload_validation**: Invalid JSON payload handling

### 4. Response Validation Tests (3 tests)
- **test_012_validate_status_codes**: Verify correct HTTP status codes
- **test_013_validate_response_times**: Verify response time < 5 seconds
- **test_014_complete_booking_lifecycle**: End-to-end booking lifecycle test

## Installation

### Prerequisites
- Python 3.7+
- Virtual environment (already created: `playwright-env`)
- pip

### Activate Virtual Environment
```bash
source playwright-env/bin/activate
```

### Install Dependencies
```bash
pip install requests pytest
```

Dependencies should already be installed in the virtual environment.

## API Methods Available

### RestfulBookerAPI Class

#### Authentication Methods
- `generate_auth_token(username, password)` - Generate auth token
- `negative_auth(username, password)` - Test invalid credentials

#### Booking CRUD Operations
- `create_booking(firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)`
- `retrieve_booking(booking_id)`
- `update_booking(booking_id, firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)`
- `partial_update_booking(booking_id, firstname, totalprice)`
- `delete_booking(booking_id, token)`
- `verify_booking_deleted(booking_id)`

#### Negative Test Methods
- `update_without_token(booking_id, firstname)`
- `delete_with_invalid_token(booking_id, invalid_token)`
- `invalid_json_payload()`

#### Validation Methods
- `validate_status_code(expected_code)`
- `validate_response_time(max_time_ms)`
- `get_last_response()`
- `get_response_json()`
- `reset()`

## Running Tests

### Run All Tests
```bash
cd /home/tajul/Documents/Playwright_Task_SQA
source playwright-env/bin/activate
pytest tests/test_restful_api.py -v
```

### Run Specific Test
```bash
pytest tests/test_restful_api.py::TestRestfulBookerAPI::test_001_generate_auth_token -v
```

### Run with Output
```bash
pytest tests/test_restful_api.py -v -s
```

### Run with Allure Report
```bash
pytest tests/test_restful_api.py --alluredir=allure-results
allure serve allure-results
```

### Run Only Authentication Tests
```bash
pytest tests/test_restful_api.py -k "auth" -v
```

### Run Only Negative Tests
```bash
pytest tests/test_restful_api.py -k "negative or invalid or without_token or invalid_token" -v
```

### Run Complete Lifecycle Test
```bash
pytest tests/test_restful_api.py::TestRestfulBookerAPI::test_014_complete_booking_lifecycle -v -s
```

## Test Scenarios

### Authentication
```
✓ Test valid credentials return auth token
✓ Test invalid credentials are handled properly
```

### Booking Lifecycle
```
✓ Create booking
✓ Retrieve booking by ID
✓ Update entire booking (PUT)
✓ Partially update booking (PATCH)
✓ Delete booking
✓ Verify booking deletion (404)
```

### Negative Scenarios
```
✓ Update booking without authentication token
✓ Delete booking with invalid token
✓ Submit incomplete/invalid JSON payload
```

### Response Validation
```
✓ Validate HTTP status codes (200, 201, 204, 404, 403)
✓ Validate response times (< 5 seconds)
✓ End-to-end lifecycle flow
```

## API Credentials

**Default Credentials:**
- Username: `admin`
- Password: `password123`

## Expected Status Codes

| Operation | Status Code | Notes |
|-----------|-------------|-------|
| Create Booking | 200 | Success |
| Get Booking | 200 | Success |
| Update Booking (PUT) | 200 | Success (requires token) |
| Partial Update (PATCH) | 200 | Success (requires token) |
| Delete Booking | 201 or 204 | Success (requires token) |
| Get Deleted Booking | 404 | Not Found |
| Invalid Auth | 403 | Forbidden |
| Bad Request | 400 | Bad Request |

## Response Time Standards

- Create Booking: < 5 seconds
- Retrieve Booking: < 5 seconds
- Update Booking: < 5 seconds
- Delete Booking: < 5 seconds

## Features

✨ **Page Object Model**: Clean, maintainable API class structure

✨ **Comprehensive Coverage**: 14+ test cases covering positive and negative scenarios

✨ **Response Time Validation**: Performance testing included

✨ **Token Management**: Built-in auth token generation and management

✨ **Error Handling**: Detailed error messages and responses

✨ **Pytest Integration**: Fully compatible with pytest, Allure reporting, and CI/CD

## Example Usage

```python
from pages.restfulapi_page import RestfulBookerAPI

# Initialize API client
api = RestfulBookerAPI()

# Generate auth token
auth = api.generate_auth_token()
token = auth["token"]

# Create a booking
booking = api.create_booking(
    firstname="John",
    lastname="Doe",
    totalprice=100,
    depositpaid=True,
    checkin="2024-01-01",
    checkout="2024-01-05"
)
booking_id = booking["booking_id"]

# Retrieve the booking
retrieved = api.retrieve_booking(booking_id)
print(retrieved["booking"])

# Update booking
updated = api.update_booking(
    booking_id=booking_id,
    firstname="Jane",
    lastname="Smith"
)

# Delete booking
deleted = api.delete_booking(booking_id)

# Verify deletion
verification = api.verify_booking_deleted(booking_id)
assert verification["is_deleted"] == True
```

## Troubleshooting

### Issue: `requests` module not found
**Solution:** Install requests
```bash
pip install requests
```

### Issue: Tests can't connect to API
**Solution:** Verify internet connection and API availability
```bash
curl https://restful-booker.herokuapp.com/ping
```

### Issue: Token validation fails
**Solution:** Use default credentials (admin/password123) or verify API is accepting credentials

### Issue: Response time validation fails
**Solution:** Check network conditions, the API may be slow. Adjust timeout in `RestfulBookerAPI.TIMEOUT`

## Notes

- All booking IDs are stored in `self.booking_id` after creation
- Auth token is stored in `self.auth_token` after generation
- Response time is tracked in `self.response_time`
- Each test has automatic cleanup via pytest fixtures
- Tests are independent and can run in any order

## Running in CI/CD

Example for GitHub Actions or similar CI tools:

```yaml
- name: Run API Tests
  run: |
    cd /home/tajul/Documents/Playwright_Task_SQA
    source playwright-env/bin/activate
    pytest tests/test_restful_api.py -v --tb=short
```

## Additional Resources

- **Restful Booker API Docs**: https://restful-booker.herokuapp.com/apidoc/index.html
- **Pytest Documentation**: https://docs.pytest.org/
- **Requests Library Docs**: https://requests.readthedocs.io/
- **REST API Best Practices**: https://www.restfulapi.net/

---

**Last Updated**: March 2, 2026
**Status**: ✓ Ready for Testing
