#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import ValidationError


class GreaterThan(object):
    """
    Compares the value of two fields. The value of self is to be greater than the supplied field.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext(u"Invalid field name '%s'.") % self.fieldname)

        print field
        print other

        print field.data <= other.data

        if field.data != '' and field.data <= other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            if self.message is None:
                self.message = field.gettext(u'Field must be greater than %(other_name)s.')

            raise ValidationError(self.message % d)

