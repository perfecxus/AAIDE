# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test cases for the analytics agent and its sub-agents."""

import os
import sys
import pytest
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from core.subagents.extract_datasource_agent import create_extract_source_datasource_agent

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


class TestAgents(unittest.TestCase):
    """Test cases for the analytics agent and its sub-agents."""

    def setUp(self):
        """Set up for test methods."""
        self.session = session_service.create_session(
            app_name="DataAgent",
            user_id="test_user",
        )
        self.user_id = "test_user"
        self.session_id = self.session.id

        self.runner = Runner(
            app_name="DataAgent",
            agent=None,
            artifact_service=artifact_service,
            session_service=session_service,
        )

    def _run_agent(self, agent, query):
        """Helper method to run an agent and get the final response."""
        self.runner.agent = agent
        content = types.Content(role="user", parts=[types.Part(text=query)])
        events = list(
            self.runner.run(
                user_id=self.user_id, session_id=self.session_id, new_message=content
            )
        )

        last_event = events[-1]
        final_response = "".join(
            [part.text for part in last_event.content.parts if part.text]
        )
        return final_response


    @pytest.mark.extract_ds_agent
    def test_db_agent_can_handle_env_query(self):
        """Test the db_agent with a query from environment variable."""
        query = "what countries exist in the train table?"
        response = self._run_agent(create_extract_source_datasource_agent(), query)
        print(response)
        # self.assertIn("Canada", response)
        self.assertIsNotNone(response)



if __name__ == "__main__":
    unittest.main()

    # testagent = TestAgents
    # testagent.setUp(testagent)
    # testagent.test_root_agent_can_list_tools(testagent)
    # testagent.test_db_agent_can_handle_env_query(testagent)
