###########################################################
# ________  ________  ________        ___  ________       #
# |\   __  \|\   __  \|\   __  \      |\  \|\_____  \     #
# \ \  \|\  \ \  \|\  \ \  \|\  \     \ \  \\|___/  /|    #
#  \ \   ____\ \   _  _\ \  \\\  \  __ \ \  \   /  / /    #
#   \ \  \___|\ \  \\  \\ \  \\\  \|\  \\_\  \ /  /_/__   #
#    \ \__\    \ \__\\ _\\ \_______\ \________\\________\ #
#     \|__|     \|__|\|__|\|_______|\|________|\|_______| #
#                                                         #
#  This ryp file is generated by the project:             #
#  https://github.com/abse4411/projz_renpy_translation)   #
###########################################################

# Enable developer console
init -1:
    python hide:
        config.developer = True

# Names for saving current selected font by our setting
define projz_gui_selected_font = "projz_gui_selected_font"
init python:
    from store import persistent
    def projz_get(name, default_value):
        if hasattr(persistent, name) and getattr(persistent, name) is not None:
            return getattr(persistent, name)
        return default_value

    def projz_set(name, value):
        setattr(persistent, name, value)
        return value
    
    def get_selected_font(name, default_value):
        return projz_get(projz_gui_selected_font, projz_get(name, default_value))


# Names of gui font var for saving default fonts
define projz_gui_vars = ["projz_gui_text_font","projz_gui_name_text_font","projz_gui_interface_text_font","projz_gui_button_text_font","projz_gui_choice_button_text_font"]
# Note: Run after define statements of font in gui.rpy
init offset = 999999
################### Make font vars dynamic since Ren’Py 6.99.14 ###################
# define gui.text_font = gui.preference(projz_gui_vars[0], gui.text_font)
# define gui.name_text_font = gui.preference(projz_gui_vars[1], gui.name_text_font)
# define gui.interface_text_font = gui.preference(projz_gui_vars[2], gui.interface_text_font)
# define gui.button_text_font = gui.preference(projz_gui_vars[3], gui.button_text_font)
# define gui.choice_button_text_font = gui.preference(projz_gui_vars[4], gui.choice_button_text_font)
###################################################################################

################### Make font vars dynamic by our implementation ###################
define gui.text_font = get_selected_font(projz_gui_vars[0], gui.text_font)
define gui.name_text_font = get_selected_font(projz_gui_vars[1], gui.name_text_font)
define gui.interface_text_font = get_selected_font(projz_gui_vars[2], gui.interface_text_font)
define gui.button_text_font = get_selected_font(projz_gui_vars[3], gui.button_text_font)
define gui.choice_button_text_font = get_selected_font(projz_gui_vars[4], gui.choice_button_text_font)
####################################################################################

define projz_languages = {"korean": ("한국어", "SourceHanSansLite.ttf"), "japanese": ("日本語","SourceHanSansLite.ttf"), "french":("Русский","DejaVuSans.ttf"), "chinese": ("简体中文","SourceHanSansLite.ttf")}
define projz_fonts = ["DejaVuSans.ttf", "KMKDSP.ttf", "SourceHanSansLite.ttf"]


init python:
    from store import persistent, Action, DictEquality
    class ProjzFontAction(Action, DictEquality):
        def __init__(self, value, rebuild=True):
            self.value = value
            self.rebuild = rebuild

        def __call__(self):
            projz_set(projz_gui_selected_font, self.value)

            if self.rebuild:
                gui.rebuild()

        def get_selected(self):
            return projz_get(projz_gui_selected_font, None) == self.value

    class ProjzDefaultFontAction(Action, DictEquality):
        def __init__(self, rebuild=True):
            self.rebuild = rebuild

        def __call__(self):
            projz_set(projz_gui_selected_font, None)

            if self.rebuild:
                gui.rebuild()

        def get_selected(self):
            return projz_get(projz_gui_selected_font, None) == None
    
    def projz_show_i18n_settings():
        renpy.show_screen('projz_i18n_settings')

    config.underlay[0].keymap['projz_show_i18n_settings'] = projz_show_i18n_settings
    config.keymap['projz_show_i18n_settings'] = ['ctrl_K_i']

