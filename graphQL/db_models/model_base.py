from time import time
from mongoengine import Document
from mongoengine.fields import (
    IntField
)

class ModelBase(Document):
    meta = {'abstract': True}
    created_at = IntField()
    updated_at = IntField(default=lambda: int(time()))

    def clean(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = int(time())
        self.updated_at = int(time())

        return super(ModelBase, self).clean(*args, **kwargs)

