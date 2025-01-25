import pytest
from src.modules.emails.logic.render_template import render_template

def test_render_template_success():
    """
    Test rendering a template with valid placeholders in the context.
    """
    template = "Hello {name}, welcome to {platform}!"
    context = {"name": "Test Name", "platform": "OpenAI"}
    expected_result = "Hello Test Name, welcome to OpenAI!"
    
    result = render_template(template, context)
    assert result == expected_result

def test_render_template_missing_placeholder():
    """
    Test rendering a template with a missing placeholder in the context.
    """
    template = "Hello {name}, welcome to {platform}!"
    context = {"name": "Test Name"}
    
    with pytest.raises(ValueError) as exc_info:
        render_template(template, context)
    
    assert "Missing placeholder in context" in str(exc_info.value)

def test_render_template_empty_template():
    """
    Test rendering an empty template.
    """
    template = ""
    context = {"name": "Test Name"}
    expected_result = ""
    
    result = render_template(template, context)
    assert result == expected_result

def test_render_template_empty_context():
    """
    Test rendering a template with an empty context.
    """
    template = "Hello {name}, welcome to {platform}!"
    context = {}
    
    with pytest.raises(ValueError) as exc_info:
        render_template(template, context)
    
    assert "Missing placeholder in context" in str(exc_info.value)

def test_render_template_no_placeholders():
    """
    Test rendering a template without any placeholders.
    """
    template = "Hello World!"
    context = {"name": "Test Name"}
    expected_result = "Hello World!"
    
    result = render_template(template, context)
    assert result == expected_result
