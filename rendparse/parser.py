"""
Classes and functions for parsing and processing the render csv files.
"""

from __future__ import division

import os
import csv
import re
import helpers

__author__ = "Ryan Tonini"


def filter_rows(filename, filters):
    """
    Generator function for data in the csv file.  It filters data according to the given conditions in filters.

    Input arguments
        - filename:   name of the csv file to be processed
        - filters:   dictionary of filter conditions
    Yield values:
        - render object corresponding to the next row in the file that satisfies the filter conditions
        -
    """
    with open(filename, "rU") as renderfile:
        renders = csv.reader(renderfile)
        for row in renders:
            # Create RenderRow object
            render = RenderRow(*row)

            # Check whether to skip this render
            # (i.e. if the render application and/or renderer don't match given values)
            skip_render = any((
                filters['app'] and filters['renderer'] and
                (filters['app'] != render.app or filters['renderer'] != render.renderer),
                filters['app'] and filters['app'] != render.app,
                filters['renderer'] and filters['renderer'] != render.renderer
            ))

            if skip_render:
                continue

            # yield only if render was successful or 'failed' flag is set to true
            if render.success or filters['failed']:
                yield render


class RenderFarmParser(object):
    """
    This class is responsible for parsing render files.
    """

    def __init__(self):
        # Stats of the render farm
        self._stats = None

    def run_parser(self, path, app=None, renderer=None, failed=False):
        """
        Read all valid filenames in the given path and process the contents of each file.
        Filter contents according to optional arguments.  This method also updates the
        render statistics after each render is read.

        Input arguments
        - path:   path to directory of csv files
        - app:   app name to filter on
        - renderer:   renderer to filter on
        - failed:   whether to include failed renders
        """
        self._stats = RenderStats()

        filters = {'app': app,
                   'renderer': renderer,
                   'failed': failed}

        # Read all files that are properly named
        filenames = [os.path.join(path, rf) for rf in os.listdir(path) if re.match(r'renders_\d{4}-\d{2}-\d{2}.csv', rf)]

        for fn in filenames:
            for render in filter_rows(fn, filters):
                # Update stats based on this render
                self._stats.update(render)

    def show_stats(self, output_type='count'):
        """
        Display stats as specified by output_type.

         Input arguments
        - output_type:  flag specifying what to output
        """
        if not self._stats:
            raise TypeError("self._stats is not defined. Try running run_parser first!")
        self._stats.print_spec(output_type)


class RenderStats(object):
    """
    This class keeps track of the overall render statistics.
    """

    def __init__(self):
        self._count = 0
        # Note the above count attribute may include failed renders with empty fields
        # (if 'failed' flag is true) thus skewing the other derived stats.  So each stat
        # will use its own counter for more accurate calculations.
        self._total_time = {'count': 0, 'value': 0}
        self._total_cpu = {'count': 0, 'value': 0}
        self._total_ram = {'count': 0, 'value': 0}
        self._max_cpu = {'uid': '', 'value': 0}
        self._max_ram = {'uid': '', 'value': 0}

    def update(self, render):
        """
        Process new render object and update stats.

        Input arguments
            - render: render object to process
        """
        self._count += 1

        # Ensure valid render fields (in case of failed renders)
        if render.render_time:
            self._total_time['count'] += 1
            self._total_time['value'] += render.render_time

        if render.peak_cpu:
            self._total_cpu['count'] += 1
            self._total_cpu['value'] += render.peak_cpu
            # Check if new render peak cpu is larger than current
            if render.peak_cpu > self._max_cpu['value']:
                self._max_cpu['uid'] = render.uid
                self._max_cpu['value'] = render.peak_cpu

        if render.peak_ram:
            self._total_ram['count'] += 1
            self._total_ram['value'] += render.peak_ram
            # Check if new render peak ram is larger than current
            if render.peak_ram > self._max_ram['value']:
                self._max_ram['uid'] = render.uid
                self._max_ram['value'] = render.peak_ram

    def print_spec(self, spec):
        """Print output specified by spec."""
        if spec == 'summary':
            print "{}\n{}\n{}\n{}\n{}".format(self.avgtime, self.avgcpu, self.avgram, self.maxram, self.maxcpu)
        else:
            print "{}".format(getattr(self, spec))

    @property
    def count(self):
        """Get the current total render count."""
        return self._count

    @property
    def avgtime(self):
        """Get the current average render time (sec)."""
        return (self._total_time['value'] / 1000) / self._total_time['count'] if self._total_time['count'] else 0

    @property
    def avgcpu(self):
        """Get the current avg peak CPU."""
        return (self._total_cpu['value'] / self._total_cpu['count']) if self._total_cpu['count'] else 0

    @property
    def avgram(self):
        """Get the current average RAM usage."""
        return (self._total_ram['value'] / self._total_ram['count']) if self._total_ram['count'] else 0

    @property
    def maxram(self):
        """Get the id with the current highest peak RAM."""
        return self._max_ram['uid']

    @property
    def maxcpu(self):
        """Get the id with the current highest peak CPU."""
        return self._max_cpu['uid']


class RenderRow(object):
    """
    This class represents a render item (single row in the csv).
    It is responsible for type casting and providing a simple to use interface for attribute access.
    """

    __slots__ = "uid", "app", "renderer", "num_frames", "success", "render_time", "peak_ram", "peak_cpu"

    def __init__(self, uid, app, renderer, num_frames, success, render_time, peak_ram, peak_cpu):
        # Set required properties of a render
        self.uid = uid
        self.app = app
        self.renderer = renderer
        self.num_frames = int(num_frames)
        self.success = True if success.strip() == 'true' else False
        # Set optional properties (try to cast to correct types, if unsuccessful set to None)
        self.render_time = helpers.try_except_typecast(int, render_time, None)
        self.peak_ram = helpers.try_except_typecast(float, peak_ram, None)
        self.peak_cpu = helpers.try_except_typecast(float, peak_cpu, None)

    def __iter__(self):
        """Iterate over attributes."""
        for attribute in self.__slots__:
            yield getattr(self, attribute)

    def __getitem__(self, index):
        """Return the attribute at the specified index."""
        return getattr(self, self.__slots__[index])





