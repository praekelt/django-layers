from django.views.generic.base import TemplateView

from layers.decorators import exclude_from_layers


class NormalView(TemplateView):
    template_name = "layers/normal_view.html"


class WebOnlyView(TemplateView):
    template_name = "layers/web_only_view.html"

    @exclude_from_layers(layers=("basic",))
    def get(self, *args, **kwargs):
        return super(WebOnlyView, self).get(*args, **kwargs)
