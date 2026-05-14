################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            textbutton _("Q.Save") action QuickSave()
            textbutton _("Q.Load") action QuickLoad()
            textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size 75
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## 右侧导航按钮 #################################################################
##
## 在游戏界面右侧显示当前位置和地图入口。

screen quick_nav():
    zorder 100

    frame:
        xalign 1.0
        xoffset -20
        yalign 0.35
        xpadding 12
        ypadding 18
        xsize 120
        background "#000000bb"

        vbox:
            spacing 8
            xalign 0.5

            text "Ubicacion Actual":
                size 13
                color "#aaaaaa"
                xalign 0.5

            text "[current_location_name]":
                size 18
                color "#ffffff"
                xalign 0.5

            null height 8

            textbutton "Mapa":
                xalign 0.5
                text_size 22
                action Show("map_screen")

            null height 5

            textbutton "Hablar":
                xalign 0.5
                text_size 22
                action Show("talk_screen")

            null height 5

            textbutton "Debug":
                xalign 0.5
                text_size 18
                text_color "#ff8844"
                action Show("debug_screen")


## 地点NPC显示 ###################################################################
##
## 在当前地点显示可点击的NPC肖像。

screen location_npcs():
    tag npc_overlay
    zorder 50

    for npc_id, loc in npc_location.items():
        if loc == current_location:
            $ pos = NPC_POSITIONS.get(current_location, (300, 400))
            $ portrait = npc_portrait_map.get(npc_id, "")
            $ npc_name = NPC_NAMES.get(npc_id, "")

            imagebutton:
                idle Transform(portrait, xysize=(250, 350), fit="contain")
                hover Transform(portrait, xysize=(265, 370), fit="contain")
                pos pos
                anchor (0.5, 1.0)
                action [Hide("location_npcs"), SetVariable("talking_to_npc", npc_id), Jump("talk_npc")]

            text npc_name:
                pos (pos[0], pos[1] + 20)
                xanchor 0.5
                size 16
                color "#ffffff"
                outlines [(2, "#000000aa", 0, 0)]


## 凶器显示 #####################################################################
##
## 在当前地点显示已分配的凶器图片和名称。

screen weapons_display():
    zorder 40

    for wnum, (wloc, wx, wy) in weapon_placements.items():
        if wloc == current_location:
            $ wtype_idx = weapon_type.get(wnum, 0)
            $ wname, wimg = WEAPON_DATA[wtype_idx]

            imagebutton:
                pos (wx, wy)
                anchor (0.5, 1.0)
                idle Transform(wimg, xsize=200, fit="contain")
                hover Transform(wimg, xsize=210, fit="contain", matrixcolor=BrightnessMatrix(0.15))
                action [Hide("location_npcs"), SetVariable("inspecting_weapon", wnum), Jump("inspect_weapon")]

            text wname:
                pos (wx, wy + 5)
                anchor (0.5, 0.0)
                size 11
                color "#ffffff"
                textalign 0.5
                outlines [(1, "#000000cc", 0, 0)]


## 凶器调试标记 #################################################################
##
## 在所有可能刷新凶器的位置显示黄色半透明色块，方便调试。
## 已禁用 - 取消注释可重新启用。

# screen debug_weapon_slots():
#     zorder 35
#
#     for dloc, positions in WEAPON_SLOTS.items():
#         if dloc == current_location:
#             for (dx, dy) in positions:
#                 frame:
#                     pos (dx, dy)
#                     anchor (0.5, 1.0)
#                     xsize 28
#                     ysize 28
#                     padding (0, 0)
#                     background "#ffff0088"


## 交谈界面 #####################################################################
##
## 显示存活人物肖像（死者除外），点击可与其对话。

