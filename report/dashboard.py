import matplotlib.pyplot as plt
from employee_events import Employee, Team
from fasthtml.common import *

from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import BaseComponent, DataTable, Dropdown, MatplotlibViz, Radio
from combined_components import CombinedComponent, FormGroup


class ReportDropdown(Dropdown):

    def build_component(self, entity_id, model):
        self.label = model.name.title()

        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):

    def build_component(self, entity_id, model):
        return H1(model.name.title())


class LineChart(MatplotlibViz):

    def visualization(self, asset_id, model):

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        df = model.event_counts(asset_id)

        # Use the pandas .fillna method to fill nulls with 0
        df = df.fillna(0)

        # Use the pandas .set_index method to set
        # the date column as the index
        df = df.set_index("event_date")

        # Sort the index
        df = df.sort_index()

        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        df = df.cumsum()

        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        ax.set_title("Cumulative Event Counts", fontsize=20)
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")


class BarChart(MatplotlibViz):

    predictor = load_model()

    def visualization(self, asset_id, model):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        data = model.model_data(asset_id)

        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        predict_proba = self.predictor.predict_proba(data)

        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        predict_proba = predict_proba[:, 1].reshape(-1, 1)

        if model.name == "team":
            # If the model's name attribute is "team"
            # We want to visualize the mean of the predict_proba output
            pred = predict_proba.mean()
        else:
            # Otherwise set `pred` to the first value
            # of the predict_proba output
            pred = predict_proba[0][0]

        fig, ax = plt.subplots()

        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")


class Visualizations(CombinedComponent):

    children = [LineChart(), BarChart()]
    outer_div_type = Div(
        cls="grid", style="background-color: rgba(255, 255, 255, 0.5);"
    )


class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


class Report(CombinedComponent):

    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app, route = fast_app()

report = Report()


@app.route("/")
def get():
    return report(1, Employee())


@app.route("/employee/{id}")
def get_employee(id: int):
    return report(id, Employee())


@app.route("/team/{id}")
def get_team(id: int):
    return report(id, Team())


# Keep the below code unchanged!
@app.get("/update_dropdown{r}")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print("PARAM", r.query_params["profile_type"])
    if r.query_params["profile_type"] == "Team":
        return dropdown(None, Team())
    elif r.query_params["profile_type"] == "Employee":
        return dropdown(None, Employee())


@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse

    data = await r.form()
    profile_type = data._dict["profile_type"]
    id = data._dict["user-selection"]
    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
