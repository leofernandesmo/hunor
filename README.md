#hunor

pip install .

hunor -j <java_home> -m <maven_home> -s <maven project dir> -c <configuration file> -o <destination dir> --mutants <mutants dir> --class <sut class>
  
Example:

hunor -j /opt/java/jdk1.8.0_181 -m /opt/maven/current -s example/relational -c example/relational/config.json -o example/relational/output --mutants example/relational/mutants --class br.ufal.ic.masg.operations.GreaterOrEqualThan
