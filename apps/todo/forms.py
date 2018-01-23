# -*- coding: utf-8 -*-

import logging

from ..models import Todo
from utils import AttrDict, ParamsError

logger = logging.getLogger(__name__)


def postTodoListView(request):
    logger.info("postTodoListView params: %s", request.form)
    title = request.form.get("title")
    detail = request.form.get("detail")
    if None in (title, detail):
        raise(ParamsError)
    if len(title) > Todo.title.max_length:
        raise(ParamsError("title too long"))

    created_time = updated_time = Todo.created_time.default()

    form = {
        "title": title,
        "detail": detail,
        "created_time": created_time,
        "updated_time": updated_time
    }
    return AttrDict(form)
