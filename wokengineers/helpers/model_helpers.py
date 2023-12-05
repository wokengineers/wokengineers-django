
from django.db.models.query import QuerySet
from wokengineers.helpers.custom_helpers import CustomExceptionHandler
from wokengineers.consts import STATUS_ACTIVE, CREATION_BY
from django.db import models
from wokengineers.status_code import invalid_log_model, error_while_log_table_saving
from wokengineers.middleware.auth import get_request
from django.utils import timezone
import logging
import datetime
logger = logging.getLogger("django")

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
        request = get_request()
        logModel.creation_by = request.user_id if request else CREATION_BY
        logModel.creation_date = datetime.datetime.now()
        logModel.save()
        return logModel
    except Exception as e:
        logger.exception("Exception is", e)
        raise CustomExceptionHandler(error_while_log_table_saving(f'{modelName} Log'))

class CustomUpdateLogAdd(QuerySet):
    logModel_config = {}

    @staticmethod
    def set_logModel(logModel, model):
        CustomUpdateLogAdd.logModel_config[model] = logModel

    def update(self, *args, **kwargs):
        logModel_name = CustomUpdateLogAdd.logModel_config.get(self.model.__name__)
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
        
class CustomUpdateManager(QuerySet):
    def update(self, *args, **kwargs):
        kwargs["updation_date"] = timezone.now()
        if request := get_request():
            kwargs["updation_by"] = request.user_id
        else:
            kwargs["updation_by"] =  "Not API request"
        super().update(*args, **kwargs)

class AddCommonField(models.Model):
    objects = CustomUpdateManager.as_manager()
    status = models.PositiveSmallIntegerField(null=False, default=STATUS_ACTIVE)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    creation_by = models.TextField(null=False)
    updation_date = models.DateTimeField(null=True, auto_now=True)
    updation_by = models.TextField(null=True, blank=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        # Set the ‘updated_by’ field to the specified username or email
        update_field = kwargs.get('update_fields')
        if update_field:
            if "id" in update_field:
                update_field.remove('id')
            update_field.extend(["creation_date","creation_by",'updation_by',"updation_date"])
            
        if request := get_request():
            if not self.pk:
                self.creation_by = request.user_id
            self.updation_by = request.user_id
        else:
            self.creation_by = "Not API request"
            self.updation_by = "Not API request"
        super().save(*args, **kwargs)
        if not self.__dict__.get('log_id') and hasattr(self,'logs'):
            self.log_object = add_log_model(self.logs.model, self, self.__class__.__name__)






        

def get_model_data(model, error_1, error_2=None, **kwargs):
    try:
        intance = model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise CustomExceptionHandler(error_1)
    
    except model.MultipleObjectsReturned:
        raise CustomExceptionHandler(error_1)

    return intance