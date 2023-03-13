"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc
from icecream import ic

from functools import partial

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

choices = ["C1", "C2", "C3"]

CHECK_LIMIT = 2

DEFAULT_DICT_CHECKBOX = {
    0: False,
    1: False,
    2: False,
}


class State(pc.State):
    """The app state."""

    checked: dict[int, bool] = {
        0: False,
        1: False,
        2: False,
    }

    disabled: dict[int, bool] = DEFAULT_DICT_CHECKBOX.copy()

    def check_box(self, index, value):
        self.checked[index] = not self.checked[index]
        if self.num_checked >= CHECK_LIMIT:
            ic("disable boxes not checked")
            for k, v in self.checked.items():
                self.disabled[k] = not v
            self.disabled = self.disabled
        else:
            self.disabled = DEFAULT_DICT_CHECKBOX.copy()
        ic(self.disabled, index)

    @pc.var
    def num_checked(self):
        return ic(sum(ck for ck in self.checked.values()))


def custom_checkbox(value, index):
    return pc.checkbox(
        value,
        value=State.checked[index],
        on_change=partial(
            State.check_box,
            index,
            value,
        ),
        is_disabled=State.disabled[index],
    )


def checkbox_group():
    return pc.vstack(
        pc.foreach(choices, lambda item, index: custom_checkbox(item, index))
    )


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Checkboxes group", font_size="2em"),
            pc.text("Select 2 items in this list:"),
            checkbox_group(),
            spacing="1.5em",
            font_size="2em",
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
