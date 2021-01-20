@echo off
echo.
set classpath=%classpath%;data/POStagger.jar;data/maxent-3.0.0.jar;data/OpenNLP.jar;data/GGSEngine2.jar

java -Xms1200m -Dfile.encoding=utf-8 uaic.postagger.tagger.HybridPOStagger data/posRoDiacr.model data/posDictRoDiacr.txt data/guesserTagset.txt data/posreduction.ggf inputuri outputuri