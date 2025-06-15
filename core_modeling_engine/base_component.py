class ModelingComponent:
    """
    Base class for all components in the modeling engine.
    """
    def __init__(self, *args, **kwargs):
        # Allow for flexible initialization of components
        pass

    def process(self, data):
        """
        Process the given data.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the 'process' method.")

    def get_name(self):
        """
        Returns the name of the component.
        By default, it's the class name.
        """
        return self.__class__.__name__
