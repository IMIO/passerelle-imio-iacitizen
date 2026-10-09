import logging

import django.apps

logger = logging.getLogger(__name__)


class AppConfig(django.apps.AppConfig):
    name = "passerelle_imio_iacitizen"
    verbose_name = "iA.Citizen"

    def ready(self):
        from passerelle.apps.plone_restapi.models import PloneRestApi
        from passerelle.base.models import BaseResource

        from .local_categories import sync_local_categories_queries

        if PloneRestApi.hourly is not BaseResource.hourly:
            logger.warning(
                "PloneRestApi defines its own hourly(): local categories synchronization disabled"
            )
            return
        PloneRestApi.hourly = sync_local_categories_queries
