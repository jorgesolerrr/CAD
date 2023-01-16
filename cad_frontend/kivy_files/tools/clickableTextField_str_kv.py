clickableTextField = """
<ClickableTextFieldRound>:
    size_hint_x: None
    size_hint_y: None
    width: "300dp"
    height: text_field.height
    drop: drop

    MDTextField:
        id: text_field
        hint_text: "search by course"
        text: root.text
        helper_text: "click on right icon for drop courses"
        helper_text_mode: "on_focus"
        icon_left: "school"

    MDIconButton:
        id : drop
        icon:"arrow-down-box"
        pos_hint: {"center_y": .5}
        pos: text_field.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release:
            root.createDrop()
            root.dropCourses()
"""