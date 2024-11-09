from django_viewcomponent import component
from django_viewcomponent.fields import RendersManyField


@component.register("table")
class TabsComponent(component.Component):
    rows = RendersManyField(required=True)

    template_name = "table/table.html"

    def __init__(self, table_id, **kwargs):
        self.table_id = table_id
