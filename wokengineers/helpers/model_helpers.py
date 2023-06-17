
from django.db.models.query import QuerySet
from kuantam.helpers.custom_helpers import CustomExceptionHandler
from kuantam.consts import STATUS_ACTIVE, CREATION_BY
from django.db import models
from kuantam.status_code import invalid_log_model, error_while_log_table_saving
import logging
import datetime
logger = logging.getLogger("django")

class CommonModel(models.Model):
    status = models.PositiveSmallIntegerField(null=False, default=STATUS_ACTIVE)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.TextField(null=False, default=CREATION_BY)
    updation_date = models.DateTimeField(null=True, auto_now=True)
    updation_by = models.TextField(null=True)

    class Meta:
        abstract = True


def add_log_model(logModel, modelInstance, modelName):
    """_summary_
    Args:
        logModel (_type_): Log Model that want to create/update 
        modelInstance (_type_): Model from which the data will be added
        modelName (_type_): Model Name use in error showing
    """
    try:
        logger.debug("Saving log model %s", modelInstance.__dict__)
        logModel = logModel()
        logModel.__dict__ = modelInstance.__dict__.copy()
        logModel.id = None
        logModel.log = modelInstance
        # request = get_request()
        logModel.created_by = CREATION_BY
        logModel.creation_date = datetime.datetime.now()
        logModel.save()
        return logModel
    except Exception as e:
        logger.exception("Exception is", e)
        raise CustomExceptionHandler(error_while_log_table_saving(f'{modelName} Log'))


class CustomUpdateManager(QuerySet):
    logModel_config = {}

    @staticmethod
    def set_logModel(logModel, model):
        CustomUpdateManager.logModel_config[model] = logModel

    def update(self, *args, **kwargs):
        logModel_name = CustomUpdateManager.logModel_config.get(self.model.__name__)
        logModel = None
        from django.apps import apps
        for app in apps.get_app_configs():
            for model in app.get_models():
                if model.__name__ == logModel_name:
                    logModel = model
                    break

        if logModel:
            instances = [instance.id for instance in self]
            super().update(*args, **kwargs) 
            for instance in self.model.filter(id__in = instances):
                add_log_model(logModel, instance, logModel.__name__)
        else:
            raise CustomExceptionHandler(invalid_log_model(self.model.__name__))
        