screen projz_i18n_settings():
    python:
        from store import persistent
        # save default fonts
        if projz_get(projz_gui_vars[0], None) is None:
            projz_set(projz_gui_vars[0], gui.text_font)
        if projz_get(projz_gui_vars[1], None) is None:
            projz_set(projz_gui_vars[1], gui.name_text_font)
        if projz_get(projz_gui_vars[2], None) is None:
            projz_set(projz_gui_vars[2], gui.interface_text_font)
        if projz_get(projz_gui_vars[3], None) is None:
            projz_set(projz_gui_vars[3], gui.button_text_font)
        if projz_get(projz_gui_vars[4], None) is None:
            projz_set(projz_gui_vars[4], gui.choice_button_text_font)
    tag menu
    use game_menu(_("I18n settings"), scroll="viewport"):
        vbox:
            hbox:
                box_wrap True
                vbox:
                    style_prefix "radio"
                    label _("Language")
                    textbutton "Default" action [Language(None)]
                    for k,v in projz_languages.items():
                        textbutton v[0] text_font v[1] action Language(k)
                ################### Make font vars dynamic by our implementation ###################
                vbox:
                    style_prefix "radio"
                    label _("Font")
                    textbutton "Default" action ProjzDefaultFontAction()
                    for f in projz_fonts:
                        textbutton f:
                            text_font f
                            action ProjzFontAction(f)
                ####################################################################################
                
                ################### Make font vars dynamic since Ren’Py 6.99.14 ###################
                # vbox:
                #     style_prefix "radio"
                #     label _("Font")
                #     textbutton "Default" action [gui.SetPreference(projz_gui_vars[0], persistent.projz_gui_text_font, rebuild=False), gui.SetPreference(projz_gui_vars[1], persistent.projz_gui_name_text_font, rebuild=False), gui.SetPreference(projz_gui_vars[2], persistent.projz_gui_interface_text_font, rebuild=False), gui.SetPreference(projz_gui_vars[3], persistent.projz_gui_button_text_font, rebuild=False), gui.SetPreference(projz_gui_vars[4], persistent.projz_gui_choice_button_text_font, rebuild=True)]
                #     for f in projz_fonts:
                #         textbutton f:
                #             text_font f
                #             action [gui.SetPreference(projz_gui_vars[0], f, rebuild=False), gui.SetPreference(projz_gui_vars[1], f, rebuild=False), gui.SetPreference(projz_gui_vars[2], f, rebuild=False), gui.SetPreference(projz_gui_vars[3], f, rebuild=False), gui.SetPreference(projz_gui_vars[4], f, rebuild=True)]
                ###################################################################################
                null height 10
                hbox:
                    style_prefix "slider"
                    box_wrap True
                    vbox:
                        label "Font size:"
                        bar value Preference("font size")
                        textbutton "Reset font size" action Preference("font size", 1.0)
                    vbox:
                        label "Font line spacing:"
                        bar value Preference("font line spacing")
                        textbutton "Reset line spacing" action Preference("font line spacing", 1.0)
            null height 10
            label "Watch"
            text _("font_size: [_preferences.font_size:.1]")
            text _("font_line_spacing: [_preferences.font_line_spacing:.1]")
            text _("text_font: [gui.text_font]")
            text _("text_font: [gui.text_font]")
            text _("name_text_font: [gui.name_text_font]")
            text _("interface_text_font: [gui.interface_text_font]")
            text _("button_text_font: [gui.button_text_font]")
            text _("choice_button_text_font: [gui.choice_button_text_font]")
            text _("language: [_preferences.language]")
            null height 10
            text _("This plugin is injected by the {a=https://github.com/abse4411/projz_renpy_translation}projz_renpy_translation{/a}.") xalign 1.0
            null height 60
