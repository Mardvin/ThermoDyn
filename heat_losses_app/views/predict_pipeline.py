from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from heat_losses_app.models import PredictPipline


class PredictPipeline(ListView):
    model = PredictPipline
    template_name = 'heat_losses_app/list_predict_pipeline.html'
    context_object_name = 'pipeline'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pipelines'] = PredictPipline.objects.filter(replacement="Да").select_related('pipeline_segment_loss__pipeline_segment')
        return context

def get_segment_data(request, segment_id):
    segment = PredictPipline.objects.select_related('pipeline_segment_loss').get(id=segment_id)
    old_loss = segment.pipeline_segment_loss.heat_loss_year or 0
    new_loss = segment.heat_loss_year or 0
    data = {
        'old_loss': float(old_loss),
        'new_loss': float(new_loss),
    }
    return JsonResponse(data)


@csrf_exempt
def update_predictions(request):
    if request.method == "POST":
        try:
            PredictPipline.objects.update_or_create_for_all_heat_loss_insulations()
            return JsonResponse({"status": "success", "message": "Перерасчет выполнен"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
