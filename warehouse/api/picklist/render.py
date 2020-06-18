from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
from random import randint
import dropbox


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}.pdf".format(params['picklist_id'])
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "picklist", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        file_from = file_path
        file_to = '/buymore2/picklist/'+file_name
        access_token = 'd7ElXR2Sr-AAAAAAAAAAC2HC0qc45ss1TYhRYB4Jy6__NJU1jjGiffP7LlP_2rrf'
        dbx = dropbox.Dropbox(access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

        return [file_name, file_path]
