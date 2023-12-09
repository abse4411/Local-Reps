
init -1:
    python hide:
        config.developer = True
# Note: Run after define statements of font in gui.py
init offset = 999999
# Make font vars dynamic since Ren’Py 6.99.14
define gui.text_font = gui.preference("projz_gui_text_font", gui.text_font)
define gui.name_text_font = gui.preference("projz_gui_name_text_font", gui.name_text_font)
define gui.interface_text_font = gui.preference("projz_gui_interface_text_font", gui.interface_text_font)
define gui.button_text_font = gui.preference("projz_gui_button_text_font", gui.button_text_font)
define gui.choice_button_text_font = gui.preference("projz_gui_choice_button_text_font", gui.choice_button_text_font)

init python:
    def projz_change_font(font):
        persistent.projz_gui_selected_font = font
        renpy.save_persistent()
    def show_i18n_settings():
        renpy.show_screen('i18n_settings')
    config.underlay[0].keymap['show_i18n_settings'] = show_i18n_settings
    config.keymap['show_i18n_settings'] = ['ctrl_K_i']

screen i18n_settings:
    ## Ensure other screens do not get input while this screen is displayed.
    modal True
    zorder 999999
    key "mouseup_3" action Hide('i18n_settings')

    python:
        # save default fonts
        from store import persistent
        if persistent.projz_gui_selected_font is None:
            persistent.projz_gui_selected_font = gui.text_font
        if persistent.projz_gui_text_font is None:
            persistent.projz_gui_text_font = gui.text_font
        if persistent.projz_gui_name_text_font is None:
            persistent.projz_gui_name_text_font = gui.name_text_font
        if persistent.projz_gui_interface_text_font is None:
            persistent.projz_gui_interface_text_font = gui.interface_text_font
        if persistent.projz_gui_button_text_font is None:
            persistent.projz_gui_button_text_font = gui.button_text_font
        if persistent.projz_gui_choice_button_text_font is None:
            persistent.projz_gui_choice_button_text_font = gui.choice_button_text_font
        renpy.save_persistent()
    frame:
        yalign 0.5
        xalign 0.5
        vbox:
            label "I18n Settings"
            text _("text_font: [gui.text_font]")
            text _("name_text_font: [gui.name_text_font]")
            text _("interface_text_font: [gui.interface_text_font]")
            text _("button_text_font: [gui.button_text_font]")
            text _("choice_button_text_font: [gui.choice_button_text_font]")
            text _("language: [_preferences.language]")
            text _("This plugin is injected by the {a=https://github.com/abse4411/projz_renpy_translation}project{/a}.")
            hbox:
                box_wrap True
                vbox:
                    style_prefix "radio"
                    label _("Language")
                    textbutton "Default" text_font "DejaVuSans.ttf" action [Language(None)]
                    textbutton "한국어" text_font "SourceHanSansLite.ttf" action [Language("korean")]
                    textbutton "Русский" text_font "DejaVuSans.ttf" action [Language("french")]
                    textbutton "日本語" text_font "SourceHanSansLite.ttf" action [Language("japanese")]
                    textbutton "简体中文" text_font "SourceHanSansLite.ttf" action [Language("chinese")]
                vbox:
                    style_prefix "radio"
                    label _("Font")
                    textbutton "Default" action [gui.SetPreference("projz_gui_text_font", persistent.projz_gui_text_font, rebuild=False), gui.SetPreference("projz_gui_name_text_font", persistent.projz_gui_name_text_font, rebuild=False), gui.SetPreference("projz_gui_interface_text_font", persistent.projz_gui_interface_text_font, rebuild=False), gui.SetPreference("projz_gui_button_text_font", persistent.projz_gui_button_text_font, rebuild=False), gui.SetPreference("projz_gui_choice_button_text_font", persistent.projz_gui_choice_button_text_font, rebuild=True)]
                    textbutton "DejaVuSans.ttf" text_font "DejaVuSans.ttf" action [Function(projz_change_font, "DejaVuSans.ttf"), gui.SetPreference("projz_gui_text_font", "DejaVuSans.ttf", rebuild=False), gui.SetPreference("projz_gui_name_text_font", "DejaVuSans.ttf", rebuild=False), gui.SetPreference("projz_gui_interface_text_font", "DejaVuSans.ttf", rebuild=False), gui.SetPreference("projz_gui_button_text_font", "DejaVuSans.ttf", rebuild=False), gui.SetPreference("projz_gui_choice_button_text_font", "DejaVuSans.ttf", rebuild=True)]
                    textbutton "KMKDSP.ttf" text_font "KMKDSP.ttf" action [Function(projz_change_font, "KMKDSP.ttf"), gui.SetPreference("projz_gui_text_font", "KMKDSP.ttf", rebuild=False), gui.SetPreference("projz_gui_name_text_font", "KMKDSP.ttf", rebuild=False), gui.SetPreference("projz_gui_interface_text_font", "KMKDSP.ttf", rebuild=False), gui.SetPreference("projz_gui_button_text_font", "KMKDSP.ttf", rebuild=False), gui.SetPreference("projz_gui_choice_button_text_font", "KMKDSP.ttf", rebuild=True)]
                    textbutton "SourceHanSansLite.ttf" text_font "SourceHanSansLite.ttf" action [Function(projz_change_font, "SourceHanSansLite.ttf"), gui.SetPreference("projz_gui_text_font", "SourceHanSansLite.ttf", rebuild=False), gui.SetPreference("projz_gui_name_text_font", "SourceHanSansLite.ttf", rebuild=False), gui.SetPreference("projz_gui_interface_text_font", "SourceHanSansLite.ttf", rebuild=False), gui.SetPreference("projz_gui_button_text_font", "SourceHanSansLite.ttf", rebuild=False), gui.SetPreference("projz_gui_choice_button_text_font", "SourceHanSansLite.ttf", rebuild=True)]
            spacing 20
            textbutton _("Hide"):
                xalign 1.0
                action Hide("i18n_settings")
