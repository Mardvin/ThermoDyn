from django.urls import path
from heat_losses_app import views
from heat_losses_app.views import update_predictions
from heat_losses_app.views.predict_pipeline import get_segment_data, updated_pipeline_table

urlpatterns = [
    path('heat_losses/', views.PipelineSegmentTable.as_view(), name='heat_losses'),
    path('heat_losses/add/', views.CreatePipelineSegment.as_view(), name='create_pipeline_segment'),
    path('heat_losses/edit/<int:pk>/', views.UpdatePipeline.as_view(), name='edit_pipeline'),
    path('heat_losses/delete/<int:pk>/', views.DeletePipeline.as_view(), name='delete_pipeline'),

    path('insulation_losses/', views.InsulationLossesView.as_view(), name='insulation_losses'),
    path('insulation_losses/add/', views.CreateInsulationLosses.as_view(), name='create_pipeline_insulation'),
    path('insulation_losses/edit/<int:pk>/', views.UpdateInsulationLosses.as_view(), name='edit_insulation'),
    path('insulation_losses/delete/<int:pk>/', views.DeleteInsulationLosses.as_view(), name='delete_insulation'),

    path('insulation_losse/result/', views.ResultLosses.as_view(), name='result_losses'),

    path('predict_pipeline/', views.PredictPipeline.as_view(), name='predict_pipeline'),
    path('get_segment_data/<int:segment_id>/', get_segment_data, name='get_segment_data'),
    path('update_predictions/', update_predictions, name='update_predictions'),
    path('get_updated_pipeline_table/', updated_pipeline_table, name='updated_pipeline_table'),
]
