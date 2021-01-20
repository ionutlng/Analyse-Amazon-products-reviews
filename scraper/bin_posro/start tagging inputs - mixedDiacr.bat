@echo off
echo.
echo parseaza toate documentele care nu sunt .xml din folderul "inputuri" si le salveaza ca xml in "outputuri"
set classpath=data/POStagger.jar;data/maxent-3.0.0.jar;data/OpenNLP.jar;data/GGSEngine2.jar

java -Xms1200m -Dfile.encoding=utf-8 uaic.postagger.tagger.HybridPOStagger data/posRoMixedDiacr.model data/posDictRoMixedDiacr.txt data/guesserTagset.txt data/posreduction.ggf inputuri outputuri