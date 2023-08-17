
from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from django.db.transaction import atomic

class CustomModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)


    def save_update_parent(self, validated_data,instance=None):
        child_data={}
        for field, property in self.get_fields().items():
            if isinstance(property, ListSerializer):
                data = validated_data.pop(self.fields[field].source,None)
                child_data[self.fields[field].source] = data
        if not instance:
            return super().create(validated_data), child_data
        else:
            return super().update(instance,validated_data), child_data

    def save_update_children(self, parent_instance, validated_data, save=True, update=False):
        for field, property in self.get_fields().items():
            if isinstance(property, ListSerializer):
                data = validated_data.pop(self.fields[field].source,None)
                if data:
                    if save and not update:
                        for child_data in data:
                            child_data['profile'] = parent_instance

                        self.fields[field].create(data)
                    if update and not save:
                        for child_data in data:
                            instance = child_data.pop("id")
                            if instance:
                                self.fields[field].child.update(instance,child_data)
                            else:
                                child_data['profile'] = parent_instance
                                self.fields[field].child.create(child_data)


    def partial_update_payload(self, instance, validated_data):
        
        pass


    @atomic
    def create(self, validated_data):
        parent_instance, child_data = self.save_update_parent(validated_data=validated_data)
        self.save_update_children(parent_instance, child_data)
        return parent_instance
    
    @atomic
    def update(self, parent_instance, validated_data):

        parent_instance, child_data = self.save_update_parent(instance = parent_instance, validated_data=validated_data)
        self.save_update_children(parent_instance, child_data, save=False, update=True)
        return parent_instance