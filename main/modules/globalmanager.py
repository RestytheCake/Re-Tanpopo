class GlobalManager:
    _instance = None
    bottom_frame_instance = None
    top_frame_instance = None
    settings_window_instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_bottom_frame_instance(cls):
        return cls.bottom_frame_instance

    @classmethod
    def set_bottom_frame_instance(cls, instance):
        cls.bottom_frame_instance = instance

    @classmethod
    def get_top_frame_instance(cls):  # Getter method for the new variable
        return cls.top_frame_instance

    @classmethod
    def set_top_frame_instance(cls, instance):  # Setter method for the new variable
        cls.top_frame_instance = instance

    @classmethod
    def get_settings_window_instance(cls):  # Getter for settings window instance
        return cls.settings_window_instance

    @classmethod
    def set_settings_window_instance(cls, instance):  # Setter for settings window instance
        cls.settings_window_instance = instance