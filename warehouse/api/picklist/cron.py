from .models import Picklist, PicklistItemAlternate, PicklistItems
import requests

def generate_picklist():
    orders = []
    picklist = Picklist.objects.filter(status='Created').first()
    picklist.status='Generating'
    picklist.save()
    # Assign Picklist Items

