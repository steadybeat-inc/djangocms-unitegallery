# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from cms.models import CMSPlugin
from cms.utils.compat.dj import python_2_unicode_compatible
# not needed anymore
# from sorl.thumbnail.templatetags.thumbnail import is_portrait

from filer.fields.image import FilerImageField

from .settings import DJANGOCMS_UNITEGALLERY_CONFIG as CONFIG


CONFIG.update(getattr(settings, 'DJANGOCMS_UNITEGALLERY_CONFIG', {}))

GALLERY_THEMES = (
    ('default', 'Default'),
    ('carousel', 'Carousel'),
    ('compact', 'Compact'),
    ('grid', 'Grid'),
    ('slider', 'Slider'),
    ('tiles', 'Tiles'),
    ('tilesgrid', 'Tiles grid'),
)


def get_media_path(instance, filename):
    return instance.gallery.get_media_path(filename)


@python_2_unicode_compatible
class Gallery(CMSPlugin):
    theme = models.CharField(
        _('Theme'),
        max_length=20,
        choices=GALLERY_THEMES,
        default=GALLERY_THEMES[0][0],
    )
    title = models.CharField(
        _("Title"),
        max_length=100,
        blank=True,
        help_text=_(
            "Leave this blank if you don't want to display a title."
        )
    )
    description = models.CharField(
        _("Description"),
        max_length=255,
        blank=True,
        help_text=_(
            "Leave this blank if you don't want to display a description."
        )
    )
    options = models.TextField(
        _('Theme options'),
        blank=True,
        help_text=_(
            'This field allow you to pass a JSON object if you want to '
            'customize the gallery. Please consult the Unite gallery docs '
            'for a list of options.'
        )
    )
    translatable_content_excluded_fields = ['options', 'theme']

    def __str__(self):
        if self.title:
            return self.title
        return self.get_theme_display()

    def copy_relations(self, old_instance):
        for photo in old_instance.photos.all():
            new_photo = GalleryPhoto(
                image=photo.image,
                title=photo.title,
                description=photo.description,
                gallery=self
            )
            new_photo.save()

    def clean(self):
        if self.options:
            try:
                json.loads(self.options)
            except ValueError:
                raise ValidationError('You must provide a valid JSON string')


@python_2_unicode_compatible
class GalleryPhoto(models.Model):
    image = FilerImageField(
        blank=True,
        null=True,
        related_name='gallery_photos',
        verbose_name=_('Photo'),
        help_text=_('Stores an image source file.')
    )
    title = models.CharField(
        _("Title"),
        max_length=100,
        blank=True,
        help_text=_(
            "Leave this blank if you don't want to display a title."
        )
    )
    description = models.CharField(
        _("Description"),
        max_length=255,
        blank=True,
        help_text=_(
            "Leave this blank if you don't want to display a description."
        )
    )
    gallery = models.ForeignKey(
        Gallery,
        verbose_name=_("Gallery"),
        related_name="photos"
    )

    def __str__(self):
        if self.title:
            return self.title
        if self.image:
          return _("Photo %s") % self.image.url
        return str(self.id)

    def get_thumbnail_size(self):
        """
        Returns a string representing the size of the thumbnail, suitable
        for sorl-thumbnail, eg.: '150', 'x200', '200x200', etc.
        """
        if not self.image or not CONFIG['THUMBNAIL_ENABLED']:
            return False
        if CONFIG['THUMBNAIL_PRESERVE_RATIO']:
            if self.image.height > self.image.width:
                ret = 'x%s' % CONFIG['THUMBNAIL_MAX_HEIGHT']
            else:
                ret = '%s' % CONFIG['THUMBNAIL_MAX_WIDTH']
        else:
            ret = '%sx%s' % (
                CONFIG['THUMBNAIL_MAX_WIDTH'], CONFIG['THUMBNAIL_MAX_HEIGHT']
            )
        return ret
