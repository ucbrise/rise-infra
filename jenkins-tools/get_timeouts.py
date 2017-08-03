#!/usr/bin/env python2

"""scan jenkins build logs for github timeouts."""

from collections import defaultdict, OrderedDict
import os
import re
import sys
import time

def get_builds(base_jobs_dir, days_to_check):
    build_count=0

    for d in os.listdir(base_jobs_dir):
        base_build_dir = os.path.join(base_jobs_dir, d, 'builds')

        # we have some orphaned/archived builds, so skip over them
        if os.path.exists(base_build_dir):
            for build_dir in os.listdir(base_build_dir):
                build_dir = os.path.join(base_build_dir, build_dir)
                build_log = os.path.join(build_dir, 'log')

                # skip over symlinks for lastStable and lastSuccessful as this
                # will potentially screw up the report
                if os.path.islink(build_dir):
                    next

                if os.path.exists(build_log):
                    build_time = os.path.getctime(build_log)
                    if build_time > days_to_check:
                        build_count += 1
                        yield (build_log, build_time)

    # now overload our yield to report back the total number of builds.
    yield ('TOTAL_BUILDS', build_count)

def get_timeouts(base_jobs_dir, days_to_check):
    # only check the first N lines for git timeouts
    max_length_to_check = 100
    retval = defaultdict(list)
    timeout_error = 'ERROR: Timeout after'
    timeouts = []
    total_builds = 0

    for logfile, timeout in get_builds(base_jobs_dir, days_to_check):

        # this means we're done scanning all the build logs, so break out of
        # this loop
        if logfile == 'TOTAL_BUILDS':
            total_builds = timeout
            break

        count = 0
        for line in open(logfile, 'r'):
            if count > max_length_to_check:
                break

            if timeout_error in line:
                project_name = logfile.split('/')[5]
                timeouts.append((project_name, timeout))
                break
            count += 1

    for k, v in timeouts:
        retval[k].append(v)
    return (retval, total_builds)

def main():
    if len(sys.argv) < 2:
        print 'Usage: %s <number of days back to check for git timeouts>' % sys.argv[0]
        sys.exit()

    now = time.time()
    time_window = int(sys.argv[1])
    days_to_check = now - 60*60*24*time_window
    base_jobs_dir = '/var/lib/jenkins/jobs'

    # now find jobs with git timeouts.  this happens in the first ~10 lines of the log file,
    # so we can bail if we don't find this by 20 lines in.
    timeouts, total_builds = get_timeouts(base_jobs_dir, days_to_check)

    # now munge the data and print out unique build names, number of failures for each, date of failures
    timeouts_by_day = defaultdict(int)
    total_failures = 0
    for fail_dates in timeouts.values():
        total_failures = total_failures + len(fail_dates)

    print "Timeouts by project:"
    for project, timeout_list in timeouts.iteritems():
        print ' %s\t%s' % (len(timeout_list), project)
        for timestamp in timeout_list:
            date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))
            timeouts_by_day[date] += 1

    print
    print "Timeouts by day:"
    d = OrderedDict(sorted(timeouts_by_day.items()))
    for day, count in d.iteritems():
        print '%s\t%s' % (day, count)

    print
    print "Total builds:\t%s" % total_builds
    print "Total timeouts:\t%s" % total_failures

    percent_failures = 100 * float(total_failures) / float(total_builds)
    print "Percentage of all builds timing out:\t%s" % percent_failures


if __name__ == "__main__":
    main()
