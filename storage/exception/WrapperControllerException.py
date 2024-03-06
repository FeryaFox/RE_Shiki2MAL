class WrapperNotFound(Exception):
    def __init__(self, wrapper_name, wrapper_type):
        super().__init__(f"Wrapper {wrapper_name} not found!")
        self.wrapper_name = wrapper_name
        self.wrapper_type = wrapper_type
