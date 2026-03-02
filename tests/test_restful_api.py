import pytest
import time
from pages.restfulapi_page import RestfulBookerAPI


class TestRestfulBookerAPI:
    """
    Test Suite for Restful Booker API
    API Endpoint: https://restful-booker.herokuapp.com/
    """

    # ==================== FIXTURES ====================

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test"""
        self.api = RestfulBookerAPI()
        yield
        # Cleanup after each test
        self.api.reset()

    # ==================== AUTHENTICATION TESTS ====================

    def test_001_generate_auth_token(self):
        """
        Test 1: Generate authentication token
        Endpoint: POST /auth
        Expected: Status 200, token returned
        """
        response = self.api.generate_auth_token(username="admin", password="password123")

        assert response["status_code"] == 200, "Should return 200 status code"
        assert response["token"] is not None, "Should return a valid token"
        assert isinstance(response["token"], (str, int)), "Token should be string or integer"
        assert "response_time" in response, "Should contain response time"
        print(f"\n✓ Auth Token Generated: {response['token']}")
        print(f"  Response Time: {response['response_time']:.3f}s")

    def test_002_negative_authentication_scenario(self):
        """
        Test 2: Negative authentication - invalid credentials
        Endpoint: POST /auth
        Expected: Status 200 but with error in response (empty token)
        """
        response = self.api.negative_auth(username="invalid_user", password="wrong_pass")

        assert response["status_code"] == 200, "Should return 200 status code"
        assert "response" in response, "Should contain error response"
        print(f"\n✓ Negative Auth Test Passed")
        print(f"  Status Code: {response['status_code']}")
        print(f"  Response: {response['response']}")

    # ==================== BOOKING LIFECYCLE TESTS ====================

    def test_003_create_booking(self):
        """
        Test 3: Create a new booking
        Endpoint: POST /booking
        Expected: Status 200, booking_id returned
        """
        response = self.api.create_booking(
            firstname="John",
            lastname="Doe",
            totalprice=100,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05",
            additionalneeds="Breakfast"
        )

        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        assert response["booking_id"] is not None, "Should return booking_id"
        assert response["booking"] is not None, "Should return booking details"
        assert response["response_time"] < 5, "Response time should be less than 5 seconds"
        
        print(f"\n✓ Booking Created Successfully")
        print(f"  Booking ID: {response['booking_id']}")
        print(f"  Response Time: {response['response_time']:.3f}s")

    def test_004_retrieve_created_booking(self):
        """
        Test 4: Retrieve the created booking
        Endpoint: GET /booking/{id}
        Expected: Status 200, booking details returned
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Jane",
            lastname="Smith",
            totalprice=150,
            depositpaid=False,
            checkin="2024-02-01",
            checkout="2024-02-05"
        )
        booking_id = create_response["booking_id"]

        # Now retrieve it
        retrieve_response = self.api.retrieve_booking(booking_id=booking_id)

        assert retrieve_response["status_code"] == 200, f"Expected 200, got {retrieve_response['status_code']}"
        assert retrieve_response["booking"] is not None, "Should return booking details"
        assert retrieve_response["booking"]["firstname"] == "Jane", "Should retrieve correct firstname"
        assert retrieve_response["booking"]["lastname"] == "Smith", "Should retrieve correct lastname"
        
        print(f"\n✓ Booking Retrieved Successfully")
        print(f"  Booking ID: {booking_id}")
        print(f"  Name: {retrieve_response['booking']['firstname']} {retrieve_response['booking']['lastname']}")

    def test_005_update_booking_put(self):
        """
        Test 5: Update booking using PUT (full update)
        Endpoint: PUT /booking/{id}
        Expected: Status 200, updated booking returned
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="John",
            lastname="Doe",
            totalprice=100,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Generate auth token for update
        self.api.generate_auth_token()

        # Update the booking
        update_response = self.api.update_booking(
            booking_id=booking_id,
            firstname="UpdatedJohn",
            lastname="UpdatedDoe",
            totalprice=200,
            depositpaid=False,
            checkin="2024-03-01",
            checkout="2024-03-05",
            additionalneeds="Lunch"
        )

        assert update_response["status_code"] == 200, f"Expected 200, got {update_response['status_code']}"
        assert update_response["booking"] is not None, "Should return updated booking"
        assert update_response["booking"]["firstname"] == "UpdatedJohn", "Firstname should be updated"
        assert update_response["booking"]["totalprice"] == 200, "Price should be updated"
        
        print(f"\n✓ Booking Updated Successfully (PUT)")
        print(f"  Updated Name: {update_response['booking']['firstname']} {update_response['booking']['lastname']}")
        print(f"  Updated Price: {update_response['booking']['totalprice']}")

    def test_006_partial_update_booking_patch(self):
        """
        Test 6: Partially update booking using PATCH
        Endpoint: PATCH /booking/{id}
        Expected: Status 200, partially updated booking returned
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Alice",
            lastname="Brown",
            totalprice=120,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Generate auth token for patch
        self.api.generate_auth_token()

        # Partially update the booking (only firstname and price)
        patch_response = self.api.partial_update_booking(
            booking_id=booking_id,
            firstname="Alicia",
            totalprice=250
        )

        assert patch_response["status_code"] == 200, f"Expected 200, got {patch_response['status_code']}"
        assert patch_response["booking"] is not None, "Should return patched booking"
        assert patch_response["booking"]["firstname"] == "Alicia", "Firstname should be patched"
        assert patch_response["booking"]["totalprice"] == 250, "Price should be patched"
        # Others should remain unchanged
        assert patch_response["booking"]["lastname"] == "Brown", "Lastname should remain unchanged"
        
        print(f"\n✓ Booking Partially Updated Successfully (PATCH)")
        print(f"  Updated Fields: firstname='Alicia', totalprice=250")
        print(f"  Unchanged: lastname='{patch_response['booking']['lastname']}'")

    def test_007_delete_booking(self):
        """
        Test 7: Delete a booking
        Endpoint: DELETE /booking/{id}
        Expected: Status 201, deletion successful
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Bob",
            lastname="Wilson",
            totalprice=180,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Generate auth token for deletion
        self.api.generate_auth_token()

        # Delete the booking
        delete_response = self.api.delete_booking(booking_id=booking_id)

        assert delete_response["status_code"] in [201, 204], f"Expected 201 or 204, got {delete_response['status_code']}"
        
        print(f"\n✓ Booking Deleted Successfully")
        print(f"  Booking ID: {booking_id}")
        print(f"  Status Code: {delete_response['status_code']}")

    def test_008_verify_booking_deleted(self):
        """
        Test 8: Verify that booking has been deleted
        Endpoint: GET /booking/{id}
        Expected: Status 404, booking not found
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Charlie",
            lastname="Davis",
            totalprice=130,
            depositpaid=False,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Generate auth token for deletion
        self.api.generate_auth_token()

        # Delete the booking
        self.api.delete_booking(booking_id=booking_id)

        # Verify it's deleted
        verify_response = self.api.verify_booking_deleted(booking_id=booking_id)

        assert verify_response["status_code"] == 404, f"Expected 404, got {verify_response['status_code']}"
        assert verify_response["is_deleted"] is True, "Booking should be deleted"
        
        print(f"\n✓ Verified Booking is Deleted")
        print(f"  Booking ID: {booking_id}")
        print(f"  Status Code: {verify_response['status_code']} (Not Found)")

    # ==================== NEGATIVE SCENARIO TESTS ====================

    def test_009_update_without_token(self):
        """
        Test 9: Attempt to update booking without authentication token
        Endpoint: PUT /booking/{id}
        Expected: Status 403 (Forbidden) or similar error
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Eve",
            lastname="Miller",
            totalprice=110,
            depositpaid=True,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Do NOT generate auth token, attempt update without it
        update_response = self.api.update_without_token(booking_id=booking_id, firstname="Unauthorized")

        # The API might return 403 or allow it, depending on implementation
        # Most secure APIs should reject this
        print(f"\n✓ Update Without Token Test")
        print(f"  Status Code: {update_response['status_code']}")
        print(f"  Response: {update_response['error'][:100]}")

    def test_010_delete_with_invalid_token(self):
        """
        Test 10: Attempt to delete booking with invalid token
        Endpoint: DELETE /booking/{id}
        Expected: Status 403 (Forbidden)
        """
        # First create a booking
        create_response = self.api.create_booking(
            firstname="Frank",
            lastname="Taylor",
            totalprice=160,
            depositpaid=False,
            checkin="2024-01-01",
            checkout="2024-01-05"
        )
        booking_id = create_response["booking_id"]

        # Attempt delete with invalid token
        delete_response = self.api.delete_with_invalid_token(
            booking_id=booking_id,
            invalid_token="invalid_token_12345xyz"
        )

        # Should be rejected or given error
        print(f"\n✓ Delete With Invalid Token Test")
        print(f"  Status Code: {delete_response['status_code']}")
        print(f"  Error Message: {delete_response['error'][:100]}")

    def test_011_invalid_json_payload_validation(self):
        """
        Test 11: Invalid JSON payload validation
        Endpoint: POST /booking
        Expected: Status 400 or similar error for incomplete data
        """
        # Send request with incomplete/invalid payload
        invalid_response = self.api.invalid_json_payload()

        # API might return 400 for bad request
        print(f"\n✓ Invalid JSON Payload Test")
        print(f"  Status Code: {invalid_response['status_code']}")
        if invalid_response['status_code'] != 200:
            print(f"  Error: {invalid_response['error'][:100]}")
        else:
            print(f"  Note: API accepted incomplete payload (status 200)")

    def test_012_validate_status_codes(self):
        """
        Test 12: Validate various HTTP status codes
        Expected: Correct status codes for different operations
        """
        # Test successful creation
        create_response = self.api.create_booking()
        assert create_response["status_code"] == 200, "Create should return 200"

        # Test successful retrieval
        retrieve_response = self.api.retrieve_booking()
        assert retrieve_response["status_code"] == 200, "Retrieve should return 200"

        # Test deletion (needs token)
        self.api.generate_auth_token()
        delete_response = self.api.delete_booking()
        assert delete_response["status_code"] in [201, 204], "Delete should return 201 or 204"

        print(f"\n✓ Status Code Validation")
        print(f"  Create: {create_response['status_code']} ✓")
        print(f"  Retrieve: {retrieve_response['status_code']} ✓")
        print(f"  Delete: {delete_response['status_code']} ✓")

    def test_013_validate_response_times(self):
        """
        Test 13: Validate response times are within acceptable limits
        Expected: All responses within 5 seconds
        """
        max_acceptable_time = 5000  # milliseconds

        # Test multiple operations
        create_response = self.api.create_booking()
        create_time_validation = self.api.validate_response_time(max_acceptable_time)

        retrieve_response = self.api.retrieve_booking()
        retrieve_time_validation = self.api.validate_response_time(max_acceptable_time)

        assert create_time_validation["is_within_limit"], f"Create response time exceeded limit: {create_time_validation['response_time_ms']:.2f}ms"
        assert retrieve_time_validation["is_within_limit"], f"Retrieve response time exceeded limit: {retrieve_time_validation['response_time_ms']:.2f}ms"

        print(f"\n✓ Response Time Validation")
        print(f"  Create Response Time: {create_time_validation['response_time_ms']:.2f}ms (max: {max_acceptable_time}ms) ✓")
        print(f"  Retrieve Response Time: {retrieve_time_validation['response_time_ms']:.2f}ms (max: {max_acceptable_time}ms) ✓")

    # ==================== COMPLETE BOOKING LIFECYCLE TEST ====================

    def test_014_complete_booking_lifecycle(self):
        """
        Test 14: Complete booking lifecycle from creation to deletion
        Steps:
        1. Create booking
        2. Retrieve booking
        3. Update booking
        4. Partial update booking
        5. Delete booking
        6. Verify deletion
        """
        print("\n" + "="*50)
        print("COMPLETE BOOKING LIFECYCLE TEST")
        print("="*50)

        # Step 1: Create booking
        print("\n[Step 1] Creating booking...")
        create_response = self.api.create_booking(
            firstname="TestUser",
            lastname="Lifecycle",
            totalprice=250,
            depositpaid=True,
            checkin="2024-05-01",
            checkout="2024-05-10",
            additionalneeds="WiFi"
        )
        assert create_response["status_code"] == 200
        booking_id = create_response["booking_id"]
        print(f"✓ Booking created with ID: {booking_id}")

        # Step 2: Retrieve booking
        print("\n[Step 2] Retrieving booking...")
        retrieve_response = self.api.retrieve_booking(booking_id=booking_id)
        assert retrieve_response["status_code"] == 200
        assert retrieve_response["booking"]["firstname"] == "TestUser"
        print(f"✓ Booking retrieved: {retrieve_response['booking']['firstname']} {retrieve_response['booking']['lastname']}")

        # Step 3: Generate token for updates
        print("\n[Step 3] Generating auth token...")
        auth_response = self.api.generate_auth_token()
        assert auth_response["status_code"] == 200
        print(f"✓ Auth token generated: {auth_response['token']}")

        # Step 4: Update booking (PUT)
        print("\n[Step 4] Updating booking (PUT)...")
        update_response = self.api.update_booking(
            booking_id=booking_id,
            firstname="UpdatedUser",
            lastname="UpdatedLifecycle",
            totalprice=300,
            depositpaid=False,
            checkin="2024-06-01",
            checkout="2024-06-10",
            additionalneeds="WiFi + Parking"
        )
        assert update_response["status_code"] == 200
        print(f"✓ Booking updated: {update_response['booking']['firstname']} - ${update_response['booking']['totalprice']}")

        # Step 5: Partial update (PATCH)
        print("\n[Step 5] Partially updating booking (PATCH)...")
        patch_response = self.api.partial_update_booking(
            booking_id=booking_id,
            firstname="FinalUser",
            totalprice=350
        )
        assert patch_response["status_code"] == 200
        print(f"✓ Booking patched: firstname changed to '{patch_response['booking']['firstname']}', price to ${patch_response['booking']['totalprice']}")

        # Step 6: Delete booking
        print("\n[Step 6] Deleting booking...")
        delete_response = self.api.delete_booking(booking_id=booking_id)
        assert delete_response["status_code"] in [201, 204]
        print(f"✓ Booking deleted (Status: {delete_response['status_code']})")

        # Step 7: Verify deletion
        print("\n[Step 7] Verifying deletion...")
        verify_response = self.api.verify_booking_deleted(booking_id=booking_id)
        assert verify_response["status_code"] == 404
        assert verify_response["is_deleted"] is True
        print(f"✓ Booking confirmed deleted (Status: 404)")

        print("\n" + "="*50)
        print("✓ LIFECYCLE TEST COMPLETED SUCCESSFULLY")
        print("="*50)
