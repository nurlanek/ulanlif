from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator:
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Bu parolanın en az %(min_length)d karakter uzunluğunda olması gerekmektedir."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _("Parola en az %(min_length)d karakter uzunluğunda olmalıdır.") % {'min_length': self.min_length}
