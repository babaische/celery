from __future__ import absolute_import

from celery.utils.functional import firstmethod, mpromise
from celery.utils.imports import instantiate

_first_match = firstmethod("annotate")
_first_match_any = firstmethod("annotate_any")


def resolve_all(anno, task):
    return filter(None, (_first_match(anno, task), _first_match_any(anno)))


class MapAnnotation(dict):

    def annotate_any(self):
        try:
            return dict(self["*"])
        except KeyError:
            pass

    def annotate(self, task):
        try:
            return dict(self[task.name])
        except KeyError:
            pass


def prepare(annotations):
    """Expands the :setting:`CELERY_ANNOTATIONS` setting."""

    def expand_annotation(annotation):
        if isinstance(annotation, dict):
            return MapAnnotation(annotation)
        elif isinstance(annotation, basestring):
            return mpromise(instantiate, annotation)
        return annotation

    if annotations is None:
        return ()
    elif not isinstance(annotations, (list, tuple)):
        annotations = (annotations, )
    return map(expand_annotation, annotations)
