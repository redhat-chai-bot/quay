"""
Tests for global messages API endpoints, specifically audit logging.

This tests the fix for PROJQUAY-12222: Add audit logging for global message
create/delete operations.
"""

from unittest.mock import patch

import pytest

from endpoints.api.globalmessages import GlobalUserMessage, GlobalUserMessages
from endpoints.api.test.shared import conduct_api_call
from endpoints.test.shared import client_with_identity
from test.fixtures import *


class TestGlobalMessageAuditLogging:
    """
    Tests that global message operations create appropriate audit log entries.

    This addresses PROJQUAY-12222: Creating and deleting global messages should
    produce audit log entries.
    """

    @pytest.fixture(autouse=True)
    def setup(self, app):
        """Enable required features for superuser operations."""
        import features

        features.import_features(
            {
                "FEATURE_SUPER_USERS": True,
                "FEATURE_SUPERUSERS_FULL_ACCESS": True,
            }
        )

    def test_create_global_message_logs_action(self, app):
        """
        Test that creating a global message logs the global_message_create action.
        """
        with client_with_identity("devtable", app) as cl:
            with patch("endpoints.api.globalmessages.log_action") as mock_log:
                body = {
                    "message": {
                        "severity": "warning",
                        "media_type": "text/plain",
                        "content": "Test message for audit logging",
                    }
                }
                conduct_api_call(cl, GlobalUserMessages, "POST", None, body, 201)

                mock_log.assert_called_once()
                call_args = mock_log.call_args
                assert call_args[0][0] == "global_message_create"
                assert call_args[0][1] is None
                metadata = call_args[0][2]
                assert metadata["severity"] == "warning"
                assert metadata["media_type"] == "text/plain"
                assert metadata["content"] == "Test message for audit logging"

    def test_create_global_message_metadata_fields(self, app):
        """
        Test that the metadata passed to log_action contains all expected fields.
        """
        with client_with_identity("devtable", app) as cl:
            with patch("endpoints.api.globalmessages.log_action") as mock_log:
                body = {
                    "message": {
                        "severity": "info",
                        "media_type": "text/markdown",
                        "content": "# Important update",
                    }
                }
                conduct_api_call(cl, GlobalUserMessages, "POST", None, body, 201)

                metadata = mock_log.call_args[0][2]
                assert set(metadata.keys()) == {"severity", "media_type", "content"}

    def test_delete_global_message_logs_action(self, app):
        """
        Test that deleting a global message logs the global_message_delete action.
        """
        # First create a message to get its UUID
        with client_with_identity("devtable", app) as cl:
            body = {
                "message": {
                    "severity": "info",
                    "media_type": "text/plain",
                    "content": "Message to delete",
                }
            }
            conduct_api_call(cl, GlobalUserMessages, "POST", None, body, 201)

            # Get the list of messages to find the UUID
            result = conduct_api_call(cl, GlobalUserMessages, "GET", None, None, 200).json
            messages = result["messages"]
            assert len(messages) > 0
            uuid = messages[-1]["uuid"]

            with patch("endpoints.api.globalmessages.log_action") as mock_log:
                params = {"uuid": uuid}
                conduct_api_call(cl, GlobalUserMessage, "DELETE", params, None, 204)

                mock_log.assert_called_once()
                call_args = mock_log.call_args
                assert call_args[0][0] == "global_message_delete"
                assert call_args[0][1] is None
                metadata = call_args[0][2]
                assert metadata["uuid"] == uuid
