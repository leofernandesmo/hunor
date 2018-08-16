import os

from argparse import ArgumentParser


def check_maven():
    if 'M2_HOME' in os.environ and os.environ['M2_HOME']:
        return os.environ['M2_HOME']
    elif 'MAVEN_HOME' in os.environ and os.environ['MAVEN_HOME']:
        return os.environ["MAVEN_HOME"]
    else:
        pass


def main():
    parser = ArgumentParser()

    parser.add_argument('-m', '--maven-home', action='store_true', dest='maven_home', default=check_maven)

    options = parser.parse_args()

    if callable(options.maven_home):
        options.maven_home()


if __name__ == '__main__':
    main()
