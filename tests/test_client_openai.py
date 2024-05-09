"""
Tests for cryorithm/clients/openai.py
"""

import pytest

from cryorithm.clients.openai import OpenAIClientWrapper  # Assuming this is the path

def test_openai_client_init_with_key():
  """Test OpenAI client initialization with a provided API key"""
  api_key = "YOUR_API_KEY"  # Replace with your actual API key
  client = OpenAIClientWrapper(api_key=api_key)
  assert isinstance(client, OpenAIClientWrapper)  # Check if the object is of the expected class

# TODO: Fix/improve this test, or just drop it.
#def test_openai_client_init_no_key():
#    """Test OpenAI client initialization without a valid API key"""
#    dummy_key = "INVALID_KEY"  # Placeholder key (replace with actual logic for handling missing keys)
#    with pytest.raises(ValueError):  # Expect an error since the key is invalid
#        client = OpenAIClientWrapper(api_key=dummy_key)
