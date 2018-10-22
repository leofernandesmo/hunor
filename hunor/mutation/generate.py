import os
import copy
import time

from hunor.tools.mujava import MuJava
from hunor.tools.java import JDK
from hunor.tools.maven import Maven
from hunor.utils import get_class_files, write_json, read_json, sort_files
from hunor.args import arg_parser, to_options
from hunor.main import Hunor
from hunor.db.models import Database
from hunor.db.queries import Queries


def main():
    options = to_options(arg_parser())

    jdk = JDK(options.java_home)

    mvn = Maven(
        jdk=jdk,
        maven_home=options.maven_home,
    )

    mvn.test(options.source)

    classes_dir = mvn.compile_project(options.source)

    if not os.path.exists(options.mutants):
        os.makedirs(options.mutants)

    tool = MuJava(options.mutants, jdk=jdk, classpath=classes_dir)
    # tool = Major(options.mutants, jdk=jdk, classpath=classes_dir)
    source_dir = os.path.join(options.source, 'src', 'main', 'java')

    files = get_class_files(source_dir, ext='.java')
    save_status_file = os.path.join(options.mutants, 'save_status.json')
    targets_file = os.path.join(options.mutants, 'targets.json')

    if os.path.exists(targets_file):
        targets = read_json(targets_file)
    else:
        targets = []

    if os.path.exists(save_status_file):
        save_status = read_json(save_status_file)
    else:
        save_status = {
            'files': [],
            'targets': 0
        }

    start_time = time.time()
    total_time = start_time - start_time
    count = 1

    db = Queries(Database(os.path.join(options.mutants, 'mutation.db')))
    db.create_tables()

    for i, file in enumerate(sort_files(files)):

        eta = ((total_time / count)
               * (len(files) - len(save_status['files']) - i))
        hours = eta // 3600
        minutes = (eta - (hours * 3600)) // 60
        seconds = (eta - (hours * 3600) - (minutes * 60))
        print('PROCESSING {0} {1}/{2} ETA: {3:.0f}h:{4:.0f}m:{5:.2f}s'.format(
            file, i + 1, len(files), hours, minutes, seconds))
        if file not in save_status['files']:
            start_time = time.time()
            t = tool.generate(classes_dir, source_dir, file, len(targets))
            print('\ttargets found: {0}'.format(len(t)))
            targets += t
            for target in t:
                o = copy.copy(options)
                o.mutants = os.path.join(o.mutants, str(target['id']))
                o.output = o.mutants
                o.sut_class = target['class']
                o.no_compile = True
                mutants, _ = Hunor(o).run()
                target['mutants'] = mutants

            for target in t:
                db.save_target_and_mutants(target, target['mutants'])

            save_status['files'].append(file)
            save_status['targets'] += len(t)
            write_json(save_status, 'save_status', options.mutants)
            write_json(targets, 'targets', options.mutants)

            count += 1
            total_time += (time.time() - start_time)


if __name__ == '__main__':
    main()