screen talk_screen():
    zorder 200
    modal True

    $ alive = [(nid, NPC_NAMES[nid], npc_portrait_map[nid]) for nid in npc_location.keys()]

    add "#000000cc"

    text "¿Con quien quieres hablar?":
        size 34
        color "#ffffff"
        xalign 0.5
        yalign 0.04
        font "DejaVuSans.ttf"

    vbox:
        xalign 0.5
        yalign 0.45
        spacing 35

        hbox:
            spacing 22
            xalign 0.5
            for nid, nname, nportrait in alive[:4]:
                button:
                    background None
                    hover_background "#ffffff22"
                    action [Hide("talk_screen"), SetVariable("talking_to_npc", nid), Jump("talk_npc")]
                    vbox:
                        xalign 0.5
                        add Transform(nportrait, xysize=(200, 250), fit="contain")
                        text nname:
                            size 12
                            color "#ffffff"
                            xalign 0.5

        if len(alive) > 4:
            hbox:
                spacing 22
                xalign 0.5
                for nid, nname, nportrait in alive[4:]:
                    button:
                        background None
                        hover_background "#ffffff22"
                        action [Hide("talk_screen"), SetVariable("talking_to_npc", nid), Jump("talk_npc")]
                        vbox:
                            xalign 0.5
                            add Transform(nportrait, xysize=(200, 250), fit="contain")
                            text nname:
                                size 12
                                color "#ffffff"
                                xalign 0.5

    textbutton "Cerrar":
        xalign 0.5
        yalign 0.90
        text_size 18
        action Hide("talk_screen")


## 地图界面 #####################################################################
##
## 显示豪宅各房间的地图，点击地点即可移动。

screen map_screen():
    zorder 200
    modal True

    # Dimmed background overlay
    add "#000000cc"

    # Titulo
    text "Mapa de la Mansion":
        size 36
        color "#ffffff"
        xalign 0.5
        yalign 0.04
        font "DejaVuSans.ttf"

    # Map image with transparent clickable hotspots
    fixed:
        xalign 0.5
        yalign 0.50

        add "gui/map/mini_map_bg.png"

        # --- Salon ---
        button:
            xpos 227  ypos 322
            xsize 404  ysize 187
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("salon")]

        # --- Master Bedroom ---
        button:
            xpos 716  ypos 91
            xsize 234  ysize 160
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("master_bedroom")]

        # --- Guest Quarters ---
        button:
            xpos 335  ypos 91
            xsize 106  ysize 132
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("guest_quarters")]

        # --- Kitchen ---
        button:
            xpos 159  ypos 90
            xsize 165  ysize 215
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("kitchen")]

        # --- Garden ---
        button:
            xpos 298  ypos 583
            xsize 346  ysize 76
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("garden")]

        # --- Pool ---
        button:
            xpos 916  ypos 442
            xsize 245  ysize 183
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("pool")]

        # --- Library ---
        button:
            xpos 453  ypos 91
            xsize 240  ysize 159
            background None
            hover_background "#ffffff22"
            action [Hide("map_screen"), Jump("library")]

        # --- Hidden Room (only after discovery) ---
        if hidden_room_found:
            button:
                xpos 647  ypos 267
                xsize 94  ysize 70
                background None
                hover_background "#ffffff22"
                action [Hide("map_screen"), Jump("hidden_room")]

    # Boton de cierre
    textbutton "Cerrar":
        xalign 0.5
        yalign 0.90
        text_size 18
        action Hide("map_screen")


## 第一人称手部 #################################################################
##
## 屏幕底部显示左右手图片，模拟第一人称视角。
## 左手点击 = Look Around，右手点击 = Open Map。

image left_hand_idle = Transform("images/Left_hand.png", xsize=420, fit="contain")
image left_hand_hover = Transform("images/Left_hand.png", xsize=420, fit="contain", matrixcolor=BrightnessMatrix(0.12))
image right_hand_idle = Transform("images/Right_hand.png", xsize=420, fit="contain")
image right_hand_hover = Transform("images/Right_hand.png", xsize=420, fit="contain", matrixcolor=BrightnessMatrix(0.12))

screen hands_display():
    zorder 150

    # Left hand - Look Around
    imagebutton:
        idle "left_hand_idle"
        hover "left_hand_hover"
        xalign 0.0
        yalign 1.0
        action Jump(current_location + "_look")

    # Right hand - Open Map
    imagebutton:
        idle "right_hand_idle"
        hover "right_hand_hover"
        xalign 1.0
        yalign 1.0
        action Show("map_screen")


