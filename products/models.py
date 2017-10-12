from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Company(models.Model):
    full_name = models.CharField(max_length=120, unique=True)
    industry = models.CharField(max_length=40, blank=True)
    rep_name = models.CharField('representative name', max_length=120, blank=True)
    addr_1 = models.CharField(max_length=60, blank=True)
    addr_2 = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pin_code = models.CharField(max_length=10)
    website = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone1 = models.CharField(max_length=10, blank=True)
    phone2 = models.CharField(max_length=10, blank=True)
    phone3 = models.CharField(max_length=10, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('active', default=False)

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = 'companies'


    def __unicode__(self):
        return self.full_name + "-" + self.industry + "-" + self.city


class ProductCategory(models.Model):
    identifier = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ('identifier', 'name')

    def __unicode__(self):
        return self.name
        
    def active_commissions(self):
        return self.productcategorycommissions.filter(valid_from__lte=timezone.now(),
                                                      valid_to__gte=timezone.now(),
                                                      is_active=True
                                                      ).order_by('-valid_from', 'valid_to')

    def active_products(self):
        return self.categoryproducts.filter(is_active=True)

    def save(self, *args, **kwargs):
        self.identifier = self.identifier.upper()
        super(ProductCategory, self).save(*args, **kwargs)


class Product(models.Model):
    brand_name = models.CharField(max_length=120)
    company = models.ForeignKey(Company)
    content = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True,
                                       related_name='categoryproducts')
    strength = models.CharField(max_length=30, blank=True)
    pack = models.CharField(max_length=30, blank=True)
    mrp = models.DecimalField(max_digits=8, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('active', default=False)

    class Meta:
        ordering = ['brand_name']
        unique_together = ('brand_name', 'strength', 'pack', 'mrp')

    def __unicode__(self):
        return self.brand_name + " " + self.strength + " " + self.pack + " INR: " + str(self.mrp) + \
               str(self.created_on) + " - " + str(self.updated_on)

    @property
    def has_active_category_commission(self):
        if self.category is None or not self.category.active_commissions().exists():
            return False
        else:
            return True

    def clean(self):
        if self.is_active and not self.has_active_category_commission:
            raise ValidationError({'category': "Category with active commission is required "
                                                     "for an active product."})


class ProductCategoryCommission(models.Model):
    product_category = models.ForeignKey(ProductCategory, related_name='productcategorycommissions')
    commission_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField('active', default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('product_category', 'valid_from', 'valid_to'),
                           ('product_category', 'commission_percentage', 'valid_from', 'valid_to'),)

    def __unicode__(self):
        return self.product_category.__unicode__() + " - " + str(self.commission_percentage)

    def clean(self):
        if not self.is_active and self.product_category.active_products().exists() \
                and not self.product_category.active_commissions().exists():
            raise ValidationError({'is_active': "At least one currently active commission is required for "
                                                "active products of this category."})

        if self.valid_from > self.valid_to:
            raise ValidationError({'valid_from':'Valid from cannot be later than Valid to'})

        if self.valid_to < timezone.now():
            raise ValidationError({'valid_to':'Valid to cannot be in the past'})



class ProductOffer(models.Model):
    product = models.ForeignKey(Product, related_name='productoffers')
    offer = models.TextField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField('active', default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offer_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offer_updated_by',
                                   blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product.__unicode__() + ' - ' + self.offer

    def clean(self):
        if not self.product.is_active and self.is_active:
            raise ValidationError({'product': 'Product must be active to create a offer'})
        if self.valid_from > self.valid_to:
            raise ValidationError({'valid_from':'Valid from cannot be later than Valid to'})
        if self.valid_to < timezone.now():
            raise ValidationError({'valid_to': 'Valid to cannot be in the past'})
