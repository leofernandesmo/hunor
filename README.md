#hunor

``` bash
usage: hunor [-h] [-m MAVEN_HOME] [-j JAVA_HOME]
             [--maven-timeout MAVEN_TIMEOUT] [--disable-randoop]
             [--disable-evosuite] -c CONFIG_FILE [-s SOURCE] [-o OUTPUT]
             --mutants MUTANTS [--coverage-threshold COVERAGE_THRESHOLD]
             --class SUT_CLASS --mutation-tool {major,mujava,pit}
```

Example:
``` bash
hunor -s example/relational -c example/relational/config.json --mutants example/relational/mutants 
--class br.ufal.ic.masg.operations.GreaterOrEqualThan
```
