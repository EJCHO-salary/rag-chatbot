import pytest
from unittest.mock import patch, MagicMock
from ragchat.llm import LLMInterface

@patch('ragchat.llm.completion')
@patch('ragchat.llm.config')
def test_generate_response(mock_config, mock_completion):
    # Setup mocks
    mock_config.LLM_MODEL = "gemini/gemini-1.5-flash"
    mock_config.GEMINI_API_KEY = "test-key"
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_completion.return_value = mock_response
    
    # Initialize LLMInterface
    llm = LLMInterface()
    
    # Call generate_response
    context = "This is context"
    user_message = "This is a question"
    response = llm.generate_response(context, user_message)
    
    # Assertions
    assert response == "Test response"
    mock_completion.assert_called_once()
    
    # Check that it's called with the correct arguments
    args, kwargs = mock_completion.call_args
    assert kwargs['model'] == "gemini/gemini-1.5-flash"
    assert kwargs['api_key'] == "test-key"
    assert kwargs['messages'][0]['role'] == "system"
    assert context in kwargs['messages'][0]['content']
    assert kwargs['messages'][1]['content'] == user_message
