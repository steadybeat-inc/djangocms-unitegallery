# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import Gallery, CONFIG
from .admin import PhotoInline


class GalleryPlugin(CMSPluginBase):
    """
    The gallery plugin instance.
    """
    model = Gallery
    name = _('Gallery')
    module = _('Unite gallery')
#    render_template = self.get_template()
    inlines = [PhotoInline, ]

    def get_render_template(self, context, instance, placeholder):
        default = 'djangocms_unitegallery/gallery.html'
        if CONFIG['USE_EASYTHUMBNAILS']:
            default = 'djangocms_unitegallery/easythumb-gallery.html'
        return default

    def render(self, context, instance, placeholder):
        context.update({
            'gallery': instance,
            'placeholder': placeholder,
            'CONFIG': CONFIG
        })
        return context


plugin_pool.register_plugin(GalleryPlugin)
