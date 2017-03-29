def get_rofi(prompt='Launch: '):
    from dynmen.rofi import Rofi
    "Get a rofi menu object with my usual settings"
    menu = Rofi()
    menu.font = 'Dejavu Sans Mono 14'
    menu.color_window = "argb:dc222222, #fac863, #fac863"
    menu.color_normal = "argb:0000000, #ffffff, argb:0000000, #fac863, #1b2b34"
    menu.color_active = "argb:0000000, #6699cc, argb:0000000, #6699cc, #1b2b34"
    menu.color_urgent = "argb:0000000, #f99157, argb:0000000, #f99157, #1b2b34"
    menu.monitor = -1
    # menu.separator_style = 'dash'
    menu.prompt = prompt
    menu.i = True
    return menu

