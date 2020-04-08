import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.transaction import atomic

logger = logging.getLogger('loggi.dispatch')


class Company(models.Model):
    name = models.CharField(max_length=200)
    shared_name = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=19, unique=True)
    landline_1 = models.CharField(max_length=22, db_index=True)
    has_cx_priority = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def can_make_orders(self):
        return self.verified

    def get_shared_name(self):
        return self.shared_name or self.name

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)


class LoggiUser(User):
    """
    This class adds the interesting bits on
    top of our the regular user model.
    """
    full_name = models.CharField(max_length=64, blank=True)
    mobile_1 = models.CharField(db_index=True, max_length=16,)
    email_is_verified = models.BooleanField(default=False)

    # email before the account was disabled
    original_email = models.CharField(max_length=256, blank=True, null=True)
    must_reset_password = models.BooleanField(default=False, db_index=True)

    company = models.ForeignKey(Company, related_name='users', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def disable(self):
        self.original_email = self.email
        self.email = self.email.replace(self.email.split('@')[0], 'inativo+{}'.format(self.id))
        self.is_active = self.is_superuser = self.is_staff = False
        self.mobile_1 = ''
        self.save()

    def enable(self):
        self.is_active = self.verified = True

        # Users deactivated before the original_email field was created have
        # it set as null. In those cases, the email field should remain
        # unchanged, no harm done
        self.email = self.original_email or self.email
        self.save()

    def set_password(self, raw_password):
        if raw_password and self.is_active:
            super(LoggiUser, self).set_password(raw_password)
        self.must_reset_password = False

    @atomic()
    def save(self, *args, **kwargs):
        self.full_name = '{} {}'.format(self.first_name, self.last_name).strip()

        super(LoggiUser, self).save(*args, **kwargs)

    def is_mobile_unique(self):
        return not LoggiUser.objects.exclude(pk=self.pk).filter(mobile_1=self.mobile_1).exists()

    def can_edit(self):
        if self.is_staff:
            return True
        if self.is_anonymous:
            return False
        return False

    def has_cx_priority(self):
        if self.company:
            return self.company.has_cx_priority

    def delete(self, *args, **kwargs):
        """
        We don't delete user objects from the db, as this would cause a bunch of
        problems (as showing a user that made the order 6 months in the past).
        """
        hard = kwargs.pop('hard_delete', False)
        if hard:
            logger.error('A user was hard deleted.')
            try:
                self.api_key.delete()
            except ObjectDoesNotExist:
                pass
            return super(LoggiUser, self).delete(*args, **kwargs)

        logger.info('A user was soft deleted')
        self.is_active = False
        self.save()
