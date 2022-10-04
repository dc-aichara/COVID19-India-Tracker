
import dash_daq as daq

def daq_display(value, clr):
        display = daq.LEDDisplay(
            label={
                "label": "  ",
                "style": {
                    "font-size": "14px",
                    "color": "green",
                    "font-family": "sans-serif",
                    "background": "white",
                    "padding": "2px",
                },
            },
            labelPosition="left",
            value=str(value),
            backgroundColor=clr,
            size=19,
            style={"display": "inline-block",},
        )
        return display