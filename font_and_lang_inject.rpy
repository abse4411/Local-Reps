


screen i18n_settings:
    ## Ensure other screens do not get input while this screen is displayed.
    modal True
    zorder 999
    key "K_i" action Hide('i18n_settings')
    frame:
        yalign 0.5
        xalign 0.5
        vbox:
            label "I18n Settings"
            text _("This plugin is injected by the {a=https://github.com/abse4411/projz_renpy_translation}project{/a}.")
            hbox:
                box_wrap True
                vbox:
                    style_prefix "radio"
                    label _("Language")
                    textbutton "Default" text_font "DejaVuSans.ttf" action Language(None)
                    textbutton "한국어" text_font "SourceHanSansLite.ttf" action Language("korean")
                    textbutton "日本語" text_font "SourceHanSansLite.ttf" action Language("japanese")
                    textbutton "简体中文" text_font "SourceHanSansLite.ttf" action Language("schinese")
                vbox:
                    style_prefix "radio"
                    label _("Font Family")
                    textbutton "DejaVuSans.ttf" text_font "DejaVuSans.ttf" action Language(None)
                    textbutton "SourceHanSansLite.ttf" text_font "SourceHanSansLite.ttf" action Language(None)
                    textbutton "SourceHanSansLite.ttf" text_font "SourceHanSansLite.ttf" action Language("japanese")
                    textbutton "SourceHanSansLite.ttf" text_font "SourceHanSansLite.ttf" action Language("schinese")
            spacing 20
            textbutton _("Hide(Press p Again)"):
                xalign 1.0
                action Hide("i18n_settings")