## 倒计时 #########################################################################
##
## 屏幕右上角显示10分钟倒计时。时间归零后强制进入指认阶段。
## 也可手动点击倒计时区域进入指认阶段（可通过退出按钮退出）。

screen countdown_timer():
    zorder 200

    if time_left > 0:
        timer 1.0 repeat True action [
            SetVariable("time_left", time_left - 1),
            If(time_left <= 1, [
                SetVariable("accusation_active", True),
                SetVariable("accusation_manual", False),
                Show("accusation_screen")
            ])
        ]

    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 10
        xpadding 14
        ypadding 8
        background "#000000bb"

        button:
            background None
            hover_background "#ffffff33"
            action [
                SetVariable("accusation_active", True),
                SetVariable("accusation_manual", True),
                Show("accusation_screen")
            ]

            vbox:
                xalign 0.5
                spacing 2
                text "Tiempo" size 12 color "#aaaaaa" xalign 0.5
                $ mins = max(0, time_left // 60)
                $ secs = max(0, time_left % 60)
                text "[mins:02d]:[secs:02d]" size 24 color "#ffffff" xalign 0.5


## 指认阶段 #####################################################################
##
## 指认阶段界面。手动进入时可退出，倒计时归零时强制进入不可退出。

screen accusation_screen():
    zorder 300
    modal True

    add "#000000cc"

    add "images/fase/pantallafinal.png":
        xalign 0.5
        yalign 0.5
        xsize 1550
        fit "contain"

    # Selection area centered over the background
    vbox:
        xalign 0.5
        yalign 0.5
        xmaximum 1450
        spacing 10

        # --- Culprit ---
        frame:
            xalign 0.5  xsize 200
            background "#00000088"
            text "CULPABLE" size 20 color "#ffffff" xalign 0.5

        hbox:
            xalign 0.5
            spacing 8
            $ alive_npcs = [(nid, NPC_NAMES[nid], npc_portrait_map[nid]) for nid in npc_location.keys()]
            for nid, nname, nportrait in alive_npcs:
                $ sel = (accusation_char == nid)
                button:
                    xsize 145  ysize 180
                    background ("#4488ff" if sel else "#222222")
                    hover_background "#666666"
                    action SetVariable("accusation_char", nid)
                    vbox:
                        xalign 0.5  yalign 0.5  spacing 5
                        add Transform(nportrait, xsize=115, ysize=140, fit="contain") xalign 0.5
                        text nname size 12 color "#ffffff" xalign 0.5 textalign 0.5

        # --- Accomplice ---
        frame:
            xalign 0.5  xsize 200
            background "#00000088"
            text "COMPLICE" size 20 color "#ffffff" xalign 0.5

        hbox:
            xalign 0.5
            spacing 8
            $ all_npcs = [(nid, NPC_NAMES[nid], npc_portrait_map[nid]) for nid in npc_portrait_map.keys() if nid != victim_id]
            for nid, nname, nportrait in all_npcs:
                $ sel = (accusation_accomplice == nid)
                button:
                    xsize 145  ysize 180
                    background ("#cc8844" if sel else "#222222")
                    hover_background "#666666"
                    action SetVariable("accusation_accomplice", nid)
                    vbox:
                        xalign 0.5  yalign 0.5  spacing 5
                        add Transform(nportrait, xsize=115, ysize=140, fit="contain") xalign 0.5
                        text nname size 12 color "#ffffff" xalign 0.5 textalign 0.5

        # --- Weapons ---
        frame:
            xalign 0.5  xsize 200
            background "#00000088"
            text "ARMAS" size 20 color "#ffffff" xalign 0.5

        hbox:
            xalign 0.5
            spacing 6
            for wnum in range(1, 14):
                $ sel = (accusation_weapon == wnum)
                $ wtype_idx = weapon_type.get(wnum, 0)
                $ wname, wimg = WEAPON_DATA[wtype_idx]
                button:
                    xsize 90  ysize 105
                    background ("#ff4444" if sel else "#222222")
                    hover_background "#666666"
                    action SetVariable("accusation_weapon", wnum)
                    vbox:
                        xalign 0.5  yalign 0.5  spacing 4
                        add Transform(wimg, xsize=65, fit="contain") xalign 0.5
                        text wname size 10 color "#ffffff" xalign 0.5 textalign 0.5

        # Weapon feedback text
        if accusation_weapon is not None:
            $ wtype_idx = weapon_type.get(accusation_weapon, 0)
            $ sel_wname, sel_wimg = WEAPON_DATA[wtype_idx]
            frame:
                xalign 0.5
                xpadding 14  ypadding 6
                background "#ff444488"
                hbox:
                    xalign 0.5
                    spacing 10
                    add Transform(sel_wimg, xsize=35, fit="contain")
                    text "Arma seleccionada: [sel_wname]":
                        size 16
                        color "#ffffff"
                        yalign 0.5

        # --- Locations ---
        frame:
            xalign 0.5  xsize 200
            background "#00000088"
            text "LUGARES" size 20 color "#ffffff" xalign 0.5

        hbox:
            xalign 0.5
            spacing 8
            for loc_id in LOCATIONS_FOR_NPC:
                $ sel = (accusation_location == loc_id)
                $ loc_data = locations.get(loc_id, {})
                $ loc_name = loc_data.get("name", loc_id)
                $ loc_img = loc_data.get("image", "")
                button:
                    xsize 145  ysize 105
                    background ("#4488ff" if sel else "#222222")
                    hover_background "#666666"
                    action SetVariable("accusation_location", loc_id)
                    vbox:
                        xalign 0.5  yalign 0.5  spacing 3
                        add Transform(loc_img, xsize=120, ysize=60, fit="contain") xalign 0.5
                        text loc_name size 11 color "#ffffff" xalign 0.5

        null height 6

        # --- Accuse button ---
        textbutton "¡Acusar!":
            xalign 0.5
            text_size 26
            action [
                SetVariable("accusation_active", False),
                Jump("accusation_result")
            ]

    # Exit button
    if accusation_manual:
        textbutton "Salir de la Acusacion":
            xalign 0.5
            yalign 0.92
            text_size 16
            action [
                SetVariable("accusation_active", False),
                SetVariable("accusation_manual", False),
                SetVariable("accusation_char", None),
                SetVariable("accusation_weapon", None),
                SetVariable("accusation_location", None),
                SetVariable("accusation_accomplice", None),
                Hide("accusation_screen")
            ]


## 调试菜单 #####################################################################
##
## 显示案件答案和推理逻辑，方便开发调试。

screen debug_screen():
    zorder 300
    modal True

    add "#000000cc"

    vbox:
        xalign 0.5
        yalign 0.5
        xmaximum 800
        spacing 12

        text "INFO DEPURACION" size 30 color "#ff8844" xalign 0.5

        null height 10

        frame:
            background "#1a1a1acc"
            xpadding 20 ypadding 15
            vbox:
                spacing 8

                hbox:
                    text "Asesino:" size 18 color "#aaaaaa" xsize 180
                    text "[murderer_name]" size 22 color "#ff4444"

                hbox:
                    text "Complice:" size 18 color "#aaaaaa" xsize 180
                    if accomplice_name:
                        text "[accomplice_name]" size 22 color "#ff8844"
                    else:
                        text "Ninguno" size 22 color "#888888"

                hbox:
                    text "Escena del Crimen:" size 18 color "#aaaaaa" xsize 180
                    text "[crime_scene_name]" size 22 color "#4488ff"

                hbox:
                    text "Arma:" size 18 color "#aaaaaa" xsize 180
                    text "[weapon_name_str]" size 22 color "#ff4444"

        null height 8

        frame:
            background "#1a1a1acc"
            xpadding 20 ypadding 15
            vbox:
                spacing 5
                text "Razonamiento" size 20 color "#ff8844"

                null height 4

                if debug_reasoning:
                    text "[debug_reasoning]" size 15 color "#cccccc"
                else:
                    text "Compara las pistas resaltadas en rojo en los dialogos de los NPC y los examenes de la escena del crimen.\nLas inconsistencias te señalaran al asesino, el arma y la ubicacion." size 15 color "#888888"

    textbutton "Cerrar":
        xalign 0.5
        yalign 0.88
        text_size 18
        action Hide("debug_screen")


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
