from django.utils.text import slugify

LOCAL_VOCABULARIES = {
    "imio.events.Event": "imio.events.vocabulary.EventsLocalCategories",
    "imio.news.NewsItem": "imio.news.vocabulary.NewsLocalCategories",
}


def local_query_slug(title):
    return "local-%s" % slugify(title)[:120]


def get_portal_type(query):
    for line in query.filter_expression.splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == "portal_type":
            return value.strip()
    return None


def build_filter_expression(portal_type, title):
    value = title
    if any(char in value for char in "&+%#="):
        from urllib.parse import quote

        value = quote(value)
    return "portal_type=%s\r\nreview_state=published\r\ncategory_and_topics=%s" % (portal_type, value)


def sync_local_categories_queries(self):
    """Tâche horaire posée sur PloneRestApi : une requête par catégorie spécifique Smartweb."""
    from passerelle.apps.plone_restapi.models import Query

    model_query = None
    for query in self.queries.order_by("pk"):
        if not query.slug.startswith("local-") and get_portal_type(query) in LOCAL_VOCABULARIES:
            model_query = query
            break
    if model_query is None:
        return

    portal_type = get_portal_type(model_query)
    response = self.request(
        path="@vocabularies/%s" % LOCAL_VOCABULARIES[portal_type], params={"b_size": 999999}
    )
    seen_slugs = set()
    for category in (response or {}).get("items") or []:
        title = category["title"]
        slug = local_query_slug(title)
        if slug in seen_slugs:
            self.logger.warning("local category %r ignored: slug %s already used", title, slug)
            continue
        seen_slugs.add(slug)
        query, created = Query.objects.update_or_create(
            resource=self,
            slug=slug,
            defaults={
                "name": title,
                "description": "Catégorie spécifique",
                "uri": model_query.uri,
                "text_template": model_query.text_template,
                "filter_expression": build_filter_expression(portal_type, title),
                "sort": model_query.sort,
                "order": model_query.order,
                "limit": model_query.limit,
            },
        )
        if created:
            self.logger.info("local category query created: %s (%s)", slug, title)
