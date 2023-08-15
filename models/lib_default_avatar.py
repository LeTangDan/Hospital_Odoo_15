import base64
from odoo.modules.module import get_module_resource


def _default_image():
    image_path = get_module_resource('hospital_management', 'static/description', 'images.png')
    return base64.b64encode(open(image_path, 'rb').read())
