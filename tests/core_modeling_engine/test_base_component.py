import pytest
from core_modeling_engine.base_component import ModelingComponent

def test_modeling_component_instantiation():
    """
    Tests that a ModelingComponent can be instantiated.
    """
    component = ModelingComponent()
    assert component is not None, "Component should not be None after instantiation."

def test_modeling_component_get_name():
    """
    Tests the get_name method of the ModelingComponent.
    """
    component = ModelingComponent()
    assert component.get_name() == "ModelingComponent", "Component name should be 'ModelingComponent'."

def test_modeling_component_process_raises_not_implemented():
    """
    Tests that calling process() on a base ModelingComponent raises NotImplementedError.
    """
    component = ModelingComponent()
    with pytest.raises(NotImplementedError) as excinfo:
        component.process(data="some_data")
    assert "Subclasses must implement the 'process' method." in str(excinfo.value)

class CustomComponent(ModelingComponent):
    def process(self, data):
        return f"Processed: {data}"

def test_custom_component_get_name():
    """
    Tests the get_name method of a subclass of ModelingComponent.
    """
    custom_component = CustomComponent()
    assert custom_component.get_name() == "CustomComponent", "Custom component name should be 'CustomComponent'."

def test_custom_component_process():
    """
    Tests the overridden process method of a subclass.
    """
    custom_component = CustomComponent()
    result = custom_component.process("test_data")
    assert result == "Processed: test_data"
