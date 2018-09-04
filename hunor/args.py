from argparse import ArgumentParser


def arg_parser():
    parser = ArgumentParser()

    parser.add_argument('-m', '--maven-home',
                        action='store',
                        dest='maven_home')

    parser.add_argument('-j', '--java-home',
                        action='store',
                        dest='java_home')

    parser.add_argument('--maven-timeout',
                        action='store',
                        dest='maven_timeout',
                        default='3600')

    parser.add_argument('--disable-randoop',
                        action='store_true',
                        dest='is_randoop_disabled')

    parser.add_argument('--disable-evosuite',
                        action='store_true',
                        dest='is_evosuite_disabled')

    parser.add_argument('-c', '--config_file',
                        action='store',
                        dest='config_file',
                        required=True)

    parser.add_argument('-s', '--source',
                        action='store',
                        dest='source')

    parser.add_argument('-o', '--output',
                        action='store',
                        dest='output',
                        default='hunor-output')

    parser.add_argument('--mutants',
                        action='store',
                        dest='mutants',
                        required=True)

    parser.add_argument('--coverage-threshold',
                        action='store',
                        dest='coverage_threshold',
                        default='0')

    parser.add_argument('--class',
                        action='store',
                        dest='sut_class',
                        required=True)

    return parser
