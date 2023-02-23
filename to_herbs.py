import yaml
import sys

class Keybind:
    def __init__(self, keybind):
        self.keybind = keybind

    def name(self):
        return self.keybind.name

    def action(self):
        return self.keybind["action"]

    def keys(self):
        return [ Key(key) for key in self.keybind["keys"] ]


class Action:
    def __init__(self, action):
        self.action = action
            


class Key:
    def __init__(self, key):
        self.key = key

    def modifiers(self, format=None):
        if format == "herbstluftwm":
            return [
                "$Mod" if m == "mod"
                else m.capitalize()
                for m in self.key["modifier"]
            ]
        else:
            return self.key["modifier"]

    def key_formatted(self):
        key = self.key["key"]
        if len(key) > 1:
            return key.capitalize()
        else:
            return key

    def formatted(self, wm=None):
        mods = self.modifiers(wm)
        if wm == "herbstluftwm":
            return "-".join(mods + [self.key_formatted()])
        elif wm == "xmonad":
            return f"({' .|. '.join(mods)}, xK_{self.key_formatted()})"


def main():
    if len(sys.argv) < 2:
        print("Enter output format")
        exit(1)

    wm = sys.argv[1]

    with open("testdata/test.yml") as f:
        config = yaml.safe_load(f)
    
    for keybind in config["keybinds"]:
        keybind = Keybind(keybind)
        line = format_to_wm(keybind, wm)
        print(line)
    

def format_to_wm(keybind, wm):
    lines = []
    actions = keybind.action()
    if wm in actions:
        action = actions[wm]
    else:
        return ""

    for key in keybind.keys():
        key = key.formatted(wm)
        if wm == "herbstluftwm":
            lines.append(f"hc keybind {key} {action}")
        elif wm == "xmonad":
            lines.append(f", ({key}), {action})")
    return "\n".join(lines)
    

if __name__ == "__main__":
    main()
