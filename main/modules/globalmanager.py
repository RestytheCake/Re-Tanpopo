class GlobalManager:
    _instance = None
    animeviewer_instance = None
    bottom_frame_instance = None
    top_frame_instance = None
    settings_window_instance = None
    details_frame_instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_animeviewer_instance(cls):
        return cls.animeviewer_instance

    @classmethod
    def set_animeviewer_instance(cls, AnimeViewer_instance):
        cls.animeviewer_instance = AnimeViewer_instance

    @classmethod
    def get_bottom_frame_instance(cls):
        return cls.bottom_frame_instance

    @classmethod
    def set_bottom_frame_instance(cls, instance):
        cls.bottom_frame_instance = instance

    @classmethod
    def get_top_frame_instance(cls):
        return cls.top_frame_instance

    @classmethod
    def set_top_frame_instance(cls, instance):
        cls.top_frame_instance = instance

    @classmethod
    def get_settings_window_instance(cls):
        return cls.settings_window_instance

    @classmethod
    def set_settings_window_instance(cls, instance):
        cls.settings_window_instance = instance

    @classmethod
    def get_details_frame_instance(cls):
        return cls.details_frame_instance

    @classmethod
    def set_details_frame_instance(cls, instance):
        cls.details_frame_instance = instance