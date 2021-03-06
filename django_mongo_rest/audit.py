from django_mongo_rest.models import BaseModel
from django_mongo_rest.utils import Enum
from django_mongoengine.mongo_auth.managers import get_user_document
from mongoengine import DynamicDocument, StringField, ReferenceField, ObjectIdField

class ACTIONS(Enum):
    CREATE = 'C'
    UPDATE = 'U'
    DELETE = 'D'

class Audit(BaseModel, DynamicDocument):

    meta = {
        'indexes': ['doc_id']
    }

    user = ReferenceField(get_user_document())
    model = StringField()
    doc_id = ObjectIdField()
    action = StringField(choices=ACTIONS.choices_dict().items())

def create(request, action, model_class, doc, extra_data):
    audit_doc = {
        'user': request.user.id,
        'model': model_class.get_collection_name(),
        'action': action.value,
        'doc_id': doc['_id'] if isinstance(doc, dict) else doc,
    }

    audit_doc.update(extra_data)
    Audit.insert_one(audit_doc)

def update(request, model_class, doc, updates):
    for k, v in updates.iteritems():
        doc[k] = v

    model_class.update_by_id(doc['_id'], **updates)
    create(request, ACTIONS.UPDATE, model_class, doc, updates)
