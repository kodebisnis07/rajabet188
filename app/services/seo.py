def meta_payload(seo):
    return {
        'title': seo.meta_title if seo else 'Rajabet188',
        'description': seo.meta_description if seo else 'Platform hiburan premium dark gold.',
        'og_image': seo.og_image if seo else ''
    }
