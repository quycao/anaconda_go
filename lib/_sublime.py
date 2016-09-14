
# Copyright (C) 2016 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

from functools import partial

from anaconda_go.lib import go
from anaconda_go.lib.helpers import get_settings, active_view
from anaconda_go.lib.plugin import anaconda_sublime, Worker, Callback

import sublime as st3_sublime


def fast_linters(view=None):
    """Run gometalinter fast linters only
    """

    if view is None:
        view = active_view()

    if not get_settings(view, 'anaconda_go_linting', True):
        return

    if view.file_name() in anaconda_sublime.ANACONDA['DISABLED']:
        anaconda_sublime.erase_lint_marks(view)
        return

    settings = _get_settings(view)

    data = {
        'vid': view.id(),
        'code': view.substr(st3_sublime.Region(0, view.size())),
        'settings': settings,
        'method': 'fast_lint',
        'handler': 'anaGonda',
        'go_env': {
            'GOROOT': go.GOROOT,
            'GOPATH': go.GOPATH,
            'CGO_ENABLED': go.CGO_ENABLED
        }
    }

    callback = partial(anaconda_sublime.parse_results, **dict(code='go'))
    Worker().execute(Callback(on_success=callback), **data)


def slow_linters(view=None):
    """Run slow gometalinter linters
    """

    if view is None:
        view = active_view()

    if not get_settings(view, 'anaconda_go_linting', True):
        return

    if view.file_name() in anaconda_sublime.ANACONDA['DISABLED']:
        anaconda_sublime.erase_lint_marks(view)
        return

    settings = _get_settings(view)

    data = {
        'vid': view.id(),
        'code': view.substr(st3_sublime.Region(0, view.size())),
        'settings': settings,
        'method': 'slow_lint',
        'handler': 'anaGonda',
        'go_env': {
            'GOROOT': go.GOROOT,
            'GOPATH': go.GOPATH,
            'CGO_ENABLED': go.CGO_ENABLED
        }
    }

    callback = partial(anaconda_sublime.parse_results, **dict(code='go'))
    Worker().execute(Callback(on_success=callback), **data)


def all_linters(view=None):
    """Run fast linters then slow linters
    """

    fast_linters(view)
    slow_linters(view)


def _get_settings(view):
    return {
        'linters': get_settings(view, 'anaconda_go_linters', []),
        'lint_test': get_settings(
            view, 'anaconda_go_lint_test', False),
        'exclude_regexps': get_settings(
            view, 'anaconda_go_exclude_regexps', []),
        'max_line_length': get_settings(
            view, 'anaconda_go_max_line_length', 120),
        'gocyclo_threshold': get_settings(
            view, 'anaconda_go_gocyclo_threshold', 10),
        'golint_min_confidence': get_settings(
            view, 'anaconda_go_golint_min_confidence', 0.80),
        'goconst_min_occurrences': get_settings(
            view, 'anaconda_go_goconst_min_occurrences', 3),
        'min_const_length': get_settings(
            view, 'anaconda_go_min_const_length', 3),
        'dupl_threshold': get_settings(
            view, 'anaconda_go_dupl_threshold', 50)
    }
