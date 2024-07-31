from main.gui.details.details import AnimeDetails
from main.modules.globalmanager import GlobalManager


def refresh_global():
    bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
    top_frame_instance = GlobalManager.get_top_frame_instance()
    settings_instance = GlobalManager.get_settings_window_instance()

    if bottom_frame_instance:
        bottom_frame_instance.update_settings()
    if top_frame_instance:
        top_frame_instance.update_settings()
    if settings_instance:
        settings_instance.update_settings()
    else:
        print("Refresh Frame instance is not initialized")
    print("Refresh done!")


def clear_main():
    animeviewer_instance = GlobalManager.get_animeviewer_instance()
    if animeviewer_instance:
        animeviewer_instance.clear()
    else:
        print("Clear Frame instance is not initialized")
    print("Clear done!")


def change_page_to_detail(title, desc, img, anime_id):
    animeviewer_instance = GlobalManager.get_animeviewer_instance()
    if animeviewer_instance:
        clear_main()
        animeviewer_instance.details_frame(title, desc, img, anime_id)
    else:
        print("AnimeViewer instance is not initialized")
